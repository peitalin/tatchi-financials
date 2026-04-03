from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Final


@dataclass(frozen=True)
class DataPathConfig:
    projection_workbook_xlsx: Path = Path("synthetic_wallet_financial_projection_model.xlsx")
    data_generation_assumptions_md: Path = Path("wallet_financial_model_assumptions.md")
    charts_dir: Path = Path("charts")
    revenue_chart_svg: str = "wallet_revenue_projection.svg"
    transactions_chart_svg: str = "wallet_escrow_transactions_projection.svg"
    audience_chart_svg: str = "wallet_audience_projection.svg"
    mau_vs_revenue_chart_svg: str = "wallet_mau_vs_revenue_projection.svg"
    charts_index_html: str = "index.html"


DATA_PATHS: Final[DataPathConfig] = DataPathConfig()
