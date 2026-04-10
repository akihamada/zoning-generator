"""
==========================================================
方法A: 単一部材検定 — GH Python Script コンポーネント用
==========================================================

■ GH キャンバスの構成:

  ┌──────────┐
  │  Panel   │──▶ section_name (str)   例 "H-400x200x8x13"
  ├──────────┤
  │  Panel   │──▶ mat_name (str)       例 "SN400B"
  ├──────────┤
  │ Slider   │──▶ L (float)            部材長 mm        例 6000
  ├──────────┤
  │ Slider   │──▶ lb (float)           横補剛間距離 mm   例 3000
  ├──────────┤
  │ Slider   │──▶ N_kN (float)         軸力 kN          例 0
  ├──────────┤                                   ┌──────────────────────┐
  │ Slider   │──▶ Mx_kNm (float) ────▶│                      │
  ├──────────┤                         │   GH Python Script    │
  │ Slider   │──▶ Vy_kN (float)  ────▶│   (このスクリプト)    │
  ├──────────┤                         │                      │──▶ ratio   (float)  → Panel
  │ Toggle   │──▶ is_short (bool) ────▶│                      │──▶ judge   (str)    → Panel
  └──────────┘                         │                      │──▶ detail  (str)    → Panel
                                       │                      │──▶ color   (Colour) → Custom Preview
                                       └──────────────────────┘

■ セットアップ手順:

  1. GH に「Script」コンポーネント（Python 3）を配置
  2. 入力端子を右クリック → 名前とType Hintを以下の通り設定:
       section_name : str
       mat_name     : str
       L            : float
       lb           : float
       N_kN         : float
       Mx_kNm       : float
       Vy_kN        : float
       is_short     : bool
  3. 出力端子を追加:
       ratio  : float
       judge  : str
       detail : str
       color  : System.Drawing.Color
  4. 以下のコードを貼り付け

■ 注意:
  - sys.path の行を自分の環境に合わせて変更すること
  - 入力は全て kN / kN·m 系（Karamba3D に合わせて）
  - 内部で N / N·mm に自動変換する
"""

# ============================================================
# ここから GH Python Script にコピペ
# ============================================================

import sys
import System.Drawing as sd

# ★★★ jp_struct のパスを自分の環境に合わせて変更 ★★★
sys.path.append(r"C:\Users\aki\tools\jp_struct")

from jp_struct.sections import get_h_section, get_bh_section, get_box_section, get_material
from jp_struct.check import MemberInput, check_member

# --- 入力の受取（GHコンポーネントの入力端子） ---
# section_name : str     "H-400x200x8x13" or "BH-500x200x9x16" or "□-300x300x12"
# mat_name     : str     "SN400B", "BCR295" 等
# L            : float   部材長 (mm)
# lb           : float   横補剛間距離 (mm)
# N_kN         : float   軸力 (kN)     正=引張, 負=圧縮
# Mx_kNm       : float   曲げモーメント (kN·m)
# Vy_kN        : float   せん断力 (kN)
# is_short     : bool    True=短期, False=長期


# --- 単位変換: kN → N, kN·m → N·mm ---
N_si = N_kN * 1000.0
Mx_si = Mx_kNm * 1e6
Vy_si = Vy_kN * 1000.0

duration = "short" if is_short else "long"

# --- 断面を自動判別して取得 ---
if section_name.startswith("BH-"):
    sec = get_bh_section(section_name)
elif section_name.startswith("□-") or section_name.startswith("BOX-"):
    # 角形鋼管: 材種を材料名から推定
    mat_type_map = {
        "BCR295": "bcr295", "BCP235": "bcp235", "BCP325": "bcp325",
        "STKR400": "bcr295", "STKR490": "bcp325",
    }
    mat_type = mat_type_map.get(mat_name, "bcr295")
    sec = get_box_section(section_name, mat_type)
else:
    sec = get_h_section(section_name)

mat = get_material(mat_name)

# --- 検定実行 ---
inp = MemberInput(
    member_id="GH-Member",
    section=sec,
    material=mat,
    L=L,
    lb=lb,
    N=N_si,
    Mx=Mx_si,
    Vy=Vy_si,
    duration=duration,
)
result = check_member(inp)

# --- 出力 ---
ratio = result.ratio_max
judge = result.judge

detail = "\n".join([
    f"断面: {result.section_name} ({result.material_name})",
    f"F = {result.F} N/mm²  荷重: {result.duration}",
    f"幅厚比区分: {result.wt_rank}",
    f"─────────────────────",
    f"作用応力度     許容応力度",
    f"σc = {result.sigma_c:7.1f}   fc = {result.fc:7.1f} N/mm²",
    f"σt = {result.sigma_t:7.1f}   ft = {result.ft:7.1f} N/mm²",
    f"σb = {result.sigma_b:7.1f}   fb = {result.fb:7.1f} N/mm²",
    f"τ  = {result.tau:7.1f}   fs = {result.fs:7.1f} N/mm²",
    f"─────────────────────",
    f"細長比: λx={result.lambda_x:.1f}  λy={result.lambda_y:.1f}",
    f"検定比(組合せ) = {result.ratio_combined:.4f}",
    f"検定比(せん断) = {result.ratio_shear:.4f}",
    f"─────────────────────",
    f"最大検定比 = {result.ratio_max:.4f}",
    f"判定: {result.judge}",
])

# --- 検定比に応じた色 ---
if ratio > 1.0:
    color = sd.Color.FromArgb(255, 80, 80)      # 赤: NG
elif ratio > 0.9:
    color = sd.Color.FromArgb(255, 220, 50)      # 黄: 注意
elif ratio > 0.7:
    color = sd.Color.FromArgb(100, 220, 100)     # 緑: OK
else:
    color = sd.Color.FromArgb(80, 160, 255)      # 青: 余裕

# ============================================================
# ここまで
# ============================================================
