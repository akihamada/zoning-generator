"""
Hops サーバ — Grasshopper から jp_struct の検定機能を呼び出す

Flask + ghhops-server を使用。
Rhino8 / Grasshopper の Hops コンポーネントから HTTP 経由でアクセスする。

起動方法:
  cd jp_struct/
  python hops/hops_server.py

エンドポイント:
  /check_h_section   — 圧延H形鋼の部材検定
  /check_bh_section  — BH断面の部材検定
  /check_box_section — 角形鋼管の部材検定
  /generate_report   — 検定結果JSONからXLSXを生成（base64返却）

依存: flask, ghhops-server
"""

import sys
import os
import json
import base64
import tempfile

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from flask import Flask, request, jsonify
import ghhops_server as hs

from jp_struct.sections import (
    get_h_section,
    get_bh_section,
    get_box_section,
    get_material,
    load_h_sections,
    load_bh_sections,
    load_box_sections,
    load_materials,
)
from jp_struct.check import MemberInput, CheckResult, check_member
from jp_struct.report import generate_report

app = Flask(__name__)
hops = hs.Hops(app)


# --- 断面名/材料名バリデーション用キャッシュ ---
_VALID_H_NAMES = None
_VALID_BH_NAMES = None
_VALID_MAT_NAMES = None


def _validate_section_name(name: str, section_type: str) -> str:
    """断面名の存在確認。見つからない場合は候補を含むエラーメッセージを返す"""
    global _VALID_H_NAMES, _VALID_BH_NAMES
    try:
        if section_type == "H":
            if _VALID_H_NAMES is None:
                _VALID_H_NAMES = [s.name for s in load_h_sections()]
            if name not in _VALID_H_NAMES:
                return (
                    f"H形鋼 '{name}' が見つかりません。\n"
                    f"利用可能: {', '.join(_VALID_H_NAMES[:5])} 等 "
                    f"({len(_VALID_H_NAMES)}件)"
                )
        elif section_type == "BH":
            if _VALID_BH_NAMES is None:
                _VALID_BH_NAMES = [s.name for s in load_bh_sections()]
            if name not in _VALID_BH_NAMES:
                return (
                    f"BH断面 '{name}' が見つかりません。\n"
                    f"利用可能: {', '.join(_VALID_BH_NAMES[:5])} 等 "
                    f"({len(_VALID_BH_NAMES)}件)"
                )
    except Exception as e:
        return str(e)
    return ""


def _validate_material_name(name: str) -> str:
    """材料名の存在確認"""
    global _VALID_MAT_NAMES
    try:
        if _VALID_MAT_NAMES is None:
            _VALID_MAT_NAMES = [m.name for m in load_materials()]
        if name not in _VALID_MAT_NAMES:
            return (
                f"鋼材 '{name}' が見つかりません。\n"
                f"利用可能: {', '.join(_VALID_MAT_NAMES)}"
            )
    except Exception as e:
        return str(e)
    return ""


def _format_result(result) -> str:
    """CheckResult をGH向けの文字列に整形"""
    lines = [
        f"部材: {result.member_id}",
        f"断面: {result.section_name} ({result.material_name})",
        f"F = {result.F} N/mm²  ({result.duration})",
        f"幅厚比区分: {result.wt_rank}",
        f"---",
        f"σc = {result.sigma_c:.1f}  fc = {result.fc:.1f} N/mm²",
        f"σt = {result.sigma_t:.1f}  ft = {result.ft:.1f} N/mm²",
        f"σb = {result.sigma_b:.1f}  fb = {result.fb:.1f} N/mm²",
        f"τ  = {result.tau:.1f}  fs = {result.fs:.1f} N/mm²",
        f"---",
        f"検定比(組合せ) = {result.ratio_combined:.4f}",
        f"検定比(せん断) = {result.ratio_shear:.4f}",
        f"最大検定比 = {result.ratio_max:.4f}",
        f"判定: {result.judge}",
    ]
    return "\n".join(lines)


