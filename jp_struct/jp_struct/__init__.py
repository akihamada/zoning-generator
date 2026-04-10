"""
jp_struct — 日本建築基準法 許容応力度設計ルート 構造検定モジュール

令82条に基づくルート1〜2の許容応力度検定を行う。
Rhino8 / Grasshopper / Karamba3D との連携を想定。

出典:
  - 建築基準法施行令 第82条〜第99条
  - 2020年版 建築物の構造関係技術基準解説書（国土交通省）
  - 鋼構造設計規準 — 許容応力度設計法（日本建築学会, 2005/2019）
  - H19国交告第594号（曲げ材の許容応力度）
  - H12建告第2464号（幅厚比区分）
  - 昭55建告第1793号（圧縮材の許容応力度）

単位系: SI（N, mm, N/mm²）  内部計算は全てこの単位系で行う。
"""

__version__ = "0.4.0-alpha"

from jp_struct.sections import (
    HSection,
    BHSection,
    BoxSection,
    SteelMaterial,
    load_h_sections,
    load_bh_sections,
    load_box_sections,
    load_materials,
    get_h_section,
    get_bh_section,
    get_box_section,
    get_material,
    get_F,
)
from jp_struct.allowable import (
    calc_fc,
    calc_fb,
    calc_ft,
    calc_fs,
    width_thickness_rank_h,
    width_thickness_rank_box,
)
from jp_struct.check import MemberInput, CheckResult, check_member
from jp_struct.loads import LoadCase, LoadCombination, STANDARD_COMBINATIONS
from jp_struct.joints import (
    BoltSpec,
    BoltJointInput,
    BoltJointResult,
    FilletWeldInput,
    FilletWeldResult,
    load_bolt_specs,
    get_bolt_spec,
    check_bolt_joint,
    check_fillet_weld,
)
from jp_struct.report import generate_report
