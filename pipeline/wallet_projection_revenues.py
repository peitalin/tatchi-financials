from __future__ import annotations

import math
import random
from datetime import date
from pathlib import Path
from typing import Any
from typing import Sequence

try:
    from .assumptions import PROJECTION_MONTHS
    from .assumptions import REVENUE_ASSUMPTIONS
    from .projection_workbook import write_projection_workbook
    from .runtime_config import DATA_PATHS
except ImportError:
    from assumptions import PROJECTION_MONTHS
    from assumptions import REVENUE_ASSUMPTIONS
    from projection_workbook import write_projection_workbook
    from runtime_config import DATA_PATHS

SCRIPT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = SCRIPT_DIR / "data"


def _add_months(value: date, months: int) -> date:
    zero_based = value.month - 1 + months
    year = value.year + zero_based // 12
    month = zero_based % 12 + 1
    return date(year, month, 1)


def _year_index(index: int) -> int:
    if index < 12:
        return 1
    if index < 24:
        return 2
    return 3


def _phase_label(index: int) -> str:
    if index < 12:
        return "phase_1_launch"
    if index < 24:
        return "phase_2_scale"
    return "phase_3_optimization"


def _seasonality_factors() -> dict[int, float]:
    factors = REVENUE_ASSUMPTIONS.monthly_seasonality_factors
    if len(factors) != 12:
        raise ValueError("monthly_seasonality_factors must contain 12 values")
    output: dict[int, float] = {}
    for month, value in enumerate(factors, start=1):
        if value <= 0:
            raise ValueError("monthly_seasonality_factors values must be > 0")
        output[month] = float(value)
    return output


def _clamp(value: float, floor: float, ceiling: float) -> float:
    return max(floor, min(ceiling, value))


def _adoption_rate_for_index(
    *,
    index: int,
    launch_month_offset: int,
    start_rate: float,
    end_rate: float,
) -> float:
    if index < launch_month_offset:
        return 0.0
    months_after_launch = index - launch_month_offset
    ramp_denominator = max(1, PROJECTION_MONTHS - launch_month_offset - 1)
    progress = _clamp(months_after_launch / ramp_denominator, 0.0, 1.0)
    return _clamp(start_rate + (end_rate - start_rate) * progress, 0.0, 1.0)


def _build_escrow_rows(
    *,
    projection_start: date,
    monthly_factors: dict[int, float],
    jitter_std: float,
    seed: int,
) -> list[dict[str, Any]]:
    rng = random.Random(seed)
    baseline_factor = monthly_factors[projection_start.month]

    rows: list[dict[str, Any]] = []
    for index in range(PROJECTION_MONTHS):
        month_start = _add_months(projection_start, index)
        seasonality_ratio = monthly_factors[month_start.month] / baseline_factor
        volume_growth = math.pow(
            1 + REVENUE_ASSUMPTIONS.escrow_volume_annual_growth,
            index / 12,
        )
        txn_growth = math.pow(
            1 + REVENUE_ASSUMPTIONS.escrow_transactions_annual_growth,
            index / 12,
        )
        volume_noise = max(0.82, 1 + rng.gauss(0.0, jitter_std * 0.35))
        txn_noise = max(0.82, 1 + rng.gauss(0.0, jitter_std * 0.30))
        escrow_volume_usd = (
            REVENUE_ASSUMPTIONS.baseline_monthly_escrow_volume_usd
            * volume_growth
            * seasonality_ratio
            * volume_noise
        )
        escrow_transaction_count = int(
            round(
                REVENUE_ASSUMPTIONS.baseline_monthly_escrow_transactions
                * txn_growth
                * seasonality_ratio
                * txn_noise
            )
        )
        escrow_transaction_count = max(1, escrow_transaction_count)
        avg_escrow_size_usd = escrow_volume_usd / escrow_transaction_count
        escrow_fee_revenue_usd = escrow_volume_usd * REVENUE_ASSUMPTIONS.escrow_fee_rate
        rows.append(
            {
                "month": str(month_start),
                "year_index": _year_index(index),
                "phase": _phase_label(index),
                "escrow_transaction_count": escrow_transaction_count,
                "avg_escrow_size_usd": round(avg_escrow_size_usd, 2),
                "escrow_volume_usd": round(escrow_volume_usd, 2),
                "escrow_fee_rate": round(REVENUE_ASSUMPTIONS.escrow_fee_rate, 4),
                "escrow_fee_revenue_usd": round(escrow_fee_revenue_usd, 2),
                "settlement_stablecoin": REVENUE_ASSUMPTIONS.escrow_settlement_stablecoin,
            }
        )
    return rows


