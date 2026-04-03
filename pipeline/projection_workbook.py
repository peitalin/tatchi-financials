from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any
from xml.etree import ElementTree as ET
from xml.sax.saxutils import escape
from zipfile import ZIP_DEFLATED
from zipfile import ZipFile

try:
    from .assumptions import RevenueProjectionAssumptions
except ImportError:
    from assumptions import RevenueProjectionAssumptions

NS_MAIN = "http://schemas.openxmlformats.org/spreadsheetml/2006/main"
NS_REL = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
NS_PACKAGE = "http://schemas.openxmlformats.org/package/2006/relationships"

STYLE_DEFAULT = 0
STYLE_SECTION_HEADER = 1
STYLE_COLUMN_HEADER = 2
STYLE_ROW_HEADER = 3

SHEET_SUMMARY = "Summary"
SHEET_ESCROW_REVENUE = "Escrow Revenue"
SHEET_ESCROW_LOGISTICS = "Escrow + Logistics"
SHEET_MAU = "MAU & Operating Metrics"
SHEET_SAAS_PRICING = "SaaS Pricing"
SHEET_EXPENSES = "OpEx"


def _col_name(index: int) -> str:
    value = index
    output = ""
    while value > 0:
        value, remainder = divmod(value - 1, 26)
        output = chr(65 + remainder) + output
    return output


def _cell_ref(col_index: int, row_index: int) -> str:
    return f"{_col_name(col_index)}{row_index}"


def _column_index(cell_ref: str) -> int:
    letters = "".join(char for char in cell_ref if char.isalpha())
    value = 0
    for char in letters:
        value = value * 26 + (ord(char.upper()) - 64)
    return value


def _xml_text(value: Any) -> str:
    return escape(str(value))


def _number_text(value: Any) -> str:
    if isinstance(value, bool):
        return "1" if value else "0"
    if isinstance(value, int):
        return str(value)
    if isinstance(value, float):
        if value.is_integer():
            return str(int(value))
        return f"{value:.15g}"
    return str(value)


@dataclass(frozen=True)
class Cell:
    kind: str
    value: str | float | int
    style_id: int = STYLE_DEFAULT

    @staticmethod
    def string(value: str, *, style_id: int = STYLE_DEFAULT) -> Cell:
        return Cell(kind="string", value=value, style_id=style_id)

    @staticmethod
    def number(value: float | int, *, style_id: int = STYLE_DEFAULT) -> Cell:
        return Cell(kind="number", value=value, style_id=style_id)


@dataclass(frozen=True)
class Sheet:
    name: str
    rows: list[list[Cell]]
    state: str = "visible"


def _cell_xml(cell_ref: str, cell: Cell) -> str:
    style_attr = f' s="{cell.style_id}"' if cell.style_id != STYLE_DEFAULT else ""
    if cell.kind == "string":
        return (
            f'<c r="{cell_ref}" t="inlineStr"{style_attr}>'
            f"<is><t>{_xml_text(cell.value)}</t></is>"
            "</c>"
        )
    if cell.kind == "number":
        return f'<c r="{cell_ref}"{style_attr}><v>{_number_text(cell.value)}</v></c>'
    raise ValueError(f"unsupported cell kind: {cell.kind}")


def _sheet_xml(sheet: Sheet) -> str:
    max_cols = max((len(row) for row in sheet.rows), default=1)
    max_rows = max(1, len(sheet.rows))
    dimension = f"A1:{_cell_ref(max_cols, max_rows)}"
    cols_xml = _sheet_columns_xml(sheet, max_cols)
    row_xml: list[str] = []
    for row_index, row in enumerate(sheet.rows, start=1):
        cells = "".join(
            _cell_xml(_cell_ref(col_index, row_index), cell)
            for col_index, cell in enumerate(row, start=1)
        )
        row_xml.append(f'<row r="{row_index}">{cells}</row>')
    return (
        f'<worksheet xmlns="{NS_MAIN}" xmlns:r="{NS_REL}">'
        f'<dimension ref="{dimension}"/>'
        '<sheetViews><sheetView workbookViewId="0"/></sheetViews>'
        "<sheetFormatPr defaultRowHeight=\"15\"/>"
        f"{cols_xml}"
        f"<sheetData>{''.join(row_xml)}</sheetData>"
        '<pageMargins left="0.7" right="0.7" top="0.75" bottom="0.75" header="0.3" footer="0.3"/>'
        "</worksheet>"
    )


def _workbook_xml(sheets: list[Sheet]) -> str:
    sheet_xml = "".join(
        (
            f'<sheet name="{_xml_text(sheet.name)}" sheetId="{index}" '
            f'state="{sheet.state}" r:id="rId{index}"/>'
        )
        for index, sheet in enumerate(sheets, start=1)
    )
    return (
        f'<workbook xmlns="{NS_MAIN}" xmlns:r="{NS_REL}">'
        "<bookViews><workbookView xWindow=\"0\" yWindow=\"0\" windowWidth=\"28800\" windowHeight=\"17280\"/></bookViews>"
        f"<sheets>{sheet_xml}</sheets>"
        '<calcPr calcId="181029" calcMode="auto" fullCalcOnLoad="1"/>'
        "</workbook>"
    )


