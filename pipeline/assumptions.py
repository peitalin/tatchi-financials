from __future__ import annotations

from dataclasses import dataclass
from typing import Final


@dataclass(frozen=True)
class RevenueProjectionAssumptions:
    # Number of monthly rows to generate for synthetic projections.
    projection_months: int = 36
    # Calendar month to start synthetic output (YYYY-MM).
    projection_start_month: str = "2026-03"
    # Standard deviation for monthly random noise in synthetic generation.
    jitter_std: float = 0.04
    # Random seed for deterministic synthetic output.
    seed: int = 42

    # Escrow (stablecoin wallet-as-a-service) revenue model.
    baseline_monthly_escrow_volume_usd: float = 800_000.0
    baseline_monthly_escrow_transactions: int = 260
    escrow_volume_annual_growth: float = 0.35
    escrow_transactions_annual_growth: float = 0.22
    escrow_fee_rate: float = 0.009
    escrow_settlement_stablecoin: str = "USDC"

    # Escrow + logistics managed-service model.
    escrow_logistics_enabled: bool = True
    escrow_logistics_launch_month_offset: int = 9
    escrow_logistics_txn_adoption_rate_start: float = 0.05
    escrow_logistics_txn_adoption_rate_end: float = 0.42
    escrow_logistics_org_adoption_rate_start: float = 0.08
    escrow_logistics_org_adoption_rate_end: float = 0.48
    escrow_logistics_fee_uplift_rate: float = 0.0035
    escrow_logistics_oracle_events_per_txn: float = 4.0
    escrow_logistics_oracle_fee_per_event_usd: float = 0.06
    escrow_logistics_platform_fee_monthly_usd: float = 349.0
    escrow_logistics_carrier_data_cost_per_event_usd: float = 0.02
    escrow_logistics_attestation_cost_per_event_usd: float = 0.01
    escrow_logistics_dispute_rate: float = 0.03
    escrow_logistics_dispute_cost_per_case_usd: float = 9.0
    escrow_logistics_support_cost_per_active_org_usd: float = 14.0

    # Monthly seasonality factors for Jan..Dec.
    monthly_seasonality_factors: tuple[float, ...] = (
        0.94,
        0.96,
        1.00,
        1.03,
        1.05,
        1.07,
        1.08,
        1.06,
        1.02,
        1.00,
        1.01,
        1.04,
    )

    # Developer organization economics.
    avg_end_user_mau_per_org_start: float = 180.0
    avg_end_user_mau_per_org_end: float = 520.0
    developer_org_paying_ratio: float = 0.70
    developer_subscription_monthly_price_usd: float = 79.0

    # Metered MAU pricing (applied per paying developer organization).
    metered_free_tier_mau_cap_per_org: int = 200
    metered_starter_tier_mau_cap_per_org: int = 1_000
    metered_starter_tier_monthly_price_per_org_usd: float = 50.0
    metered_growth_tier_mau_cap_per_org: int = 5_000
    metered_growth_tier_monthly_price_per_org_usd: float = 175.0
    metered_scale_tier_mau_cap_per_org: int = 10_000
    metered_scale_overage_price_per_mau_usd: float = 0.03
    metered_enterprise_overage_price_per_mau_usd: float = 0.025

    # Metered activity pricing.
    metered_included_escrow_txns_per_paying_org: int = 150
    metered_price_per_additional_escrow_txn_usd: float = 0.20

    # Audience model (drives MAU, which then drives SaaS pricing).
    new_users_start: float = 1_100.0
    new_users_monthly_growth_year1: float = 0.09
    new_users_monthly_growth_year2: float = 0.05
    new_users_monthly_growth_year3: float = 0.03
    new_user_holiday_spike_multiplier: float = 1.20
    user_retention_month_1: float = 0.29
    user_retention_month_2: float = 0.16
    user_retention_month_3: float = 0.09
    user_retention_decay: float = 0.97
    # Simplified operating expense model.
    infrastructure_base_monthly_usd: float = 1_200.0
    infrastructure_cost_per_mau_usd: float = 0.04
    infrastructure_cost_per_new_user_usd: float = 0.70
    infrastructure_cost_per_escrow_txn_usd: float = 1.80
    instagram_marketing_monthly_year1: float = 1_500.0
    instagram_marketing_monthly_year2: float = 2_200.0
    instagram_marketing_monthly_year3: float = 2_900.0
    twitter_marketing_monthly_year1: float = 500.0
    twitter_marketing_monthly_year2: float = 750.0
    twitter_marketing_monthly_year3: float = 1_000.0
    facebook_marketing_monthly_year1: float = 1_000.0
    facebook_marketing_monthly_year2: float = 1_400.0
    facebook_marketing_monthly_year3: float = 1_900.0
    content_creation_monthly_year1: float = 800.0
    content_creation_monthly_year2: float = 1_200.0
    content_creation_monthly_year3: float = 1_600.0
    team_size_year1: int = 3
    team_size_year2: int = 4
    team_size_year3: int = 5
    software_tools_per_team_member_monthly_usd: float = 42.0
    incorporation_setup_usd: float = 500.0


REVENUE_ASSUMPTIONS: Final[RevenueProjectionAssumptions] = RevenueProjectionAssumptions()
PROJECTION_MONTHS: Final[int] = REVENUE_ASSUMPTIONS.projection_months