def _cohort_growth_rate_for_index(index: int) -> float:
    if index < 12:
        return REVENUE_ASSUMPTIONS.new_users_monthly_growth_year1
    if index < 24:
        return REVENUE_ASSUMPTIONS.new_users_monthly_growth_year2
    return REVENUE_ASSUMPTIONS.new_users_monthly_growth_year3


def _cohort_new_user_multiplier(index: int) -> float:
    year1 = REVENUE_ASSUMPTIONS.new_users_monthly_growth_year1
    year2 = REVENUE_ASSUMPTIONS.new_users_monthly_growth_year2
    year3 = REVENUE_ASSUMPTIONS.new_users_monthly_growth_year3
    if index < 12:
        return math.pow(1 + year1, index)
    if index < 24:
        return math.pow(1 + year1, 11) * math.pow(1 + year2, index - 11)
    return math.pow(1 + year1, 11) * math.pow(1 + year2, 12) * math.pow(1 + year3, index - 23)


def _cohort_retained_share(age: int) -> float:
    if age <= 0:
        return 1.0
    if age == 1:
        return REVENUE_ASSUMPTIONS.user_retention_month_1
    if age == 2:
        return REVENUE_ASSUMPTIONS.user_retention_month_2
    if age == 3:
        return REVENUE_ASSUMPTIONS.user_retention_month_3
    return REVENUE_ASSUMPTIONS.user_retention_month_3 * math.pow(
        REVENUE_ASSUMPTIONS.user_retention_decay,
        age - 3,
    )


def _build_user_cohort_rows(
    escrow_rows: list[dict[str, Any]],
    monthly_factors: dict[int, float],
    jitter_std: float,
    seed: int,
) -> list[dict[str, Any]]:
    rng = random.Random(seed + 101)
    rows: list[dict[str, Any]] = []
    for index, escrow_row in enumerate(escrow_rows):
        month_text = str(escrow_row["month"])
        month_key = date.fromisoformat(month_text)
        acquisition_growth_rate = _cohort_growth_rate_for_index(index)
        base_new_users = REVENUE_ASSUMPTIONS.new_users_start * _cohort_new_user_multiplier(index)
        seasonality = monthly_factors[month_key.month]
        if month_key.month in (11, 12):
            seasonality *= REVENUE_ASSUMPTIONS.new_user_holiday_spike_multiplier
        noise_acquisition = max(0.85, 1 + rng.gauss(0.0, jitter_std * 0.35))
        new_users = max(150.0, base_new_users * seasonality * noise_acquisition)
        rows.append(
            {
                "month": month_text,
                "year_index": escrow_row["year_index"],
                "phase": escrow_row["phase"],
                "acquisition_growth_rate": round(acquisition_growth_rate, 4),
                "base_new_users": round(base_new_users, 2),
                "seasonality_factor": round(seasonality, 6),
                "noise_acquisition": round(noise_acquisition, 6),
                "new_users": int(round(new_users)),
            }
        )
    return rows


def _build_user_cohort_matrix(cohort_rows: list[dict[str, Any]]) -> list[list[int]]:
    matrix: list[list[int]] = []
    for start_index, row in enumerate(cohort_rows):
        new_users = float(row["new_users"])
        contribution_row: list[int] = []
        for month_index in range(len(cohort_rows)):
            if month_index < start_index:
                contribution_row.append(0)
                continue
            retained_share = _cohort_retained_share(month_index - start_index)
            contribution_row.append(int(round(new_users * retained_share)))
        matrix.append(contribution_row)
    return matrix


