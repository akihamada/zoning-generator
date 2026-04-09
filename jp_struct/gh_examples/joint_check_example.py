"""
接合部検定サンプル — Grasshopper Python コンポーネント用

高力ボルト摩擦接合と隅肉溶接の検定例。
"""

import sys
# sys.path.append(r"C:\path\to\jp_struct")

from jp_struct.joints import (
    get_bolt_spec,
    BoltJointInput,
    check_bolt_joint,
    FilletWeldInput,
    check_fillet_weld,
    check_groove_weld_note,
)

# ============================================================
# 例1: 高力ボルト摩擦接合（梁フランジ継手）
# ============================================================

bolt = get_bolt_spec("M20")  # F10T M20

inp_bolt = BoltJointInput(
    joint_id="J1-flange",
    bolt_spec=bolt,
    n_bolts=6,           # 6本（3行×2列）
    n_friction=2,        # 2面摩擦（スプライスプレート両面）
    Q=300e3,             # せん断力 300 kN
    T=0,                 # 引張なし
    edge_dist=30,        # 縁端距離 30mm
    bolt_pitch=60,       # ボルト間隔 60mm
    edge_type="rolled",  # 圧延縁
    duration="long",
)

result_bolt = check_bolt_joint(inp_bolt)
print(f"=== ボルト接合 {result_bolt.joint_id} ===")
print(f"  {result_bolt.bolt_size} × {result_bolt.n_bolts} 本, 2面摩擦")
print(f"  許容せん断力 = {result_bolt.Qa_total/1000:.1f} kN")
print(f"  検定比 = {result_bolt.ratio_max:.4f}")
print(f"  判定: {result_bolt.judge}")
if result_bolt.messages:
    for msg in result_bolt.messages:
        print(f"  注意: {msg}")

# ============================================================
# 例2: 隅肉溶接（ウェブ接合）
# ============================================================

inp_weld = FilletWeldInput(
    joint_id="J1-web-weld",
    s=6,              # 脚長 6mm
    L_total=200,      # 溶接全長 200mm
    F=235,            # 母材 SS400
    Q=120e3,          # せん断力 120 kN
    duration="long",
)

result_weld = check_fillet_weld(inp_weld)
print(f"\n=== 隅肉溶接 {result_weld.joint_id} ===")
print(f"  脚長 s={result_weld.s}mm, のど厚 a={result_weld.a}mm")
print(f"  有効長さ L_eff={result_weld.L_eff}mm")
print(f"  許容耐力 = {result_weld.Qa/1000:.1f} kN")
print(f"  検定比 = {result_weld.ratio:.4f}")
print(f"  判定: {result_weld.judge}")

# ============================================================
# 例3: 完全溶込み突合せ溶接
# ============================================================

print(f"\n=== 突合せ溶接 ===")
print(f"  {check_groove_weld_note()}")