@hops.component(
    "/check_h_section",
    name="CheckHSection",
    description="圧延H形鋼の許容応力度検定（令82条）",
    inputs=[
        hs.HopsString("部材ID", "ID", "部材の識別名"),
        hs.HopsString("断面名", "Sec", "H形鋼名 例: H-400x200x8x13"),
        hs.HopsString("鋼材名", "Mat", "鋼材名 例: SN400B"),
        hs.HopsNumber("部材長", "L", "部材長さ (mm)"),
        hs.HopsNumber("横補剛間距離", "lb", "横補剛間距離 (mm)"),
        hs.HopsNumber("軸力", "N", "軸力 (N) 引張+/圧縮-"),
        hs.HopsNumber("曲げモーメント", "Mx", "強軸曲げモーメント (N·mm)"),
        hs.HopsNumber("せん断力", "Vy", "せん断力 (N)"),
        hs.HopsString("荷重期間", "Dur", "long or short", default="long"),
    ],
    outputs=[
        hs.HopsNumber("検定比", "Ratio", "最大検定比"),
        hs.HopsString("判定", "Judge", "OK or NG"),
        hs.HopsString("詳細", "Detail", "検定結果の詳細"),
    ],
)
def check_h_section(member_id, sec_name, mat_name, L, lb, N, Mx, Vy, duration):
    # 入力バリデーション
    err = _validate_section_name(sec_name, "H")
    if err:
        return 999.0, "ERROR", err
    err = _validate_material_name(mat_name)
    if err:
        return 999.0, "ERROR", err
    try:
        sec = get_h_section(sec_name)
        mat = get_material(mat_name)
        inp = MemberInput(
            member_id=member_id, section=sec, material=mat,
            L=L, lb=lb, N=N, Mx=Mx, Vy=Vy, duration=duration,
        )
        result = check_member(inp)
        return result.ratio_max, result.judge, _format_result(result)
    except Exception as e:
        return 999.0, "ERROR", str(e)


@hops.component(
    "/check_bh_section",
    name="CheckBHSection",
    description="BH断面（溶接組立H形鋼）の許容応力度検定（令82条）",
    inputs=[
        hs.HopsString("部材ID", "ID", "部材の識別名"),
        hs.HopsString("断面名", "Sec", "BH断面名 例: BH-500x200x9x16"),
        hs.HopsString("鋼材名", "Mat", "鋼材名 例: SN400B"),
        hs.HopsNumber("部材長", "L", "部材長さ (mm)"),
        hs.HopsNumber("横補剛間距離", "lb", "横補剛間距離 (mm)"),
        hs.HopsNumber("軸力", "N", "軸力 (N) 引張+/圧縮-"),
        hs.HopsNumber("曲げモーメント", "Mx", "強軸曲げモーメント (N·mm)"),
        hs.HopsNumber("せん断力", "Vy", "せん断力 (N)"),
        hs.HopsString("荷重期間", "Dur", "long or short", default="long"),
    ],
    outputs=[
        hs.HopsNumber("検定比", "Ratio", "最大検定比"),
        hs.HopsString("判定", "Judge", "OK or NG"),
        hs.HopsString("詳細", "Detail", "検定結果の詳細"),
    ],
)
def check_bh_section(member_id, sec_name, mat_name, L, lb, N, Mx, Vy, duration):
    err = _validate_section_name(sec_name, "BH")
    if err:
        return 999.0, "ERROR", err
    err = _validate_material_name(mat_name)
    if err:
        return 999.0, "ERROR", err
    try:
        sec = get_bh_section(sec_name)
        mat = get_material(mat_name)
        inp = MemberInput(
            member_id=member_id, section=sec, material=mat,
            L=L, lb=lb, N=N, Mx=Mx, Vy=Vy, duration=duration,
        )
        result = check_member(inp)
        return result.ratio_max, result.judge, _format_result(result)
    except Exception as e:
        return 999.0, "ERROR", str(e)