def _build_mau_summary_rows(
    cohort_rows: list[dict[str, Any]],
    cohort_matrix: list[list[int]],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    progression_denominator = max(1, PROJECTION_MONTHS - 1)

    for index, cohort_row in enumerate(cohort_rows):
        new_users = int(cohort_row["new_users"])
        mau = int(sum(matrix_row[index] for matrix_row in cohort_matrix))
        returning_users = max(0, mau - new_users)
        progression = index / progression_denominator
        avg_end_user_mau_per_org = (
            REVENUE_ASSUMPTIONS.avg_end_user_mau_per_org_start
            + (
                REVENUE_ASSUMPTIONS.avg_end_user_mau_per_org_end
                - REVENUE_ASSUMPTIONS.avg_end_user_mau_per_org_start
            )
            * progression
        )
        developer_org_count = max(1, int(round(mau / max(1.0, avg_end_user_mau_per_org))))
        paying_developer_org_count = max(
            1,
            int(round(developer_org_count * REVENUE_ASSUMPTIONS.developer_org_paying_ratio)),
        )
        avg_end_user_mau_per_paying_org = mau / max(1, paying_developer_org_count)
        rows.append(
            {
                "month": cohort_row["month"],
                "year_index": cohort_row["year_index"],
                "phase": cohort_row["phase"],
                "new_users": new_users,
                "returning_users": returning_users,
                "mau": mau,
                "acquisition_growth_rate": float(cohort_row["acquisition_growth_rate"]),
                "base_new_users": float(cohort_row["base_new_users"]),
                "seasonality_factor": float(cohort_row["seasonality_factor"]),
                "noise_acquisition": float(cohort_row["noise_acquisition"]),
                "developer_org_count": developer_org_count,
                "paying_developer_org_count": paying_developer_org_count,
                "avg_end_user_mau_per_org": round(avg_end_user_mau_per_org, 2),
                "avg_end_user_mau_per_paying_org": round(avg_end_user_mau_per_paying_org, 2),
            }
        )
    return rows


def _metered_mau_fee_for_org(end_user_mau: float) -> tuple[str, float, int, float]:
    mau = max(0, int(round(end_user_mau)))
    free_cap = REVENUE_ASSUMPTIONS.metered_free_tier_mau_cap_per_org
    starter_cap = REVENUE_ASSUMPTIONS.metered_starter_tier_mau_cap_per_org
    growth_cap = REVENUE_ASSUMPTIONS.metered_growth_tier_mau_cap_per_org
    scale_cap = REVENUE_ASSUMPTIONS.metered_scale_tier_mau_cap_per_org
    starter_price = REVENUE_ASSUMPTIONS.metered_starter_tier_monthly_price_per_org_usd
    growth_price = REVENUE_ASSUMPTIONS.metered_growth_tier_monthly_price_per_org_usd
    scale_overage_price = REVENUE_ASSUMPTIONS.metered_scale_overage_price_per_mau_usd
    enterprise_overage_price = REVENUE_ASSUMPTIONS.metered_enterprise_overage_price_per_mau_usd
    if mau <= free_cap:
        return "free", 0.0, 0, 0.0
    if mau <= starter_cap:
        return "starter", starter_price, 0, 0.0
    if mau <= growth_cap:
        return "growth", growth_price, 0, 0.0
    if mau <= scale_cap:
        overage_mau = mau - growth_cap
        overage_revenue = overage_mau * scale_overage_price
        return "scale", growth_price + overage_revenue, overage_mau, scale_overage_price
    scale_base_revenue = growth_price + (scale_cap - growth_cap) * scale_overage_price
    enterprise_overage_mau = mau - scale_cap
    enterprise_overage_revenue = enterprise_overage_mau * enterprise_overage_price
    return (
        "enterprise",
        scale_base_revenue + enterprise_overage_revenue,
        enterprise_overage_mau,
        enterprise_overage_price,
    )


def _build_saas_rows(
    mau_rows: list[dict[str, Any]],
    escrow_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for index, row in enumerate(mau_rows):
        mau = int(row["mau"])
        developer_org_count = int(row["developer_org_count"])
        paying_developer_org_count = int(row["paying_developer_org_count"])
        avg_end_user_mau_per_paying_org = float(row["avg_end_user_mau_per_paying_org"])
        escrow_transaction_count = int(escrow_rows[index]["escrow_transaction_count"])
        (
            plan_tier,
            metered_mau_fee_per_paying_org_usd,
            metered_mau_overage_per_paying_org,
            metered_mau_overage_price_per_unit_usd,
        ) = _metered_mau_fee_for_org(avg_end_user_mau_per_paying_org)
        developer_subscription_revenue_usd = (
            paying_developer_org_count
            * REVENUE_ASSUMPTIONS.developer_subscription_monthly_price_usd
        )
        metered_mau_revenue_usd = (
            paying_developer_org_count * metered_mau_fee_per_paying_org_usd
        )
        included_escrow_txns = (
            paying_developer_org_count
            * REVENUE_ASSUMPTIONS.metered_included_escrow_txns_per_paying_org
        )
        billable_escrow_txns = max(0, escrow_transaction_count - included_escrow_txns)
        metered_escrow_txn_revenue_usd = (
            billable_escrow_txns
            * REVENUE_ASSUMPTIONS.metered_price_per_additional_escrow_txn_usd
        )
        saas_revenue_usd = (
            developer_subscription_revenue_usd
            + metered_mau_revenue_usd
            + metered_escrow_txn_revenue_usd
        )
        effective_arpu_usd = saas_revenue_usd / max(1, mau)
        rows.append(
            {
                "month": row["month"],
                "year_index": row["year_index"],
                "phase": row["phase"],
                "mau": mau,
                "developer_org_count": developer_org_count,
                "paying_developer_org_count": paying_developer_org_count,
                "avg_end_user_mau_per_paying_org": round(avg_end_user_mau_per_paying_org, 2),
                "plan_tier": plan_tier,
                "developer_subscription_price_usd": round(
                    REVENUE_ASSUMPTIONS.developer_subscription_monthly_price_usd, 2
                ),
                "developer_subscription_revenue_usd": round(
                    developer_subscription_revenue_usd, 2
                ),
                "metered_mau_fee_per_paying_org_usd": round(
                    metered_mau_fee_per_paying_org_usd, 2
                ),
                "metered_mau_overage_per_paying_org": metered_mau_overage_per_paying_org,
                "metered_mau_overage_price_per_unit_usd": round(
                    metered_mau_overage_price_per_unit_usd, 4
                ),
                "metered_mau_revenue_usd": round(metered_mau_revenue_usd, 2),
                "escrow_transaction_count": escrow_transaction_count,
                "included_escrow_txns": included_escrow_txns,
                "billable_escrow_txns": billable_escrow_txns,
                "metered_price_per_additional_escrow_txn_usd": round(
                    REVENUE_ASSUMPTIONS.metered_price_per_additional_escrow_txn_usd, 2
                ),
                "metered_escrow_txn_revenue_usd": round(
                    metered_escrow_txn_revenue_usd, 2
                ),
                "saas_revenue_usd": round(saas_revenue_usd, 2),
                "effective_arpu_usd": round(effective_arpu_usd, 4),
            }
        )
    return rows


def _build_escrow_logistics_rows(
    escrow_rows: list[dict[str, Any]],
    mau_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    launch_month_offset = max(0, REVENUE_ASSUMPTIONS.escrow_logistics_launch_month_offset)

    for index, escrow_row in enumerate(escrow_rows):
        escrow_transaction_count = int(escrow_row["escrow_transaction_count"])
        escrow_volume_usd = float(escrow_row["escrow_volume_usd"])
        paying_developer_org_count = int(mau_rows[index]["paying_developer_org_count"])

        if REVENUE_ASSUMPTIONS.escrow_logistics_enabled:
            txn_adoption_rate = _adoption_rate_for_index(
                index=index,
                launch_month_offset=launch_month_offset,
                start_rate=REVENUE_ASSUMPTIONS.escrow_logistics_txn_adoption_rate_start,
                end_rate=REVENUE_ASSUMPTIONS.escrow_logistics_txn_adoption_rate_end,
            )
            org_adoption_rate = _adoption_rate_for_index(
                index=index,
                launch_month_offset=launch_month_offset,
                start_rate=REVENUE_ASSUMPTIONS.escrow_logistics_org_adoption_rate_start,
                end_rate=REVENUE_ASSUMPTIONS.escrow_logistics_org_adoption_rate_end,
            )
        else:
            txn_adoption_rate = 0.0
            org_adoption_rate = 0.0

        logistics_escrow_txn_count = int(round(escrow_transaction_count * txn_adoption_rate))
        logistics_escrow_volume_usd = escrow_volume_usd * txn_adoption_rate
        active_logistics_org_count = int(round(paying_developer_org_count * org_adoption_rate))
        oracle_event_count = (
            logistics_escrow_txn_count * REVENUE_ASSUMPTIONS.escrow_logistics_oracle_events_per_txn
        )

        escrow_fee_uplift_revenue_usd = (
            logistics_escrow_volume_usd * REVENUE_ASSUMPTIONS.escrow_logistics_fee_uplift_rate
        )
        oracle_event_revenue_usd = (
            oracle_event_count * REVENUE_ASSUMPTIONS.escrow_logistics_oracle_fee_per_event_usd
        )
        platform_subscription_revenue_usd = (
            active_logistics_org_count * REVENUE_ASSUMPTIONS.escrow_logistics_platform_fee_monthly_usd
        )
        total_logistics_revenue_usd = (
            escrow_fee_uplift_revenue_usd
            + oracle_event_revenue_usd
            + platform_subscription_revenue_usd
        )

        carrier_data_cost_usd = (
            oracle_event_count
            * REVENUE_ASSUMPTIONS.escrow_logistics_carrier_data_cost_per_event_usd
        )
        attestation_compute_cost_usd = (
            oracle_event_count
            * REVENUE_ASSUMPTIONS.escrow_logistics_attestation_cost_per_event_usd
        )
        dispute_case_count = logistics_escrow_txn_count * REVENUE_ASSUMPTIONS.escrow_logistics_dispute_rate
        dispute_ops_cost_usd = (
            dispute_case_count * REVENUE_ASSUMPTIONS.escrow_logistics_dispute_cost_per_case_usd
        )
        support_cost_usd = (
            active_logistics_org_count
            * REVENUE_ASSUMPTIONS.escrow_logistics_support_cost_per_active_org_usd
        )
        total_logistics_cost_usd = (
            carrier_data_cost_usd
            + attestation_compute_cost_usd
            + dispute_ops_cost_usd
            + support_cost_usd
        )
        logistics_contribution_usd = total_logistics_revenue_usd - total_logistics_cost_usd
        logistics_gross_margin_pct = (
            logistics_contribution_usd / total_logistics_revenue_usd
            if total_logistics_revenue_usd > 0
            else 0.0
        )
        logistics_take_rate_pct = (
            total_logistics_revenue_usd / logistics_escrow_volume_usd
            if logistics_escrow_volume_usd > 0
            else 0.0
        )

        rows.append(
            {
                "month": escrow_row["month"],
                "year_index": escrow_row["year_index"],
                "phase": escrow_row["phase"],
                "escrow_transaction_count": escrow_transaction_count,
                "escrow_volume_usd": round(escrow_volume_usd, 2),
                "paying_developer_org_count": paying_developer_org_count,
                "txn_adoption_rate": round(txn_adoption_rate, 4),
                "org_adoption_rate": round(org_adoption_rate, 4),
                "logistics_escrow_txn_count": logistics_escrow_txn_count,
                "logistics_escrow_volume_usd": round(logistics_escrow_volume_usd, 2),
                "active_logistics_org_count": active_logistics_org_count,
                "oracle_events_per_txn": round(
                    REVENUE_ASSUMPTIONS.escrow_logistics_oracle_events_per_txn, 2
                ),
                "oracle_event_count": round(oracle_event_count, 2),
                "escrow_fee_uplift_rate": round(
                    REVENUE_ASSUMPTIONS.escrow_logistics_fee_uplift_rate, 4
                ),
                "escrow_fee_uplift_revenue_usd": round(escrow_fee_uplift_revenue_usd, 2),
                "oracle_fee_per_event_usd": round(
                    REVENUE_ASSUMPTIONS.escrow_logistics_oracle_fee_per_event_usd, 4
                ),
                "oracle_event_revenue_usd": round(oracle_event_revenue_usd, 2),
                "platform_fee_monthly_usd": round(
                    REVENUE_ASSUMPTIONS.escrow_logistics_platform_fee_monthly_usd, 2
                ),
                "platform_subscription_revenue_usd": round(
                    platform_subscription_revenue_usd, 2
                ),
                "total_logistics_revenue_usd": round(total_logistics_revenue_usd, 2),
                "carrier_data_cost_per_event_usd": round(
                    REVENUE_ASSUMPTIONS.escrow_logistics_carrier_data_cost_per_event_usd, 4
                ),
                "carrier_data_cost_usd": round(carrier_data_cost_usd, 2),
                "attestation_cost_per_event_usd": round(
                    REVENUE_ASSUMPTIONS.escrow_logistics_attestation_cost_per_event_usd, 4
                ),
                "attestation_compute_cost_usd": round(attestation_compute_cost_usd, 2),
                "dispute_rate": round(REVENUE_ASSUMPTIONS.escrow_logistics_dispute_rate, 4),
                "dispute_case_count": round(dispute_case_count, 2),
                "dispute_cost_per_case_usd": round(
                    REVENUE_ASSUMPTIONS.escrow_logistics_dispute_cost_per_case_usd, 2
                ),
                "dispute_ops_cost_usd": round(dispute_ops_cost_usd, 2),
                "support_cost_per_active_org_usd": round(
                    REVENUE_ASSUMPTIONS.escrow_logistics_support_cost_per_active_org_usd, 2
                ),
                "support_cost_usd": round(support_cost_usd, 2),
                "total_logistics_cost_usd": round(total_logistics_cost_usd, 2),
                "logistics_contribution_usd": round(logistics_contribution_usd, 2),
                "logistics_gross_margin_pct": round(logistics_gross_margin_pct, 4),
                "logistics_take_rate_pct": round(logistics_take_rate_pct, 4),
            }
        )
    return rows


def _build_expense_rows(
    mau_rows: list[dict[str, Any]],
    escrow_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for index, mau_row in enumerate(mau_rows):
        year_index = int(mau_row["year_index"])
        mau = float(mau_row["mau"])
        new_users = float(mau_row["new_users"])
        escrow_txn_count = float(escrow_rows[index]["escrow_transaction_count"])
        technology_opex = (
            REVENUE_ASSUMPTIONS.infrastructure_base_monthly_usd
            + mau * REVENUE_ASSUMPTIONS.infrastructure_cost_per_mau_usd
            + new_users * REVENUE_ASSUMPTIONS.infrastructure_cost_per_new_user_usd
            + escrow_txn_count * REVENUE_ASSUMPTIONS.infrastructure_cost_per_escrow_txn_usd
        )
        if year_index == 1:
            sales_marketing_opex = (
                REVENUE_ASSUMPTIONS.instagram_marketing_monthly_year1
                + REVENUE_ASSUMPTIONS.twitter_marketing_monthly_year1
                + REVENUE_ASSUMPTIONS.facebook_marketing_monthly_year1
                + REVENUE_ASSUMPTIONS.content_creation_monthly_year1
            )
            team_size = REVENUE_ASSUMPTIONS.team_size_year1
        elif year_index == 2:
            sales_marketing_opex = (
                REVENUE_ASSUMPTIONS.instagram_marketing_monthly_year2
                + REVENUE_ASSUMPTIONS.twitter_marketing_monthly_year2
                + REVENUE_ASSUMPTIONS.facebook_marketing_monthly_year2
                + REVENUE_ASSUMPTIONS.content_creation_monthly_year2
            )
            team_size = REVENUE_ASSUMPTIONS.team_size_year2
        else:
            sales_marketing_opex = (
                REVENUE_ASSUMPTIONS.instagram_marketing_monthly_year3
                + REVENUE_ASSUMPTIONS.twitter_marketing_monthly_year3
                + REVENUE_ASSUMPTIONS.facebook_marketing_monthly_year3
                + REVENUE_ASSUMPTIONS.content_creation_monthly_year3
            )
            team_size = REVENUE_ASSUMPTIONS.team_size_year3
        general_and_administrative_opex = (
            team_size * REVENUE_ASSUMPTIONS.software_tools_per_team_member_monthly_usd
        )
        if index == 0:
            general_and_administrative_opex += REVENUE_ASSUMPTIONS.incorporation_setup_usd
        total_opex = (
            technology_opex + sales_marketing_opex + general_and_administrative_opex
        )
        rows.append(
            {
                "month": mau_row["month"],
                "year_index": year_index,
                "phase": mau_row["phase"],
                "technology_and_infrastructure_opex_usd": round(technology_opex, 2),
                "sales_and_marketing_opex_usd": round(sales_marketing_opex, 2),
                "general_and_administrative_opex_usd": round(general_and_administrative_opex, 2),
                "total_operating_expenses_usd": round(total_opex, 2),
            }
        )
    return rows


def main(argv: Sequence[str] | None = None) -> int:
    _ = argv
    projection_start = date.fromisoformat(f"{REVENUE_ASSUMPTIONS.projection_start_month}-01")
    workbook_output = DATA_DIR / DATA_PATHS.projection_workbook_xlsx
    monthly_factors = _seasonality_factors()

    escrow_rows = _build_escrow_rows(
        projection_start=projection_start,
        monthly_factors=monthly_factors,
        jitter_std=REVENUE_ASSUMPTIONS.jitter_std,
        seed=REVENUE_ASSUMPTIONS.seed,
    )
    user_cohort_rows = _build_user_cohort_rows(
        escrow_rows=escrow_rows,
        monthly_factors=monthly_factors,
        jitter_std=REVENUE_ASSUMPTIONS.jitter_std,
        seed=REVENUE_ASSUMPTIONS.seed,
    )
    user_cohort_matrix = _build_user_cohort_matrix(user_cohort_rows)
    mau_rows = _build_mau_summary_rows(
        cohort_rows=user_cohort_rows,
        cohort_matrix=user_cohort_matrix,
    )
    saas_rows = _build_saas_rows(mau_rows, escrow_rows)
    escrow_logistics_rows = _build_escrow_logistics_rows(escrow_rows, mau_rows)
    expense_rows = _build_expense_rows(mau_rows, escrow_rows)

    write_projection_workbook(
        workbook_output,
        assumptions=REVENUE_ASSUMPTIONS,
        escrow_rows=escrow_rows,
        mau_rows=mau_rows,
        saas_rows=saas_rows,
        escrow_logistics_rows=escrow_logistics_rows,
        expense_rows=expense_rows,
    )

    print(f"projection_start_month={projection_start.isoformat()}")
    print(f"escrow_rows={len(escrow_rows)}")
    print(f"user_cohort_rows={len(user_cohort_rows)}")
    print(f"saas_rows={len(saas_rows)}")
    print(f"escrow_logistics_rows={len(escrow_logistics_rows)}")
    print(f"expense_rows={len(expense_rows)}")
    print(f"workbook_output={workbook_output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
