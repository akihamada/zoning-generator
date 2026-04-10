"""
検定表XLSX自動出力モジュール

CheckResult のリストを受け取り、確認申請補助資料として使えるXLSX形式で出力する。

出典:
  出力内容は以下に基づく検定結果の整理表:
  - 建築基準法施行令 第82条
  - 鋼構造設計規準（日本建築学会, 2005/2019）

依存: openpyxl

単位: N, mm, N/mm²
"""

from datetime import datetime
from typing import Optional

import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

import jp_struct

# --- スタイル定義 ---
_FONT_HEADER = Font(name="Yu Gothic", size=10, bold=True)
_FONT_NORMAL = Font(name="Yu Gothic", size=10)
_FONT_TITLE = Font(name="Yu Gothic", size=14, bold=True)
_FONT_SUBTITLE = Font(name="Yu Gothic", size=10, color="666666")

_FILL_HEADER = PatternFill(start_color="4472C4", end_color="4472C4", fill_type="solid")
_FILL_NG = PatternFill(start_color="FF6666", end_color="FF6666", fill_type="solid")
_FILL_WARN = PatternFill(start_color="FFFF66", end_color="FFFF66", fill_type="solid")
_FILL_OK = PatternFill(start_color="FFFFFF", end_color="FFFFFF", fill_type="solid")

_FONT_HEADER_WHITE = Font(name="Yu Gothic", size=10, bold=True, color="FFFFFF")

_ALIGN_CENTER = Alignment(horizontal="center", vertical="center")
_ALIGN_RIGHT = Alignment(horizontal="right", vertical="center")
_ALIGN_LEFT = Alignment(horizontal="left", vertical="center")

_THIN_BORDER = Border(
    left=Side(style="thin"),
    right=Side(style="thin"),
    top=Side(style="thin"),
    bottom=Side(style="thin"),
)


def _apply_header_style(cell):
    """ヘッダセルのスタイルを適用"""
    cell.font = _FONT_HEADER_WHITE
    cell.fill = _FILL_HEADER
    cell.alignment = _ALIGN_CENTER
    cell.border = _THIN_BORDER


def _apply_data_style(cell, ratio: float = 0.0):
    """データセルのスタイルを適用（検定比に応じた背景色）"""
    cell.font = _FONT_NORMAL
    cell.border = _THIN_BORDER
    if ratio > 1.0:
        cell.fill = _FILL_NG
    elif ratio > 0.9:
        cell.fill = _FILL_WARN
    else:
        cell.fill = _FILL_OK


def generate_report(
    results: list,
    filepath: str,
    project_name: str = "",
    author: str = "",
) -> str:
    """検定結果をXLSXファイルとして出力する

    Parameters:
        results:      CheckResult のリスト
        filepath:     出力ファイルパス (.xlsx)
        project_name: プロジェクト名（ヘッダに記載）
        author:       作成者名

    Returns:
        出力ファイルパス

    出力シート:
      シート1「部材一覧」: ID, 断面, 材料, L, lb, 幅厚比区分, 検定比, 判定
      シート2「詳細」: 各部材の応力, 許容応力度, 細長比, 等
      シート3「凡例」: 検定式と出典
    """
    wb = openpyxl.Workbook()

    # --- シート1: 部材一覧 ---
    ws1 = wb.active
    ws1.title = "部材一覧"
    _write_summary_sheet(ws1, results, project_name, author)

    # --- シート2: 詳細 ---
    ws2 = wb.create_sheet("詳細")
    _write_detail_sheet(ws2, results)

    # --- シート3: 凡例 ---
    ws3 = wb.create_sheet("凡例")
    _write_legend_sheet(ws3)

    wb.save(filepath)
    return filepath


