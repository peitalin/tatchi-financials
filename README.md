# wallet-financials

Synthetic spreadsheet generation for a wallet-as-a-service financial model.

## Commands

Run from this folder:

```bash
python3 main.py revenues
python3 main.py bundle
python3 main.py plot
```

## Outputs

Workbook and assumptions snapshot:
- `data/synthetic_wallet_financial_projection_model.xlsx`
- `data/wallet_financial_model_assumptions.md`

Charts:
- `data/charts/wallet_revenue_projection.svg`
- `data/charts/wallet_mau_vs_revenue_projection.svg`
- `data/charts/wallet_escrow_transactions_projection.svg`
- `data/charts/wallet_audience_projection.svg`
- `data/charts/index.html`

Assumptions source of truth:
- `pipeline/assumptions.py`