def _content_types_xml(sheet_count: int) -> str:
    overrides = [
        '<Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>',
        '<Override PartName="/xl/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.styles+xml"/>',
        '<Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/>',
        '<Override PartName="/docProps/app.xml" ContentType="application/vnd.openxmlformats-officedocument.extended-properties+xml"/>',
    ]
    overrides.extend(
        f'<Override PartName="/xl/worksheets/sheet{index}.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>'
        for index in range(1, sheet_count + 1)
    )
    return (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
        '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
        '<Default Extension="xml" ContentType="application/xml"/>'
        f"{''.join(overrides)}"
        "</Types>"
    )


def _root_rels_xml() -> str:
    return (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        f'<Relationships xmlns="{NS_PACKAGE}">'
        '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/>'
        '<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="docProps/core.xml"/>'
        '<Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/extended-properties" Target="docProps/app.xml"/>'
        "</Relationships>"
    )


def _workbook_rels_xml(sheet_count: int) -> str:
    rels = "".join(
        f'<Relationship Id="rId{index}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet{index}.xml"/>'
        for index in range(1, sheet_count + 1)
    )
    rels += (
        f'<Relationship Id="rId{sheet_count + 1}" '
        'Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" '
        'Target="styles.xml"/>'
    )
    return (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        f'<Relationships xmlns="{NS_PACKAGE}">{rels}</Relationships>'
    )


def _core_xml() -> str:
    return (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" '
        'xmlns:dc="http://purl.org/dc/elements/1.1/" '
        'xmlns:dcterms="http://purl.org/dc/terms/" '
        'xmlns:dcmitype="http://purl.org/dc/dcmitype/" '
        'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">'
        "<dc:title>Synthetic Wallet Financial Projection Model</dc:title>"
        "<dc:creator>Codex</dc:creator>"
        "</cp:coreProperties>"
    )


def _app_xml(sheet_names: list[str]) -> str:
    heading_pairs = '<vt:vector size="2" baseType="variant"><vt:variant><vt:lpstr>Worksheets</vt:lpstr></vt:variant><vt:variant><vt:i4>{}</vt:i4></vt:variant></vt:vector>'.format(
        len(sheet_names)
    )
    titles = "".join(f"<vt:lpstr>{_xml_text(name)}</vt:lpstr>" for name in sheet_names)
    return (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties" '
        'xmlns:vt="http://schemas.openxmlformats.org/officeDocument/2006/docPropsVTypes">'
        "<Application>Codex</Application>"
        f"<HeadingPairs>{heading_pairs}</HeadingPairs>"
        f'<TitlesOfParts><vt:vector size="{len(sheet_names)}" baseType="lpstr">{titles}</vt:vector></TitlesOfParts>'
        "</Properties>"
    )


def _styles_xml() -> str:
    return (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        f'<styleSheet xmlns="{NS_MAIN}">'
        '<fonts count="4">'
        '<font><sz val="11"/><color theme="1"/><name val="Aptos"/><family val="2"/></font>'
        '<font><b/><sz val="11"/><color rgb="FFFFFFFF"/><name val="Aptos"/><family val="2"/></font>'
        '<font><b/><sz val="11"/><color rgb="FF0F172A"/><name val="Aptos"/><family val="2"/></font>'
        '<font><b/><sz val="11"/><color rgb="FF1F2937"/><name val="Aptos"/><family val="2"/></font>'
        "</fonts>"
        '<fills count="5">'
        '<fill><patternFill patternType="none"/></fill>'
        '<fill><patternFill patternType="gray125"/></fill>'
        '<fill><patternFill patternType="solid"><fgColor rgb="FF0F766E"/><bgColor rgb="FF0F766E"/></patternFill></fill>'
        '<fill><patternFill patternType="solid"><fgColor rgb="FFE0F2FE"/><bgColor rgb="FFE0F2FE"/></patternFill></fill>'
        '<fill><patternFill patternType="solid"><fgColor rgb="FFF1F5F9"/><bgColor rgb="FFF1F5F9"/></patternFill></fill>'
        "</fills>"
        '<borders count="1"><border><left/><right/><top/><bottom/><diagonal/></border></borders>'
        '<cellStyleXfs count="1"><xf numFmtId="0" fontId="0" fillId="0" borderId="0"/></cellStyleXfs>'
        '<cellXfs count="4">'
        '<xf numFmtId="0" fontId="0" fillId="0" borderId="0" xfId="0"/>'
        '<xf numFmtId="0" fontId="1" fillId="2" borderId="0" xfId="0" applyFont="1" applyFill="1" applyAlignment="1"><alignment vertical="center" wrapText="1"/></xf>'
        '<xf numFmtId="0" fontId="2" fillId="3" borderId="0" xfId="0" applyFont="1" applyFill="1" applyAlignment="1"><alignment vertical="center" wrapText="1"/></xf>'
        '<xf numFmtId="0" fontId="3" fillId="4" borderId="0" xfId="0" applyFont="1" applyFill="1" applyAlignment="1"><alignment vertical="center" wrapText="1"/></xf>'
        "</cellXfs>"
        '<cellStyles count="1"><cellStyle name="Normal" xfId="0" builtinId="0"/></cellStyles>'
        '<dxfs count="0"/>'
        '<tableStyles count="0" defaultTableStyle="TableStyleMedium2" defaultPivotStyle="PivotStyleLight16"/>'
        "</styleSheet>"
    )


