# Wallet Finance Outputs

## synthetic_wallet_financial_projection_model.xlsx

Single workbook that contains the projection inputs and output sheets.

Sheets:
- `Summary`: 36-month income-statement style rollup.
- `Escrow Revenue`: stablecoin escrow volume, escrow transactions, and escrow fee revenue.
- `Escrow + Logistics`: managed-service logistics-oracle adoption, revenue, costs, and contribution.
- `MAU & Operating Metrics`: cohort-based audience model.
- `SaaS Pricing`: MAU-tier billing and projected SaaS revenue.
- `OpEx`: simplified operating expense model.

### Summary

Monthly line items:
- `Escrow Fee Revenue`
- `SaaS Revenue`
- `Total Revenue (Base Wallet)`
- `Escrow + Logistics Revenue`
- `Total Revenue (With Logistics)`
- `Total Operating Expenses`
- `Operating Profit / (Loss) Base`
- `Escrow + Logistics Direct Costs`
- `Escrow + Logistics Contribution`
- `Adjusted Operating Expenses (With Logistics)`
- `Operating Profit / (Loss) With Logistics`

### Escrow Revenue

- `month`
- `year_index`
- `phase`
- `escrow_transaction_count`
- `avg_escrow_size_usd`
- `escrow_volume_usd`
- `escrow_fee_rate`
- `escrow_fee_revenue_usd`
- `settlement_stablecoin`

### Escrow + Logistics

- `month`
- `year_index`
- `phase`
- `escrow_transaction_count`
- `escrow_volume_usd`
- `paying_developer_org_count`
- `txn_adoption_rate`
- `org_adoption_rate`
- `logistics_escrow_txn_count`
- `logistics_escrow_volume_usd`
- `active_logistics_org_count`
- `oracle_events_per_txn`
- `oracle_event_count`
- `escrow_fee_uplift_rate`
- `escrow_fee_uplift_revenue_usd`
- `oracle_fee_per_event_usd`
- `oracle_event_revenue_usd`
- `platform_fee_monthly_usd`
- `platform_subscription_revenue_usd`
- `total_logistics_revenue_usd`
- `carrier_data_cost_per_event_usd`
- `carrier_data_cost_usd`
- `attestation_cost_per_event_usd`
- `attestation_compute_cost_usd`
- `dispute_rate`
- `dispute_case_count`
- `dispute_cost_per_case_usd`
- `dispute_ops_cost_usd`
- `support_cost_per_active_org_usd`
- `support_cost_usd`
- `total_logistics_cost_usd`
- `logistics_contribution_usd`
- `logistics_gross_margin_pct`
- `logistics_take_rate_pct`

### MAU & Operating Metrics

- `month`
- `year_index`
- `phase`
- `new_users`
- `returning_users`
- `mau`
- `acquisition_growth_rate`
- `base_new_users`
- `seasonality_factor`
- `noise_acquisition`
- `developer_org_count`
- `paying_developer_org_count`
- `avg_end_user_mau_per_org`
- `avg_end_user_mau_per_paying_org`

### SaaS Pricing

- `month`
- `year_index`
- `phase`
- `mau`
- `developer_org_count`
- `paying_developer_org_count`
- `avg_end_user_mau_per_paying_org`
- `plan_tier`
- `developer_subscription_price_usd`
- `developer_subscription_revenue_usd`
- `metered_mau_fee_per_paying_org_usd`
- `metered_mau_overage_per_paying_org`
- `metered_mau_overage_price_per_unit_usd`
- `metered_mau_revenue_usd`
- `escrow_transaction_count`
- `included_escrow_txns`
- `billable_escrow_txns`
- `metered_price_per_additional_escrow_txn_usd`
- `metered_escrow_txn_revenue_usd`
- `saas_revenue_usd`
- `effective_arpu_usd`

### OpEx

- `month`
- `year_index`
- `phase`
- `technology_and_infrastructure_opex_usd`
- `sales_and_marketing_opex_usd`
- `general_and_administrative_opex_usd`
- `total_operating_expenses_usd`

## Charts

- `wallet_revenue_projection.svg`: total, escrow fee, and SaaS revenue lines over time.
- `wallet_mau_vs_revenue_projection.svg`: MAU-to-revenue relationship across monthly observations.
- `wallet_escrow_transactions_projection.svg`: escrow transactions over time.
- `wallet_audience_projection.svg`: MAU versus billable MAU over time.