def _write_summary_sheet(ws, results, project_name, author):
    """シート1: 部材一覧"""
    # タイトル
    ws.merge_cells("A1:H1")
    ws["A1"] = "構造部材検定一覧表"
    ws["A1"].font = _FONT_TITLE

    # メタ情報
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    ws["A2"] = f"作成日時: {now}  jp_struct v{jp_struct.__version__}"
    ws["A2"].font = _FONT_SUBTITLE
    if project_name:
        ws["A3"] = f"プロジェクト: {project_name}"
        ws["A3"].font = _FONT_SUBTITLE
    if author:
        ws["B3"] = f"作成者: {author}"
        ws["B3"].font = _FONT_SUBTITLE

    # ヘッダ行
    headers = [
        "部材ID", "断面", "材料", "F\n(N/mm²)",
        "荷重期間", "幅厚比\n区分", "最大\n検定比", "判定",
    ]
    row = 5
    for col, header in enumerate(headers, 1):
        cell = ws.cell(row=row, column=col, value=header)
        _apply_header_style(cell)

    # データ行
    for i, r in enumerate(results):
        row = 6 + i
        data = [
            r.member_id, r.section_name, r.material_name,
            r.F, r.duration, r.wt_rank,
            r.ratio_max, r.judge,
        ]
        for col, val in enumerate(data, 1):
            cell = ws.cell(row=row, column=col, value=val)
            _apply_data_style(cell, r.ratio_max)
            if col in (4, 7):  # 数値列
                cell.alignment = _ALIGN_RIGHT
                if col == 7:
                    cell.number_format = "0.0000"
            elif col == 8:
                cell.alignment = _ALIGN_CENTER

    # 列幅
    widths = [12, 22, 10, 10, 10, 10, 10, 8]
    for i, w in enumerate(widths, 1):
        ws.column_dimensions[get_column_letter(i)].width = w


def _write_detail_sheet(ws, results):
    """シート2: 詳細"""
    headers = [
        "部材ID", "断面", "材料", "F",
        "σc", "σt", "σb", "τ",
        "fc", "ft", "fb", "fs",
        "λx", "λy", "幅厚比区分",
        "検定比\n(組合せ)", "検定比\n(せん断)", "最大\n検定比", "判定",
    ]
    for col, header in enumerate(headers, 1):
        cell = ws.cell(row=1, column=col, value=header)
        _apply_header_style(cell)

    for i, r in enumerate(results):
        row = 2 + i
        data = [
            r.member_id, r.section_name, r.material_name, r.F,
            r.sigma_c, r.sigma_t, r.sigma_b, r.tau,
            r.fc, r.ft, r.fb, r.fs,
            r.lambda_x, r.lambda_y, r.wt_rank,
            r.ratio_combined, r.ratio_shear, r.ratio_max, r.judge,
        ]
        for col, val in enumerate(data, 1):
            cell = ws.cell(row=row, column=col, value=val)
            _apply_data_style(cell, r.ratio_max)
            if isinstance(val, float):
                cell.alignment = _ALIGN_RIGHT
                cell.number_format = "0.00" if col <= 14 else "0.0000"

    # 列幅
    for i in range(1, len(headers) + 1):
        ws.column_dimensions[get_column_letter(i)].width = 12


def _write_legend_sheet(ws):
    """シート3: 凡例"""
    legends = [
        ("検定式と出典", "", True),
        ("", "", False),
        ("組合せ応力の検定", "鋼構造設計規準 6.1節", False),
        ("  圧縮＋曲げ:", "σc/fc + σb/fb ≤ 1.0", False),
        ("  引張＋曲げ:", "σt/ft + σb/fb ≤ 1.0", False),
        ("  せん断:", "τ/fs ≤ 1.0", False),
        ("", "", False),
        ("許容応力度", "出典", True),
        ("ft = F / 1.5", "令90条", False),
        ("fs = F / (1.5√3)", "令90条", False),
        ("fc（座屈考慮）", "昭55建告第1793号", False),
        ("fb（横座屈考慮）", "H19国交告第594号", False),
        ("", "", False),
        ("幅厚比区分", "H12建告第2464号", True),
        ("FA: コンパクト断面", "局部座屈なし", False),
        ("FB: ノンコンパクト断面", "弾性範囲で局部座屈", False),
        ("FC: スレンダー断面", "弾性座屈あり", False),
        ("FD: 制限外", "設計変更を検討", False),
        ("", "", False),
        ("長期 / 短期", "", True),
        ("長期: 常時荷重", "安全率 1.5", False),
        ("短期: 地震・風・積雪", "許容応力度 = 長期 × 1.5", False),
        ("", "", False),
        ("背景色", "", True),
        ("赤: 検定比 > 1.0 (NG)", "", False),
        ("黄: 検定比 > 0.9 (注意)", "", False),
        ("白: 検定比 ≤ 0.9 (OK)", "", False),
        ("", "", False),
        ("単位系", "", True),
        ("力: N, 長さ: mm, 応力: N/mm²", "", False),
        ("モーメント: N·mm", "", False),
    ]

    for i, (col_a, col_b, is_header) in enumerate(legends, 1):
        cell_a = ws.cell(row=i, column=1, value=col_a)
        cell_b = ws.cell(row=i, column=2, value=col_b)
        if is_header:
            cell_a.font = _FONT_HEADER
        else:
            cell_a.font = _FONT_NORMAL
        cell_b.font = _FONT_NORMAL

    ws.column_dimensions["A"].width = 30
    ws.column_dimensions["B"].width = 30