def _value_cell(value: Any) -> Cell:
    if isinstance(value, bool):
        return Cell.number(1 if value else 0)
    if isinstance(value, (int, float)):
        return Cell.number(value)
    return Cell.string(str(value))


def _sheet_columns_xml(sheet: Sheet, max_cols: int) -> str:
    column_xml: list[str] = []
    widths = _estimate_column_widths(sheet.rows, max_cols=max_cols)
    for col_index in range(1, max_cols + 1):
        width = widths.get(col_index)
        if width is None:
            continue
        column_xml.append(
            f'<col min="{col_index}" max="{col_index}" width="{width:.2f}" customWidth="1"/>'
        )
    if not column_xml:
        return ""
    return f"<cols>{''.join(column_xml)}</cols>"


def _estimate_column_widths(rows: list[list[Cell]], *, max_cols: int) -> dict[int, float]:
    widths: dict[int, float] = {}
    has_assumption_layout = any(
        row
        and row[0].kind == "string"
        and str(row[0].value).startswith("[")
        for row in rows
    )
    for col_index in range(1, max_cols + 1):
        max_length = 0
        for row in rows:
            if len(row) < col_index:
                continue
            cell = row[col_index - 1]
            text = str(cell.value).strip()
            if not text:
                continue
            normalized = text.replace("_", " ")
            text_length = len(normalized)
            if cell.style_id == STYLE_COLUMN_HEADER:
                text_length += 2
            elif cell.style_id == STYLE_SECTION_HEADER:
                text_length += 4
            max_length = max(max_length, text_length)
        if max_length == 0:
            continue
        min_width = 10.0
        max_width = 22.0
        if col_index == 1:
            min_width = 18.0
            max_width = 40.0
        elif has_assumption_layout and col_index == 3:
            min_width = 20.0
            max_width = 56.0
        estimated = max(min_width, min(max_width, max_length * 0.95 + 2.0))
        widths[col_index] = estimated
    return widths


def _styled_row(cells: list[Cell], style_id: int) -> list[Cell]:
    return [
        Cell(kind=cell.kind, value=cell.value, style_id=style_id)
        for cell in cells
    ]


def _assumption_block(
    title: str,
    rows: list[tuple[str, Any, str]],
) -> list[list[Cell]]:
    output: list[list[Cell]] = [
        _styled_row(
            [Cell.string(f"[{title}]"), Cell.string(""), Cell.string("")],
            STYLE_SECTION_HEADER,
        ),
        _styled_row(
            [Cell.string("name"), Cell.string("value"), Cell.string("details")],
            STYLE_COLUMN_HEADER,
        ),
    ]
    for name, value, detail in rows:
        output.append(
            [
                Cell.string(name, style_id=STYLE_ROW_HEADER),
                _value_cell(value),
                Cell.string(detail),
            ]
        )
    output.append([Cell.string(""), Cell.string(""), Cell.string("")])
    return output