@hops.component(
    "/check_box_section",
    name="CheckBoxSection",
    description="角形鋼管の許容応力度検定（令82条）",
    inputs=[
        hs.HopsString("部材ID", "ID", "部材の識別名"),
        hs.HopsString("断面名", "Sec", "断面名 例: □-300x300x12"),
        hs.HopsString("材種", "Type", "材種 bcr295/bcp235/bcp325"),
        hs.HopsString("鋼材名", "Mat", "鋼材名 例: BCR295"),
        hs.HopsNumber("部材長", "L", "部材長さ (mm)"),
        hs.HopsNumber("軸力", "N", "軸力 (N) 引張+/圧縮-"),
        hs.HopsNumber("曲げモーメント", "Mx", "曲げモーメント (N·mm)"),
        hs.HopsNumber("せん断力", "Vy", "せん断力 (N)"),
        hs.HopsString("荷重期間", "Dur", "long or short", default="long"),
    ],
    outputs=[
        hs.HopsNumber("検定比", "Ratio", "最大検定比"),
        hs.HopsString("判定", "Judge", "OK or NG"),
        hs.HopsString("詳細", "Detail", "検定結果の詳細"),
    ],
)
def check_box_section(member_id, sec_name, mat_type, mat_name, L, N, Mx, Vy, duration):
    err = _validate_material_name(mat_name)
    if err:
        return 999.0, "ERROR", err
    valid_types = ("bcr295", "bcp235", "bcp325")
    if mat_type.lower() not in valid_types:
        return 999.0, "ERROR", (
            f"材種 '{mat_type}' は未対応です。\n"
            f"利用可能: {', '.join(valid_types)}"
        )
    try:
        sec = get_box_section(sec_name, mat_type)
        mat = get_material(mat_name)
        inp = MemberInput(
            member_id=member_id, section=sec, material=mat,
            L=L, lb=L, N=N, Mx=Mx, Vy=Vy, duration=duration,
        )
        result = check_member(inp)
        return result.ratio_max, result.judge, _format_result(result)
    except Exception as e:
        return 999.0, "ERROR", str(e)


# ============================================================
# レポート生成エンドポイント（REST API — Hopsではなく直接Flask）
# ============================================================


@app.route("/generate_report", methods=["POST"])
def generate_report_endpoint():
    """検定結果JSONを受け取りXLSXをbase64で返す

    リクエストJSON:
      {
        "results": [CheckResultのdict, ...],
        "project_name": "プロジェクト名",
        "author": "作成者"
      }

    レスポンスJSON:
      {
        "xlsx_base64": "base64エンコードされたXLSXデータ",
        "filename": "report_YYYYMMDD_HHMMSS.xlsx"
      }
    """
    try:
        data = request.get_json()
        if not data or "results" not in data:
            return jsonify({"error": "リクエストに 'results' が必要です"}), 400

        # CheckResult を再構築
        check_results = []
        for r in data["results"]:
            check_results.append(CheckResult(**r))

        if not check_results:
            return jsonify({"error": "検定結果が空です"}), 400

        project_name = data.get("project_name", "")
        author = data.get("author", "")

        # 一時ファイルに出力
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"report_{timestamp}.xlsx"

        with tempfile.NamedTemporaryFile(suffix=".xlsx", delete=False) as f:
            tmp_path = f.name

        try:
            generate_report(check_results, tmp_path, project_name, author)
            with open(tmp_path, "rb") as f:
                xlsx_bytes = f.read()
            xlsx_b64 = base64.b64encode(xlsx_bytes).decode("ascii")
        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)

        return jsonify({
            "xlsx_base64": xlsx_b64,
            "filename": filename,
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    print("jp_struct Hops Server 起動中...")
    print("エンドポイント:")
    print("  /check_h_section   — 圧延H形鋼")
    print("  /check_bh_section  — BH断面")
    print("  /check_box_section — 角形鋼管")
    print("  /generate_report   — XLSX生成 (POST, JSON → base64)")
    app.run(host="localhost", port=5000, debug=True)
