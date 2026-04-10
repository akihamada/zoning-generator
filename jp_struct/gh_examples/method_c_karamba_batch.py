"""
==========================================================
方法C: Karamba3D 一括検定 + 色分け表示 + XLSX出力
==========================================================

■ GH キャンバスの構成:

  ┌───────────────────────────────────────────────────────────────────────┐
  │                                                                       │
  │  ┌──────────┐   ┌──────────┐   ┌──────────┐                          │
  │  │ Geometry │──▶│ Karamba  │──▶│ Karamba  │                          │
  │  │ (Line等) │   │ Assemble │   │ Analyze  │                          │
  │  └──────────┘   │ Model    │   │          │                          │
  │                 └──────────┘   └────┬─────┘                          │
  │                                     │                                 │
  │                              ┌──────▼──────┐                          │
  │                              │ BeamForces  │                          │
  │                              │  N (kN)     │                          │
  │                              │  M (kN·m)   │                          │
  │                              │  V (kN)     │                          │
  │                              └──────┬──────┘                          │
  │                                     │                                 │
  │  ┌──────────┐                ┌──────▼──────────────────┐              │
  │  │ Panel    │──▶ sec_names   │                         │              │
  │  │ リスト   │──▶ lb_vals     │   GH Python Script      │              │
  │  │          │                │   (このスクリプト)       │              │
  │  ├──────────┤                │                         │──▶ ratios    │
  │  │ Panel    │──▶ mat_name    │   入力:                 │──▶ judges    │
  │  │"SN400B"  │                │     ids, sec_names,     │──▶ colors    │──▶ Custom Preview
  │  ├──────────┤                │     lengths, lb_vals,   │──▶ details   │──▶ Panel
  │  │ Toggle   │──▶ export_xlsx │     N_list, M_list,     │──▶ summary   │──▶ Panel
  │  │          │                │     V_list, mat_name,   │──▶ ng_count  │──▶ Wallacei
  │  ├──────────┤                │     export_xlsx,        │──▶ max_ratio │──▶ Wallacei
  │  │ Panel    │──▶ xlsx_path   │     xlsx_path           │              │
  │  │ ファイル │                │                         │              │
  │  └──────────┘                └─────────────────────────┘              │
  │                                                                       │
  │  ■ Custom Preview の接続:                                             │
  │    G (Geometry) ← Karamba の Line または ModelView の Mesh             │
  │    S (Shader)   ← colors 出力                                        │
  │                                                                       │
  │  ■ Wallacei 最適化:                                                   │
  │    目的関数1: ng_count   → 最小化                                     │
  │    目的関数2: max_ratio  → 最小化                                     │
  │    目的関数3: (任意) 総重量 → 最小化                                  │
  └───────────────────────────────────────────────────────────────────────┘

■ 入力端子の Type Hint 設定:

  ids          : list[str]     Karamba Element ID     (List Access)
  sec_names    : list[str]     断面名リスト           (List Access)
  lengths      : list[float]   部材長 mm              (List Access)
  lb_vals      : list[float]   横補剛間距離 mm        (List Access)
  N_list       : list[float]   軸力 kN               (List Access)
  M_list       : list[float]   曲げモーメント kN·m    (List Access)
  V_list       : list[float]   せん断力 kN            (List Access)
  mat_name     : str           鋼材名 "SN400B"       (Item Access)
  export_xlsx  : bool          XLSX出力するか         (Item Access)
  xlsx_path    : str           出力パス               (Item Access)

  ※ ids 〜 V_list は全て同じ長さのリスト（部材数分）

■ Karamba3D からの接続:

  「Beam Forces」コンポーネントの出力:
    N → N_list (軸力 kN)     ※符号: 引張+/圧縮-
    M → M_list (曲げ kN·m)   ※各部材の最大値を取る場合は Abs + Maximum
    V → V_list (せん断 kN)   ※同上

  「Element IDs」→ ids
  「Cross Section Names」→ sec_names
  「Element Lengths」→ lengths (mm注意、Karamba は m の場合 ×1000 必要)

  横補剛間距離 lb は Karamba から直接取れないため、
  別途 Panel/Slider で指定するか、部材長と同じにする。
"""