def write_projection_workbook(
    output_path: Path,
    *,
    assumptions: RevenueProjectionAssumptions,
    escrow_rows: list[dict[str, Any]],
    mau_rows: list[dict[str, Any]],
    saas_rows: list[dict[str, Any]],
    escrow_logistics_rows: list[dict[str, Any]],
    expense_rows: list[dict[str, Any]],
) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)

    escrow_sheet_rows = _assumption_block(
        "Escrow Revenue Assumptions",
        [
            (
                "escrow_settlement_stablecoin",
                assumptions.escrow_settlement_stablecoin,
                "Primary settlement stablecoin for the escrow flow.",
            ),
            (
                "escrow_fee_rate",
                assumptions.escrow_fee_rate,
                "Percentage fee charged on escrowed stablecoin volume.",
            ),
            (
                "baseline_monthly_escrow_volume_usd",
                assumptions.baseline_monthly_escrow_volume_usd,
                "Baseline monthly escrow volume used as model anchor.",
            ),
            (
                "baseline_monthly_escrow_transactions",
                assumptions.baseline_monthly_escrow_transactions,
                "Baseline monthly escrow transactions used as model anchor.",
            ),
            (
                "escrow_volume_annual_growth",
                assumptions.escrow_volume_annual_growth,
                "Annual growth rate applied to escrow volume.",
            ),
            (
                "escrow_transactions_annual_growth",
                assumptions.escrow_transactions_annual_growth,
                "Annual growth rate applied to escrow transaction count.",
            ),
            (
                "projection_start_month",
                assumptions.projection_start_month,
                "First month in the projection horizon (YYYY-MM).",
            ),
            (
                "projection_months",
                assumptions.projection_months,
                "Number of monthly rows generated.",
            ),
            ("jitter_std", assumptions.jitter_std, "Monthly volatility term."),
            ("seed", assumptions.seed, "Random seed for deterministic generation."),
        ],
    )
    escrow_sheet_rows.append(
        _styled_row(
            [
            Cell.string("month"),
            Cell.string("year_index"),
            Cell.string("phase"),
            Cell.string("escrow_transaction_count"),
            Cell.string("avg_escrow_size_usd"),
            Cell.string("escrow_volume_usd"),
            Cell.string("escrow_fee_rate"),
            Cell.string("escrow_fee_revenue_usd"),
            Cell.string("settlement_stablecoin"),
            ],
            STYLE_COLUMN_HEADER,
        )
    )
    for row in escrow_rows:
        escrow_sheet_rows.append(
            [
                Cell.string(str(row["month"])),
                Cell.number(int(row["year_index"])),
                Cell.string(str(row["phase"])),
                Cell.number(float(row["escrow_transaction_count"])),
                Cell.number(float(row["avg_escrow_size_usd"])),
                Cell.number(float(row["escrow_volume_usd"])),
                Cell.number(float(row["escrow_fee_rate"])),
                Cell.number(float(row["escrow_fee_revenue_usd"])),
                Cell.string(str(row["settlement_stablecoin"])),
            ]
        )

    escrow_logistics_sheet_rows = _assumption_block(
        "Escrow + Logistics Assumptions",
        [
            (
                "escrow_logistics_enabled",
                assumptions.escrow_logistics_enabled,
                "Flag to enable logistics-oracle managed-service scenario rows.",
            ),
            (
                "escrow_logistics_launch_month_offset",
                assumptions.escrow_logistics_launch_month_offset,
                "Month index offset (0-based) when logistics product starts.",
            ),
            (
                "escrow_logistics_txn_adoption_rate_start",
                assumptions.escrow_logistics_txn_adoption_rate_start,
                "Share of escrow transactions using logistics at launch.",
            ),
            (
                "escrow_logistics_txn_adoption_rate_end",
                assumptions.escrow_logistics_txn_adoption_rate_end,
                "Share of escrow transactions using logistics by month 36.",
            ),
            (
                "escrow_logistics_org_adoption_rate_start",
                assumptions.escrow_logistics_org_adoption_rate_start,
                "Share of paying developer orgs using logistics at launch.",
            ),
            (
                "escrow_logistics_org_adoption_rate_end",
                assumptions.escrow_logistics_org_adoption_rate_end,
                "Share of paying developer orgs using logistics by month 36.",
            ),
            (
                "escrow_logistics_fee_uplift_rate",
                assumptions.escrow_logistics_fee_uplift_rate,
                "Additional escrow bps charged on logistics-enabled escrow volume.",
            ),
            (
                "escrow_logistics_oracle_events_per_txn",
                assumptions.escrow_logistics_oracle_events_per_txn,
                "Average carrier/oracle verification events billed per escrow transaction.",
            ),
            (
                "escrow_logistics_oracle_fee_per_event_usd",
                assumptions.escrow_logistics_oracle_fee_per_event_usd,
                "Revenue billed per logistics oracle event.",
            ),
            (
                "escrow_logistics_platform_fee_monthly_usd",
                assumptions.escrow_logistics_platform_fee_monthly_usd,
                "Monthly managed-service platform fee per active logistics org.",
            ),
            (
                "escrow_logistics_carrier_data_cost_per_event_usd",
                assumptions.escrow_logistics_carrier_data_cost_per_event_usd,
                "Direct carrier/tracking data cost per event.",
            ),
            (
                "escrow_logistics_attestation_cost_per_event_usd",
                assumptions.escrow_logistics_attestation_cost_per_event_usd,
                "Attestation/compute cost per oracle event.",
            ),
            (
                "escrow_logistics_dispute_rate",
                assumptions.escrow_logistics_dispute_rate,
                "Dispute incidence rate for logistics-enabled escrow transactions.",
            ),
            (
                "escrow_logistics_dispute_cost_per_case_usd",
                assumptions.escrow_logistics_dispute_cost_per_case_usd,
                "Direct dispute operations cost per logistics dispute case.",
            ),
            (
                "escrow_logistics_support_cost_per_active_org_usd",
                assumptions.escrow_logistics_support_cost_per_active_org_usd,
                "Monthly support/compliance operations cost per active logistics org.",
            ),
        ],
    )
    escrow_logistics_sheet_rows.append(
        _styled_row(
            [
            Cell.string("month"),
            Cell.string("year_index"),
            Cell.string("phase"),
            Cell.string("escrow_transaction_count"),
            Cell.string("escrow_volume_usd"),
            Cell.string("paying_developer_org_count"),
            Cell.string("txn_adoption_rate"),
            Cell.string("org_adoption_rate"),
            Cell.string("logistics_escrow_txn_count"),
            Cell.string("logistics_escrow_volume_usd"),
            Cell.string("active_logistics_org_count"),
            Cell.string("oracle_events_per_txn"),
            Cell.string("oracle_event_count"),
            Cell.string("escrow_fee_uplift_rate"),
            Cell.string("escrow_fee_uplift_revenue_usd"),
            Cell.string("oracle_fee_per_event_usd"),
            Cell.string("oracle_event_revenue_usd"),
            Cell.string("platform_fee_monthly_usd"),
            Cell.string("platform_subscription_revenue_usd"),
            Cell.string("total_logistics_revenue_usd"),
            Cell.string("carrier_data_cost_per_event_usd"),
            Cell.string("carrier_data_cost_usd"),
            Cell.string("attestation_cost_per_event_usd"),
            Cell.string("attestation_compute_cost_usd"),
            Cell.string("dispute_rate"),
            Cell.string("dispute_case_count"),
            Cell.string("dispute_cost_per_case_usd"),
            Cell.string("dispute_ops_cost_usd"),
            Cell.string("support_cost_per_active_org_usd"),
            Cell.string("support_cost_usd"),
            Cell.string("total_logistics_cost_usd"),
            Cell.string("logistics_contribution_usd"),
            Cell.string("logistics_gross_margin_pct"),
            Cell.string("logistics_take_rate_pct"),
            ],
            STYLE_COLUMN_HEADER,
        )
    )
    for row in escrow_logistics_rows:
        escrow_logistics_sheet_rows.append(
            [
                Cell.string(str(row["month"])),
                Cell.number(int(row["year_index"])),
                Cell.string(str(row["phase"])),
                Cell.number(float(row["escrow_transaction_count"])),
                Cell.number(float(row["escrow_volume_usd"])),
                Cell.number(float(row["paying_developer_org_count"])),
                Cell.number(float(row["txn_adoption_rate"])),
                Cell.number(float(row["org_adoption_rate"])),
                Cell.number(float(row["logistics_escrow_txn_count"])),
                Cell.number(float(row["logistics_escrow_volume_usd"])),
                Cell.number(float(row["active_logistics_org_count"])),
                Cell.number(float(row["oracle_events_per_txn"])),
                Cell.number(float(row["oracle_event_count"])),
                Cell.number(float(row["escrow_fee_uplift_rate"])),
                Cell.number(float(row["escrow_fee_uplift_revenue_usd"])),
                Cell.number(float(row["oracle_fee_per_event_usd"])),
                Cell.number(float(row["oracle_event_revenue_usd"])),
                Cell.number(float(row["platform_fee_monthly_usd"])),
                Cell.number(float(row["platform_subscription_revenue_usd"])),
                Cell.number(float(row["total_logistics_revenue_usd"])),
                Cell.number(float(row["carrier_data_cost_per_event_usd"])),
                Cell.number(float(row["carrier_data_cost_usd"])),
                Cell.number(float(row["attestation_cost_per_event_usd"])),
                Cell.number(float(row["attestation_compute_cost_usd"])),
                Cell.number(float(row["dispute_rate"])),
                Cell.number(float(row["dispute_case_count"])),
                Cell.number(float(row["dispute_cost_per_case_usd"])),
                Cell.number(float(row["dispute_ops_cost_usd"])),
                Cell.number(float(row["support_cost_per_active_org_usd"])),
                Cell.number(float(row["support_cost_usd"])),
                Cell.number(float(row["total_logistics_cost_usd"])),
                Cell.number(float(row["logistics_contribution_usd"])),
                Cell.number(float(row["logistics_gross_margin_pct"])),
                Cell.number(float(row["logistics_take_rate_pct"])),
            ]
        )

    mau_sheet_rows = _assumption_block(
        "MAU Assumptions",
        [
            ("new_users_start", assumptions.new_users_start, "Starting monthly cohort size."),
            (
                "new_users_monthly_growth_year1",
                assumptions.new_users_monthly_growth_year1,
                "Monthly new-user growth rate for year 1.",
            ),
            (
                "new_users_monthly_growth_year2",
                assumptions.new_users_monthly_growth_year2,
                "Monthly new-user growth rate for year 2.",
            ),
            (
                "new_users_monthly_growth_year3",
                assumptions.new_users_monthly_growth_year3,
                "Monthly new-user growth rate for year 3.",
            ),
            (
                "new_user_holiday_spike_multiplier",
                assumptions.new_user_holiday_spike_multiplier,
                "Multiplier applied in November and December.",
            ),
            ("user_retention_month_1", assumptions.user_retention_month_1, "Share retained in month 1."),
            ("user_retention_month_2", assumptions.user_retention_month_2, "Share retained in month 2."),
            ("user_retention_month_3", assumptions.user_retention_month_3, "Share retained in month 3."),
            ("user_retention_decay", assumptions.user_retention_decay, "Decay applied from month 4 onward."),
            (
                "avg_end_user_mau_per_org_start",
                assumptions.avg_end_user_mau_per_org_start,
                "Average end-user MAU managed by each developer org at projection start.",
            ),
            (
                "avg_end_user_mau_per_org_end",
                assumptions.avg_end_user_mau_per_org_end,
                "Average end-user MAU managed by each developer org at projection end.",
            ),
            (
                "developer_org_paying_ratio",
                assumptions.developer_org_paying_ratio,
                "Share of developer orgs that are paying subscription customers.",
            ),
        ],
    )
    mau_sheet_rows.append(
        _styled_row(
            [
            Cell.string("month"),
            Cell.string("year_index"),
            Cell.string("phase"),
            Cell.string("new_users"),
            Cell.string("returning_users"),
            Cell.string("mau"),
            Cell.string("acquisition_growth_rate"),
            Cell.string("base_new_users"),
            Cell.string("seasonality_factor"),
            Cell.string("noise_acquisition"),
            Cell.string("developer_org_count"),
            Cell.string("paying_developer_org_count"),
            Cell.string("avg_end_user_mau_per_org"),
            Cell.string("avg_end_user_mau_per_paying_org"),
            ],
            STYLE_COLUMN_HEADER,
        )
    )
    for row in mau_rows:
        mau_sheet_rows.append(
            [
                Cell.string(str(row["month"])),
                Cell.number(int(row["year_index"])),
                Cell.string(str(row["phase"])),
                Cell.number(float(row["new_users"])),
                Cell.number(float(row["returning_users"])),
                Cell.number(float(row["mau"])),
                Cell.number(float(row["acquisition_growth_rate"])),
                Cell.number(float(row["base_new_users"])),
                Cell.number(float(row["seasonality_factor"])),
                Cell.number(float(row["noise_acquisition"])),
                Cell.number(float(row["developer_org_count"])),
                Cell.number(float(row["paying_developer_org_count"])),
                Cell.number(float(row["avg_end_user_mau_per_org"])),
                Cell.number(float(row["avg_end_user_mau_per_paying_org"])),
            ]
        )

    saas_sheet_rows = _assumption_block(
        "SaaS Revenue Assumptions",
        [
            (
                "developer_subscription_monthly_price_usd",
                assumptions.developer_subscription_monthly_price_usd,
                "Base monthly subscription charged per paying developer org.",
            ),
            (
                "metered_free_tier_mau_cap_per_org",
                assumptions.metered_free_tier_mau_cap_per_org,
                "Per-org MAU cap for free metered pricing.",
            ),
            (
                "metered_starter_tier_mau_cap_per_org",
                assumptions.metered_starter_tier_mau_cap_per_org,
                "Per-org MAU cap for starter metered tier.",
            ),
            (
                "metered_starter_tier_monthly_price_per_org_usd",
                assumptions.metered_starter_tier_monthly_price_per_org_usd,
                "Starter metered fee per paying org.",
            ),
            (
                "metered_growth_tier_mau_cap_per_org",
                assumptions.metered_growth_tier_mau_cap_per_org,
                "Per-org MAU cap for growth metered tier.",
            ),
            (
                "metered_growth_tier_monthly_price_per_org_usd",
                assumptions.metered_growth_tier_monthly_price_per_org_usd,
                "Growth metered fee per paying org.",
            ),
            (
                "metered_scale_tier_mau_cap_per_org",
                assumptions.metered_scale_tier_mau_cap_per_org,
                "Upper MAU bound before enterprise overage pricing per org.",
            ),
            (
                "metered_scale_overage_price_per_mau_usd",
                assumptions.metered_scale_overage_price_per_mau_usd,
                "Per-MAU overage price between growth and scale caps per org.",
            ),
            (
                "metered_enterprise_overage_price_per_mau_usd",
                assumptions.metered_enterprise_overage_price_per_mau_usd,
                "Per-MAU overage price above scale cap per org.",
            ),
            (
                "metered_included_escrow_txns_per_paying_org",
                assumptions.metered_included_escrow_txns_per_paying_org,
                "Monthly escrow transactions included for each paying developer org.",
            ),
            (
                "metered_price_per_additional_escrow_txn_usd",
                assumptions.metered_price_per_additional_escrow_txn_usd,
                "Metered fee per additional escrow transaction.",
            ),
        ],
    )
    saas_sheet_rows.append(
        _styled_row(
            [
            Cell.string("month"),
            Cell.string("year_index"),
            Cell.string("phase"),
            Cell.string("mau"),
            Cell.string("developer_org_count"),
            Cell.string("paying_developer_org_count"),
            Cell.string("avg_end_user_mau_per_paying_org"),
            Cell.string("plan_tier"),
            Cell.string("developer_subscription_price_usd"),
            Cell.string("developer_subscription_revenue_usd"),
            Cell.string("metered_mau_fee_per_paying_org_usd"),
            Cell.string("metered_mau_overage_per_paying_org"),
            Cell.string("metered_mau_overage_price_per_unit_usd"),
            Cell.string("metered_mau_revenue_usd"),
            Cell.string("escrow_transaction_count"),
            Cell.string("included_escrow_txns"),
            Cell.string("billable_escrow_txns"),
            Cell.string("metered_price_per_additional_escrow_txn_usd"),
            Cell.string("metered_escrow_txn_revenue_usd"),
            Cell.string("saas_revenue_usd"),
            Cell.string("effective_arpu_usd"),
            ],
            STYLE_COLUMN_HEADER,
        )
    )
    for row in saas_rows:
        saas_sheet_rows.append(
            [
                Cell.string(str(row["month"])),
                Cell.number(int(row["year_index"])),
                Cell.string(str(row["phase"])),
                Cell.number(float(row["mau"])),
                Cell.number(float(row["developer_org_count"])),
                Cell.number(float(row["paying_developer_org_count"])),
                Cell.number(float(row["avg_end_user_mau_per_paying_org"])),
                Cell.string(str(row["plan_tier"])),
                Cell.number(float(row["developer_subscription_price_usd"])),
                Cell.number(float(row["developer_subscription_revenue_usd"])),
                Cell.number(float(row["metered_mau_fee_per_paying_org_usd"])),
                Cell.number(float(row["metered_mau_overage_per_paying_org"])),
                Cell.number(float(row["metered_mau_overage_price_per_unit_usd"])),
                Cell.number(float(row["metered_mau_revenue_usd"])),
                Cell.number(float(row["escrow_transaction_count"])),
                Cell.number(float(row["included_escrow_txns"])),
                Cell.number(float(row["billable_escrow_txns"])),
                Cell.number(float(row["metered_price_per_additional_escrow_txn_usd"])),
                Cell.number(float(row["metered_escrow_txn_revenue_usd"])),
                Cell.number(float(row["saas_revenue_usd"])),
                Cell.number(float(row["effective_arpu_usd"])),
            ]
        )

    expenses_sheet_rows = _assumption_block(
        "OpEx Assumptions",
        [
            (
                "infrastructure_base_monthly_usd",
                assumptions.infrastructure_base_monthly_usd,
                "Base infrastructure cost independent of usage.",
            ),
            (
                "infrastructure_cost_per_mau_usd",
                assumptions.infrastructure_cost_per_mau_usd,
                "Variable infrastructure cost per MAU.",
            ),
            (
                "infrastructure_cost_per_new_user_usd",
                assumptions.infrastructure_cost_per_new_user_usd,
                "Variable infrastructure cost per newly acquired user.",
            ),
            (
                "infrastructure_cost_per_escrow_txn_usd",
                assumptions.infrastructure_cost_per_escrow_txn_usd,
                "Variable infrastructure cost per escrow transaction.",
            ),
            ("team_size_year1", assumptions.team_size_year1, "Headcount assumption in year 1."),
            ("team_size_year2", assumptions.team_size_year2, "Headcount assumption in year 2."),
            ("team_size_year3", assumptions.team_size_year3, "Headcount assumption in year 3."),
            (
                "software_tools_per_team_member_monthly_usd",
                assumptions.software_tools_per_team_member_monthly_usd,
                "SaaS tooling cost per team member.",
            ),
            ("incorporation_setup_usd", assumptions.incorporation_setup_usd, "One-time setup cost in first projected month."),
        ],
    )
    expenses_sheet_rows.append(
        _styled_row(
            [
            Cell.string("month"),
            Cell.string("year_index"),
            Cell.string("phase"),
            Cell.string("technology_and_infrastructure_opex_usd"),
            Cell.string("sales_and_marketing_opex_usd"),
            Cell.string("general_and_administrative_opex_usd"),
            Cell.string("total_operating_expenses_usd"),
            ],
            STYLE_COLUMN_HEADER,
        )
    )
    for row in expense_rows:
        expenses_sheet_rows.append(
            [
                Cell.string(str(row["month"])),
                Cell.number(int(row["year_index"])),
                Cell.string(str(row["phase"])),
                Cell.number(float(row["technology_and_infrastructure_opex_usd"])),
                Cell.number(float(row["sales_and_marketing_opex_usd"])),
                Cell.number(float(row["general_and_administrative_opex_usd"])),
                Cell.number(float(row["total_operating_expenses_usd"])),
            ]
        )

    escrow_revenue_values = [float(row["escrow_fee_revenue_usd"]) for row in escrow_rows]
    saas_revenue_values = [float(row["saas_revenue_usd"]) for row in saas_rows]
    base_total_revenue_values = [
        round(escrow_revenue_values[index] + saas_revenue_values[index], 2)
        for index in range(len(escrow_rows))
    ]
    logistics_revenue_values = [
        float(row["total_logistics_revenue_usd"]) for row in escrow_logistics_rows
    ]
    logistics_cost_values = [
        float(row["total_logistics_cost_usd"]) for row in escrow_logistics_rows
    ]
    logistics_contribution_values = [
        round(logistics_revenue_values[index] - logistics_cost_values[index], 2)
        for index in range(len(escrow_rows))
    ]
    total_revenue_values = [
        round(base_total_revenue_values[index] + logistics_revenue_values[index], 2)
        for index in range(len(escrow_rows))
    ]
    total_opex_values = [float(row["total_operating_expenses_usd"]) for row in expense_rows]
    adjusted_total_opex_values = [
        round(total_opex_values[index] + logistics_cost_values[index], 2)
        for index in range(len(escrow_rows))
    ]
    base_operating_profit_values = [
        round(base_total_revenue_values[index] - total_opex_values[index], 2)
        for index in range(len(total_revenue_values))
    ]
    operating_profit_values = [
        round(total_revenue_values[index] - adjusted_total_opex_values[index], 2)
        for index in range(len(total_revenue_values))
    ]
    month_headers = _styled_row(
        [Cell.string("month")] + [Cell.string(str(row["month"])) for row in escrow_rows],
        STYLE_COLUMN_HEADER,
    )
    summary_rows: list[list[Cell]] = [
        _styled_row(
            [
                Cell.string("[Summary]"),
                Cell.string(""),
                Cell.string("36-month revenue and operating profit summary for the wallet-as-a-service model."),
            ],
            STYLE_SECTION_HEADER,
        ),
        [Cell.string("")],
        month_headers,
        [Cell.string("Escrow Fee Revenue", style_id=STYLE_ROW_HEADER)]
        + [Cell.number(value) for value in escrow_revenue_values],
        [Cell.string("SaaS Revenue", style_id=STYLE_ROW_HEADER)]
        + [Cell.number(value) for value in saas_revenue_values],
        [Cell.string("Total Revenue (Base Wallet)", style_id=STYLE_ROW_HEADER)]
        + [Cell.number(value) for value in base_total_revenue_values],
        [Cell.string("Escrow + Logistics Revenue", style_id=STYLE_ROW_HEADER)]
        + [Cell.number(value) for value in logistics_revenue_values],
        [Cell.string("Total Revenue (With Logistics)", style_id=STYLE_ROW_HEADER)]
        + [Cell.number(value) for value in total_revenue_values],
        [Cell.string("")],
        [Cell.string("Total Operating Expenses", style_id=STYLE_ROW_HEADER)]
        + [Cell.number(value) for value in total_opex_values],
        [Cell.string("Operating Profit / (Loss) Base", style_id=STYLE_ROW_HEADER)]
        + [Cell.number(value) for value in base_operating_profit_values],
        [Cell.string("Escrow + Logistics Direct Costs", style_id=STYLE_ROW_HEADER)]
        + [Cell.number(value) for value in logistics_cost_values],
        [Cell.string("Escrow + Logistics Contribution", style_id=STYLE_ROW_HEADER)]
        + [Cell.number(value) for value in logistics_contribution_values],
        [Cell.string("Adjusted Operating Expenses (With Logistics)", style_id=STYLE_ROW_HEADER)]
        + [Cell.number(value) for value in adjusted_total_opex_values],
        [Cell.string("Operating Profit / (Loss) With Logistics", style_id=STYLE_ROW_HEADER)]
        + [Cell.number(value) for value in operating_profit_values],
    ]

    sheets = [
        Sheet(SHEET_SUMMARY, summary_rows),
        Sheet(SHEET_ESCROW_REVENUE, escrow_sheet_rows),
        Sheet(SHEET_ESCROW_LOGISTICS, escrow_logistics_sheet_rows),
        Sheet(SHEET_MAU, mau_sheet_rows),
        Sheet(SHEET_SAAS_PRICING, saas_sheet_rows),
        Sheet(SHEET_EXPENSES, expenses_sheet_rows),
    ]

    temp_output_path = output_path.with_name(f".{output_path.name}.tmp")
    if temp_output_path.exists():
        temp_output_path.unlink()

    with ZipFile(temp_output_path, "w", compression=ZIP_DEFLATED) as archive:
        archive.writestr("[Content_Types].xml", _content_types_xml(len(sheets)))
        archive.writestr("_rels/.rels", _root_rels_xml())
        archive.writestr("docProps/core.xml", _core_xml())
        archive.writestr("docProps/app.xml", _app_xml([sheet.name for sheet in sheets]))
        archive.writestr("xl/workbook.xml", _workbook_xml(sheets))
        archive.writestr("xl/styles.xml", _styles_xml())
        archive.writestr("xl/_rels/workbook.xml.rels", _workbook_rels_xml(len(sheets)))
        for index, sheet in enumerate(sheets, start=1):
            archive.writestr(f"xl/worksheets/sheet{index}.xml", _sheet_xml(sheet))

    temp_output_path.replace(output_path)


