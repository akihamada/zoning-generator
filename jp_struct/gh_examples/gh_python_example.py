"""
Grasshopper Python コンポーネント用サンプルスクリプト

GH の Python Script コンポーネント内に貼り付けて使用する。
jp_struct がインストール済み（sys.path に追加済み）であることが前提。

使い方:
  1. GH上に Python Script コンポーネントを配置
  2. 入力: section_name (str), L (float), lb (float), Mx (float), Vy (float)
  3. 出力: ratio (float), judge (str), detail (str)
"""

import sys
# Rhino8 CPython 環境で jp_struct のパスを追加
# sys.path.append(r"C:\path\to\jp_struct")

from jp_struct.sections import get_h_section, get_material
from jp_struct.check import MemberInput, check_member

# --- 入力（GHコンポーネントの入力端子から） ---
# section_name = "H-400x200x8x13"  # GH入力
# L = 6000.0        # 部材長 mm
# lb = 3000.0       # 横補剛間距離 mm
# Mx = 200e6        # 曲げモーメント N·mm (= 200 kN·m)
# Vy = 100e3        # せん断力 N (= 100 kN)

sec = get_h_section(section_name)
mat = get_material("SN400B")

inp = MemberInput(
    member_id="GH-Beam",
    section=sec,
    material=mat,
    L=L,
    lb=lb,
    N=0,
    Mx=Mx,
    Vy=Vy,
    duration="long",
)

result = check_member(inp)

# --- 出力（GHコンポーネントの出力端子へ） ---
ratio = result.ratio_max
judge = result.judge
detail = (
    f"断面: {result.section_name}\n"
    f"σb={result.sigma_b:.1f} / fb={result.fb:.1f} N/mm²\n"
    f"τ={result.tau:.1f} / fs={result.fs:.1f} N/mm²\n"
    f"検定比={result.ratio_max:.3f} {result.judge}"
)
