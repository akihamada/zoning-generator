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

依存: flask, ghhops-server
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from flask import Flask
import ghhops_server as hs

from jp_struct.sections import (
    get_h_section,
    get_bh_section,
    get_box_section,
    get_material,
)
from jp_struct.check import MemberInput, check_member

app = Flask(__name__)
hops = hs.Hops(app)


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


if __name__ == "__main__":
    print("jp_struct Hops Server 起動中...")
    print("エンドポイント:")
    print("  /check_h_section   — 圧延H形鋼")
    print("  /check_bh_section  — BH断面")
    print("  /check_box_section — 角形鋼管")
    app.run(host="localhost", port=5000, debug=True)