def read_projection_sheet_rows(path: Path, sheet_name: str) -> list[dict[str, str]]:
    if not path.exists():
        raise FileNotFoundError(f"projection workbook not found: {path}")

    with ZipFile(path, "r") as archive:
        workbook_xml = ET.fromstring(archive.read("xl/workbook.xml"))
        workbook_rels_xml = ET.fromstring(archive.read("xl/_rels/workbook.xml.rels"))

        rel_targets = {
            rel.attrib["Id"]: rel.attrib["Target"]
            for rel in workbook_rels_xml.findall(f"{{{NS_PACKAGE}}}Relationship")
        }

        worksheet_target = None
        for sheet in workbook_xml.findall(f"{{{NS_MAIN}}}sheets/{{{NS_MAIN}}}sheet"):
            if sheet.attrib.get("name") == sheet_name:
                rel_id = sheet.attrib.get(f"{{{NS_REL}}}id")
                worksheet_target = rel_targets.get(rel_id or "")
                break
        if not worksheet_target:
            raise ValueError(f"sheet not found in workbook: {sheet_name}")

        worksheet_xml = ET.fromstring(archive.read(f"xl/{worksheet_target}"))

    rows_by_index: dict[int, dict[int, str]] = {}
    for row in worksheet_xml.findall(f"{{{NS_MAIN}}}sheetData/{{{NS_MAIN}}}row"):
        row_number = int(row.attrib["r"])
        cell_map: dict[int, str] = {}
        for cell in row.findall(f"{{{NS_MAIN}}}c"):
            ref = cell.attrib.get("r", "")
            column_index = _column_index(ref)
            cell_type = cell.attrib.get("t", "")
            value = ""
            if cell_type == "inlineStr":
                text_node = cell.find(f"{{{NS_MAIN}}}is/{{{NS_MAIN}}}t")
                value = text_node.text if text_node is not None and text_node.text is not None else ""
            else:
                value_node = cell.find(f"{{{NS_MAIN}}}v")
                value = value_node.text if value_node is not None and value_node.text is not None else ""
            cell_map[column_index] = value
        rows_by_index[row_number] = cell_map

    header_row_number = next(
        (
            row_number
            for row_number in sorted(rows_by_index.keys())
            if rows_by_index[row_number].get(1, "") == "month"
        ),
        1,
    )
    header_cells = rows_by_index.get(header_row_number, {})
    headers = {
        column_index: value
        for column_index, value in header_cells.items()
        if value
    }
    output: list[dict[str, str]] = []
    for row_number in sorted(number for number in rows_by_index.keys() if number > header_row_number):
        row_cells = rows_by_index[row_number]
        record = {
            header: row_cells.get(column_index, "")
            for column_index, header in headers.items()
        }
        if not any(value != "" for value in record.values()):
            if output:
                break
            continue
        if row_cells.get(1, "") == "month":
            break
        output.append(record)
    return output
