# Wallet-as-a-Service Financial Model Assumptions (36-Month Synthetic Model)

This document captures the assumptions used to generate:
- `synthetic_wallet_financial_projection_model.xlsx`

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
- settlement stablecoin: `USDC`
- baseline monthly escrow volume: `$800,000.00`
- baseline monthly escrow transactions: `260`
- annual escrow volume growth: `35.00%`
- annual escrow transaction growth: `22.00%`
- escrow fee rate: `0.90%`

SaaS revenue assumptions:
- paying developer subscription price: `$79.00` per paying org
- developer org paying ratio: `70.00%`
- average end-user MAU per org ramps from `180` to `520`
- per-paying-org metered MAU pricing tiers:
  - free: `0` to `200` MAU => `$0.00/mo`
  - starter: `201` to `1000` MAU => `$50.00/mo`
  - growth: `1001` to `5000` MAU => `$175.00/mo`
  - scale overage: `5001` to `10000` MAU => `$0.030` per MAU above `5000`
  - enterprise overage: above `10000` MAU => `$0.025` per MAU
- metered escrow activity:
  - included escrow transactions per paying org: `150`
  - additional escrow transaction fee: `$0.20`

Escrow + logistics managed-service assumptions:
- scenario enabled: `True`
- launch month offset (0-based): `9`
- txn adoption rate ramp: `5.00%` -> `42.00%`
- org adoption rate ramp: `8.00%` -> `48.00%`
- escrow fee uplift rate on logistics-enabled volume: `0.35%`
- oracle events per logistics escrow txn: `4.00`
- revenue per oracle event: `$0.0600`
- monthly platform fee per active logistics org: `$349.00`
- direct cost per oracle event:
  - carrier data: `$0.0200`
  - attestation compute: `$0.0100`
- dispute ops:
  - dispute rate: `3.00%`
  - cost per dispute case: `$9.00`
- support cost per active logistics org: `$14.00`

## Audience Specs

MAU is generated from monthly cohorts with:
- initial cohort: `1,100` new users
- month-over-month growth: `9.00%` (Y1), `5.00%` (Y2), `3.00%` (Y3)
- holiday spike (Nov/Dec): `1.20x`
- retention curve: M1 `29.00%`, M2 `16.00%`, M3 `9.00%`, then `97.00%` monthly decay factor

## Operating Expense Specs

Technology and infrastructure OpEx:
- base monthly cost: `$1,200.00`
- variable cost per MAU: `$0.04`
- variable cost per new user: `$0.70`
- variable cost per escrow transaction: `$1.80`

Sales and marketing OpEx is modeled as fixed monthly channel budgets by year.

G&A OpEx:
- software tools per team member: `$42.00`
- team size: `3` (Y1), `4` (Y2), `5` (Y3)
- one-time incorporation setup: `$500.00` in month 1

## Reproducibility

- projection months: `36`
- start month: `2026-03`
- noise standard deviation: `0.0400`
- random seed: `42`
