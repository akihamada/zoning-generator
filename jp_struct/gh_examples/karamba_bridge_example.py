"""
Karamba3D → jp_struct ブリッジ サンプル

Karamba3D の解析結果（断面力）を jp_struct の検定入力に変換する例。
GH 上の Python Script コンポーネントで使用する。

前提:
  - Karamba3D の ModelView / BeamForces コンポーネントで
    各部材の断面力 (N, Mx, Vy) を取得済み
  - 単位変換: Karamba3D は kN/kNm 系 → jp_struct は N/Nmm 系

使い方:
  入力端子:
    karamba_ids:    List[str]  部材ID列
    karamba_N:      List[float]  軸力 (kN)
    karamba_Mx:     List[float]  曲げモーメント (kN·m)
    karamba_Vy:     List[float]  せん断力 (kN)
    section_names:  List[str]  断面名（H形鋼）
    member_lengths: List[float]  部材長 (mm)
    lb_values:      List[float]  横補剛間距離 (mm)

  出力端子:
    ratios:  List[float]  検定比
    judges:  List[str]    判定
    details: List[str]    詳細
"""

import sys
# sys.path.append(r"C:\path\to\jp_struct")

from jp_struct.sections import get_h_section, get_material
from jp_struct.check import MemberInput, check_member

# --- 単位変換 (kN/kNm → N/Nmm) ---
kN_to_N = 1000.0
kNm_to_Nmm = 1e6

mat = get_material("SN400B")

ratios = []
judges = []
details = []

for i in range(len(karamba_ids)):
    sec = get_h_section(section_names[i])

    # Karamba3D の値を SI に変換
    N_si = karamba_N[i] * kN_to_N
    Mx_si = karamba_Mx[i] * kNm_to_Nmm
    Vy_si = karamba_Vy[i] * kN_to_N

    inp = MemberInput(
        member_id=karamba_ids[i],
        section=sec,
        material=mat,
        L=member_lengths[i],
        lb=lb_values[i],
        N=N_si,
        Mx=Mx_si,
        Vy=Vy_si,
        duration="long",
    )

    result = check_member(inp)

    ratios.append(result.ratio_max)
    judges.append(result.judge)
    details.append(
        f"{result.member_id}: {result.section_name} "
        f"ratio={result.ratio_max:.3f} {result.judge}"
    )
