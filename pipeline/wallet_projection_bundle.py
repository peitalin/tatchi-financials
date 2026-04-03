from __future__ import annotations

from pathlib import Path
from textwrap import dedent
from typing import Sequence

try:
    from .assumptions import REVENUE_ASSUMPTIONS
    from .runtime_config import DATA_PATHS
    from .wallet_projection_revenues import main as generate_wallet_projection
except ImportError:
    from assumptions import REVENUE_ASSUMPTIONS
    from runtime_config import DATA_PATHS
    from wallet_projection_revenues import main as generate_wallet_projection

SCRIPT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = SCRIPT_DIR / "data"


def _write_assumptions_summary() -> None:
    assumptions_output = DATA_DIR / DATA_PATHS.data_generation_assumptions_md
    assumption_text = dedent(
        f"""
        # Wallet-as-a-Service Financial Model Assumptions (36-Month Synthetic Model)

        This document captures the assumptions used to generate:
        - `{DATA_PATHS.projection_workbook_xlsx}`

        Workbook sheets:
        - `Summary`
        - `Escrow Revenue`
        - `Escrow + Logistics`
        - `MAU & Operating Metrics`
        - `SaaS Pricing`
        - `OpEx`

        ## Source of Truth

        The canonical source of truth for data-generating assumptions is:
        - `pipeline/assumptions.py`

        ## Revenue Specs

        Monthly total revenue is modeled as:

        `Total Revenue (Base Wallet) = Escrow Fee Revenue + SaaS Revenue`
        `Total Revenue (With Logistics) = Total Revenue (Base Wallet) + Escrow + Logistics Revenue`

        Escrow assumptions:
        - settlement stablecoin: `{REVENUE_ASSUMPTIONS.escrow_settlement_stablecoin}`
        - baseline monthly escrow volume: `${REVENUE_ASSUMPTIONS.baseline_monthly_escrow_volume_usd:,.2f}`
        - baseline monthly escrow transactions: `{REVENUE_ASSUMPTIONS.baseline_monthly_escrow_transactions:,}`
        - annual escrow volume growth: `{REVENUE_ASSUMPTIONS.escrow_volume_annual_growth:.2%}`
        - annual escrow transaction growth: `{REVENUE_ASSUMPTIONS.escrow_transactions_annual_growth:.2%}`
        - escrow fee rate: `{REVENUE_ASSUMPTIONS.escrow_fee_rate:.2%}`

        SaaS revenue assumptions:
        - paying developer subscription price: `${REVENUE_ASSUMPTIONS.developer_subscription_monthly_price_usd:,.2f}` per paying org
        - developer org paying ratio: `{REVENUE_ASSUMPTIONS.developer_org_paying_ratio:.2%}`
        - average end-user MAU per org ramps from `{REVENUE_ASSUMPTIONS.avg_end_user_mau_per_org_start:.0f}` to `{REVENUE_ASSUMPTIONS.avg_end_user_mau_per_org_end:.0f}`
        - per-paying-org metered MAU pricing tiers:
          - free: `0` to `{REVENUE_ASSUMPTIONS.metered_free_tier_mau_cap_per_org}` MAU => `${0:,.2f}/mo`
          - starter: `{REVENUE_ASSUMPTIONS.metered_free_tier_mau_cap_per_org + 1}` to `{REVENUE_ASSUMPTIONS.metered_starter_tier_mau_cap_per_org}` MAU => `${REVENUE_ASSUMPTIONS.metered_starter_tier_monthly_price_per_org_usd:,.2f}/mo`
          - growth: `{REVENUE_ASSUMPTIONS.metered_starter_tier_mau_cap_per_org + 1}` to `{REVENUE_ASSUMPTIONS.metered_growth_tier_mau_cap_per_org}` MAU => `${REVENUE_ASSUMPTIONS.metered_growth_tier_monthly_price_per_org_usd:,.2f}/mo`
          - scale overage: `{REVENUE_ASSUMPTIONS.metered_growth_tier_mau_cap_per_org + 1}` to `{REVENUE_ASSUMPTIONS.metered_scale_tier_mau_cap_per_org}` MAU => `${REVENUE_ASSUMPTIONS.metered_scale_overage_price_per_mau_usd:.3f}` per MAU above `{REVENUE_ASSUMPTIONS.metered_growth_tier_mau_cap_per_org}`
          - enterprise overage: above `{REVENUE_ASSUMPTIONS.metered_scale_tier_mau_cap_per_org}` MAU => `${REVENUE_ASSUMPTIONS.metered_enterprise_overage_price_per_mau_usd:.3f}` per MAU
        - metered escrow activity:
          - included escrow transactions per paying org: `{REVENUE_ASSUMPTIONS.metered_included_escrow_txns_per_paying_org}`
          - additional escrow transaction fee: `${REVENUE_ASSUMPTIONS.metered_price_per_additional_escrow_txn_usd:.2f}`

        Escrow + logistics managed-service assumptions:
        - scenario enabled: `{REVENUE_ASSUMPTIONS.escrow_logistics_enabled}`
        - launch month offset (0-based): `{REVENUE_ASSUMPTIONS.escrow_logistics_launch_month_offset}`
        - txn adoption rate ramp: `{REVENUE_ASSUMPTIONS.escrow_logistics_txn_adoption_rate_start:.2%}` -> `{REVENUE_ASSUMPTIONS.escrow_logistics_txn_adoption_rate_end:.2%}`
        - org adoption rate ramp: `{REVENUE_ASSUMPTIONS.escrow_logistics_org_adoption_rate_start:.2%}` -> `{REVENUE_ASSUMPTIONS.escrow_logistics_org_adoption_rate_end:.2%}`
        - escrow fee uplift rate on logistics-enabled volume: `{REVENUE_ASSUMPTIONS.escrow_logistics_fee_uplift_rate:.2%}`
        - oracle events per logistics escrow txn: `{REVENUE_ASSUMPTIONS.escrow_logistics_oracle_events_per_txn:.2f}`
        - revenue per oracle event: `${REVENUE_ASSUMPTIONS.escrow_logistics_oracle_fee_per_event_usd:.4f}`
        - monthly platform fee per active logistics org: `${REVENUE_ASSUMPTIONS.escrow_logistics_platform_fee_monthly_usd:.2f}`
        - direct cost per oracle event:
          - carrier data: `${REVENUE_ASSUMPTIONS.escrow_logistics_carrier_data_cost_per_event_usd:.4f}`
          - attestation compute: `${REVENUE_ASSUMPTIONS.escrow_logistics_attestation_cost_per_event_usd:.4f}`
        - dispute ops:
          - dispute rate: `{REVENUE_ASSUMPTIONS.escrow_logistics_dispute_rate:.2%}`
          - cost per dispute case: `${REVENUE_ASSUMPTIONS.escrow_logistics_dispute_cost_per_case_usd:.2f}`
        - support cost per active logistics org: `${REVENUE_ASSUMPTIONS.escrow_logistics_support_cost_per_active_org_usd:.2f}`

        ## Audience Specs

        MAU is generated from monthly cohorts with:
        - initial cohort: `{REVENUE_ASSUMPTIONS.new_users_start:,.0f}` new users
        - month-over-month growth: `{REVENUE_ASSUMPTIONS.new_users_monthly_growth_year1:.2%}` (Y1), `{REVENUE_ASSUMPTIONS.new_users_monthly_growth_year2:.2%}` (Y2), `{REVENUE_ASSUMPTIONS.new_users_monthly_growth_year3:.2%}` (Y3)
        - holiday spike (Nov/Dec): `{REVENUE_ASSUMPTIONS.new_user_holiday_spike_multiplier:.2f}x`
        - retention curve: M1 `{REVENUE_ASSUMPTIONS.user_retention_month_1:.2%}`, M2 `{REVENUE_ASSUMPTIONS.user_retention_month_2:.2%}`, M3 `{REVENUE_ASSUMPTIONS.user_retention_month_3:.2%}`, then `{REVENUE_ASSUMPTIONS.user_retention_decay:.2%}` monthly decay factor

        ## Operating Expense Specs

        Technology and infrastructure OpEx:
        - base monthly cost: `${REVENUE_ASSUMPTIONS.infrastructure_base_monthly_usd:,.2f}`
        - variable cost per MAU: `${REVENUE_ASSUMPTIONS.infrastructure_cost_per_mau_usd:.2f}`
        - variable cost per new user: `${REVENUE_ASSUMPTIONS.infrastructure_cost_per_new_user_usd:.2f}`
        - variable cost per escrow transaction: `${REVENUE_ASSUMPTIONS.infrastructure_cost_per_escrow_txn_usd:.2f}`

        Sales and marketing OpEx is modeled as fixed monthly channel budgets by year.

        G&A OpEx:
        - software tools per team member: `${REVENUE_ASSUMPTIONS.software_tools_per_team_member_monthly_usd:.2f}`
        - team size: `{REVENUE_ASSUMPTIONS.team_size_year1}` (Y1), `{REVENUE_ASSUMPTIONS.team_size_year2}` (Y2), `{REVENUE_ASSUMPTIONS.team_size_year3}` (Y3)
        - one-time incorporation setup: `${REVENUE_ASSUMPTIONS.incorporation_setup_usd:.2f}` in month 1

        ## Reproducibility

        - projection months: `{REVENUE_ASSUMPTIONS.projection_months}`
        - start month: `{REVENUE_ASSUMPTIONS.projection_start_month}`
        - noise standard deviation: `{REVENUE_ASSUMPTIONS.jitter_std:.4f}`
        - random seed: `{REVENUE_ASSUMPTIONS.seed}`
        """
    ).strip()
    assumptions_output.parent.mkdir(parents=True, exist_ok=True)
    assumptions_output.write_text(f"{assumption_text}\n", encoding="utf-8")


def main(argv: Sequence[str] | None = None) -> int:
    _ = argv
    revenue_exit = generate_wallet_projection(None)
    if revenue_exit != 0:
        return int(revenue_exit)

    _write_assumptions_summary()

    print(f"workbook_output={DATA_DIR / DATA_PATHS.projection_workbook_xlsx}")
    print(f"assumptions_output={DATA_DIR / DATA_PATHS.data_generation_assumptions_md}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