# ============================================================
# ここから GH Python Script にコピペ
# ============================================================

import sys
import System.Drawing as sd

# ★★★ jp_struct のパスを自分の環境に合わせて変更 ★★★
sys.path.append(r"C:\Users\aki\tools\jp_struct")

from jp_struct.sections import (
    get_h_section, get_bh_section, get_box_section, get_material
)
from jp_struct.check import MemberInput, check_member


# --- 断面の自動判別 ---
def _get_section(name, mat_name):
    """断面名のプレフィクスで断面タイプを自動判別"""
    if name.startswith("BH-"):
        return get_bh_section(name)
    elif name.startswith("□-") or name.startswith("BOX-"):
        type_map = {
            "BCR295": "bcr295", "BCP235": "bcp235", "BCP325": "bcp325",
            "STKR400": "bcr295", "STKR490": "bcp325",
        }
        return get_box_section(name, type_map.get(mat_name, "bcr295"))
    else:
        return get_h_section(name)


# --- 検定比 → 色変換 ---
def _ratio_to_color(r):
    """
    検定比に応じた色を返す
      > 1.0  赤   NG（部材サイズアップが必要）
      > 0.9  黄   注意（余裕が少ない）
      > 0.7  緑   OK
      ≤ 0.7  青   余裕あり（部材サイズダウン検討可）
    """
    if r > 1.0:
        return sd.Color.FromArgb(255, 80, 80)
    elif r > 0.9:
        return sd.Color.FromArgb(255, 220, 50)
    elif r > 0.7:
        return sd.Color.FromArgb(100, 220, 100)
    else:
        return sd.Color.FromArgb(80, 160, 255)


# ============================================================
# メイン処理
# ============================================================

mat = get_material(mat_name)
n_members = len(ids)

# 出力リスト
ratios = []
judges = []
colors = []
details = []
check_results = []  # XLSX用

for i in range(n_members):
    sec = _get_section(sec_names[i], mat_name)

    # 単位変換: kN → N, kN·m → N·mm
    inp = MemberInput(
        member_id=ids[i],
        section=sec,
        material=mat,
        L=lengths[i],
        lb=lb_vals[i],
        N=N_list[i] * 1000.0,
        Mx=abs(M_list[i]) * 1e6,    # 最大曲げは絶対値
        Vy=abs(V_list[i]) * 1000.0,  # 同上
        duration="long",
    )

    r = check_member(inp)
    check_results.append(r)

    ratios.append(r.ratio_max)
    judges.append(r.judge)
    colors.append(_ratio_to_color(r.ratio_max))
    details.append(
        f"{r.member_id}: {r.section_name} "
        f"ratio={r.ratio_max:.3f} {r.judge} "
        f"(σb/fb={r.sigma_b:.0f}/{r.fb:.0f})"
    )


# --- 集計 ---
ng_count = sum(1 for j in judges if j == "NG")
ok_count = n_members - ng_count
max_ratio = max(ratios) if ratios else 0
avg_ratio = sum(ratios) / len(ratios) if ratios else 0

summary = "\n".join([
    f"=== 検定結果サマリ ({n_members} 部材) ===",
    f"OK: {ok_count}  NG: {ng_count}",
    f"最大検定比: {max_ratio:.3f}",
    f"平均検定比: {avg_ratio:.3f}",
    f"",
    f"色の凡例:",
    f"  赤 = NG (>1.0)   黄 = 注意 (>0.9)",
    f"  緑 = OK (>0.7)   青 = 余裕 (≤0.7)",
])


# --- XLSX出力 ---
if export_xlsx and xlsx_path:
    from jp_struct.report import generate_report
    generate_report(
        check_results,
        xlsx_path,
        project_name="Grasshopper Structural Check",
        author="AHA",
    )
    summary += f"\n\nXLSX出力: {xlsx_path}"

# ============================================================
# ここまで
# ============================================================
