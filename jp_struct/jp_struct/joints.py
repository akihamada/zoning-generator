"""
接合部検定モジュール — 高力ボルト摩擦接合 + 溶接接合

出典:
  - 建築基準法施行令 第68条（高力ボルト接合）
  - 建築基準法施行令 第92条（溶接）
  - JIS B 1186（摩擦接合用高力六角ボルト・六角ナット・平座金のセット）
  - 鋼構造接合部設計指針（日本建築学会, 2012）
  - 鋼構造設計規準 — 許容応力度設計法（日本建築学会, 2005/2019）

単位: N, mm, N/mm²
"""

from dataclasses import dataclass
from typing import Optional
import json
import math
import os

_DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")


# ============================================================
# データ構造
# ============================================================


@dataclass(frozen=True)
class BoltSpec:
    """高力ボルトの仕様

    出典: JIS B 1186 (F10T), 鋼構造接合部設計指針 表2.1

    Attributes:
        grade:         等級 ("F10T")
        size:          呼び径 ("M16", "M20", "M22", "M24")
        d:             呼び径 (mm)
        d_hole:        標準孔径 (mm) — 摩擦接合: d + 2mm
        Ab:            軸断面積 (mm²)
        Ae:            有効断面積 (ねじ部, mm²)
        N0:            設計ボルト張力 (N) — ≈ 0.75 × σB × Ae
        mu:            すべり係数 (標準: 0.45)
        e_min_sheared: 最小縁端距離・せん断縁 (mm)
        e_min_rolled:  最小縁端距離・圧延縁/切断縁 (mm)
        p_min:         最小ボルト間隔 (mm) — 2.5d
    """

    grade: str
    size: str
    d: float
    d_hole: float
    Ab: float
    Ae: float
    N0: float
    mu: float
    e_min_sheared: float
    e_min_rolled: float
    p_min: float


@dataclass
class BoltJointInput:
    """ボルト接合部の検定入力

    Attributes:
        joint_id:       接合部ID
        bolt_spec:      ボルト仕様
        n_bolts:        ボルト本数
        n_friction:     摩擦面数 (1 or 2)
        Q:              作用せん断力 (N)
        T:              作用外力による引張力 (N) — ボルト軸方向
        edge_dist:      実際の縁端距離 (mm) — 最小値
        bolt_pitch:     実際のボルト間隔 (mm) — 最小値
        edge_type:      縁端の種類 ("sheared" or "rolled")
        duration:       "long" or "short"
    """

    joint_id: str
    bolt_spec: BoltSpec
    n_bolts: int
    n_friction: int = 1
    Q: float = 0.0
    T: float = 0.0
    edge_dist: float = 0.0
    bolt_pitch: float = 0.0
    edge_type: str = "rolled"
    duration: str = "long"


@dataclass
class BoltJointResult:
    """ボルト接合部の検定結果

    Attributes:
        joint_id:          接合部ID
        bolt_size:         ボルトサイズ
        n_bolts:           ボルト本数
        Qa_per_bolt:       1本あたり許容せん断力 (N)
        Qa_total:          全ボルト許容せん断力 (N)
        Ta_per_bolt:       1本あたり許容引張力 (N)
        ratio_shear:       せん断検定比
        ratio_tension:     引張検定比
        ratio_combined:    組合せ検定比
        ratio_max:         最大検定比
        edge_ok:           縁端距離 OK
        pitch_ok:          ボルト間隔 OK
        judge:             判定 ("OK" or "NG")
        messages:          注意事項・NG理由
    """

    joint_id: str
    bolt_size: str
    n_bolts: int
    Qa_per_bolt: float = 0.0
    Qa_total: float = 0.0
    Ta_per_bolt: float = 0.0
    ratio_shear: float = 0.0
    ratio_tension: float = 0.0
    ratio_combined: float = 0.0
    ratio_max: float = 0.0
    edge_ok: bool = True
    pitch_ok: bool = True
    judge: str = ""
    messages: list = None

    def __post_init__(self):
        if self.messages is None:
            self.messages = []


@dataclass
class FilletWeldInput:
    """隅肉溶接の検定入力

    Attributes:
        joint_id:    接合部ID
        s:           脚長 (mm)
        L_total:     溶接全長 (mm)
        F:           母材の基準強度 (N/mm²)
        Q:           作用せん断力 (N) — 溶接線方向
        duration:    "long" or "short"
    """

    joint_id: str
    s: float
    L_total: float
    F: float
    Q: float = 0.0
    duration: str = "long"


@dataclass
class FilletWeldResult:
    """隅肉溶接の検定結果

    Attributes:
        joint_id:      接合部ID
        s:             脚長 (mm)
        a:             のど厚 (mm) = 0.7 × s
        L_eff:         有効長さ (mm) = L_total − 2s
        fw:            溶接許容応力度 (N/mm²)
        Qa:            許容耐力 (N)
        ratio:         検定比
        judge:         判定
        messages:      注意事項
    """

    joint_id: str
    s: float = 0.0
    a: float = 0.0
    L_eff: float = 0.0
    fw: float = 0.0
    Qa: float = 0.0
    ratio: float = 0.0
    judge: str = ""
    messages: list = None

    def __post_init__(self):
        if self.messages is None:
            self.messages = []


# ============================================================
# データベースローダ
# ============================================================


def load_bolt_specs() -> list[BoltSpec]:
    """高力ボルトデータベースを読み込む

    出典: JIS B 1186, 鋼構造接合部設計指針 表2.1
    """
    filepath = os.path.join(_DATA_DIR, "hsfg_bolts.json")
    with open(filepath, "r", encoding="utf-8") as f:
        raw = json.load(f)
    return [BoltSpec(**d) for d in raw]


def get_bolt_spec(size: str, grade: str = "F10T") -> BoltSpec:
    """サイズと等級でボルト仕様を検索"""
    for b in load_bolt_specs():
        if b.size == size and b.grade == grade:
            return b
    raise ValueError(f"ボルト {grade} {size} が見つかりません")


# ============================================================
# 高力ボルト摩擦接合の検定
# ============================================================


def check_bolt_joint(inp: BoltJointInput) -> BoltJointResult:
    """高力ボルト摩擦接合の検定

    出典:
      - 令68条（高力ボルト接合）
      - 鋼構造接合部設計指針（日本建築学会, 2012）2.2節〜2.4節

    許容せん断力（1本1面あたり, 長期）:
      Qa1 = μ × N0 / 1.5
      ここで μ = すべり係数（標準 0.45）, N0 = 設計ボルト張力

    許容引張力（1本あたり, 長期）:
      Ta = N0 / 1.5

    組合せ応力（せん断＋引張）:
      (Q/Qa)² + (T/Ta)² ≤ 1.0
      出典: 鋼構造接合部設計指針 式(2.4)

    Parameters:
        inp: BoltJointInput

    Returns:
        BoltJointResult
    """
    bolt = inp.bolt_spec
    msgs = []

    duration_factor = 1.5 if inp.duration == "short" else 1.0

    # --- 許容せん断力 ---
    # 1本1面あたりの長期許容せん断力
    Qa1_long = bolt.mu * bolt.N0 / 1.5
    # n面摩擦
    Qa_per_bolt = Qa1_long * inp.n_friction * duration_factor
    Qa_total = Qa_per_bolt * inp.n_bolts

    # --- 許容引張力 ---
    # 外力による引張に対する許容値
    # 出典: 鋼構造接合部設計指針 2.3節
    Ta_per_bolt = bolt.N0 / 1.5 * duration_factor

    # --- 検定比 ---
    Q_per_bolt = abs(inp.Q) / inp.n_bolts if inp.n_bolts > 0 else 0
    T_per_bolt = abs(inp.T) / inp.n_bolts if inp.n_bolts > 0 else 0

    ratio_shear = Q_per_bolt / Qa_per_bolt if Qa_per_bolt > 0 else 0
    ratio_tension = T_per_bolt / Ta_per_bolt if Ta_per_bolt > 0 else 0

    # 組合せ（せん断＋引張の二乗和）
    # 出典: 鋼構造接合部設計指針 式(2.4)
    ratio_combined = math.sqrt(ratio_shear**2 + ratio_tension**2)

    ratio_max = ratio_combined

    # --- 縁端距離チェック ---
    edge_ok = True
    if inp.edge_dist > 0:
        if inp.edge_type == "sheared":
            e_min = bolt.e_min_sheared
        else:
            e_min = bolt.e_min_rolled
        if inp.edge_dist < e_min:
            edge_ok = False
            msgs.append(
                f"縁端距離不足: {inp.edge_dist}mm < {e_min}mm "
                f"({inp.edge_type}縁)"
            )

    # --- ボルト間隔チェック ---
    pitch_ok = True
    if inp.bolt_pitch > 0:
        if inp.bolt_pitch < bolt.p_min:
            pitch_ok = False
            msgs.append(
                f"ボルト間隔不足: {inp.bolt_pitch}mm < {bolt.p_min}mm"
            )

    # --- 判定 ---
    if not edge_ok or not pitch_ok:
        ratio_max = max(ratio_max, 999)  # 配置NGは強制NG
    judge = "OK" if ratio_max <= 1.0 else "NG"

    return BoltJointResult(
        joint_id=inp.joint_id,
        bolt_size=bolt.size,
        n_bolts=inp.n_bolts,
        Qa_per_bolt=round(Qa_per_bolt, 1),
        Qa_total=round(Qa_total, 1),
        Ta_per_bolt=round(Ta_per_bolt, 1),
        ratio_shear=round(ratio_shear, 4),
        ratio_tension=round(ratio_tension, 4),
        ratio_combined=round(ratio_combined, 4),
        ratio_max=round(ratio_max, 4),
        edge_ok=edge_ok,
        pitch_ok=pitch_ok,
        judge=judge,
        messages=msgs,
    )


# ============================================================
# 隅肉溶接の検定
# ============================================================


def check_fillet_weld(inp: FilletWeldInput) -> FilletWeldResult:
    """隅肉溶接の検定

    出典:
      - 令92条（溶接の許容応力度）
      - 鋼構造設計規準 7.2節
      - 鋼構造接合部設計指針 3.2節

    のど厚:
      a = 0.7 × s
      出典: 鋼構造設計規準 7.2.1

    有効長さ:
      L_eff = L_total − 2s
      始終端のクレータを控除する。
      出典: 鋼構造設計規準 7.2.2

    溶接許容せん断応力度（長期）:
      fw = F / (√3 × 1.5)
      出典: 令92条 — 溶接部は母材のせん断許容応力度と同等

    許容耐力:
      Qa = a × L_eff × fw

    Parameters:
        inp: FilletWeldInput

    Returns:
        FilletWeldResult
    """
    msgs = []

    # のど厚
    a = 0.7 * inp.s

    # 有効長さ（始終端クレータ控除）
    L_eff = inp.L_total - 2 * inp.s

    # 有効長さの最小値チェック
    # 出典: 鋼構造設計規準 7.2.2
    L_eff_min = max(10 * inp.s, 40)
    if L_eff < L_eff_min:
        msgs.append(
            f"有効長さ不足: L_eff={L_eff:.1f}mm < "
            f"min({10*inp.s:.0f}, 40)={L_eff_min:.0f}mm"
        )

    # 脚長の最小値チェック
    if inp.s < 4:
        msgs.append(f"脚長が小さい: s={inp.s}mm (推奨 ≥ 4mm)")

    duration_factor = 1.5 if inp.duration == "short" else 1.0

    # 溶接許容応力度
    # 出典: 令92条 — fw = F / (√3 × 1.5) (長期)
    fw = inp.F / (math.sqrt(3) * 1.5) * duration_factor

    # 許容耐力
    Qa = a * max(L_eff, 0) * fw

    # 検定比
    ratio = abs(inp.Q) / Qa if Qa > 0 else 999
    judge = "OK" if ratio <= 1.0 and not msgs else ("NG" if ratio > 1.0 else "OK*")

    return FilletWeldResult(
        joint_id=inp.joint_id,
        s=inp.s,
        a=round(a, 2),
        L_eff=round(L_eff, 1),
        fw=round(fw, 2),
        Qa=round(Qa, 1),
        ratio=round(ratio, 4),
        judge=judge,
        messages=msgs,
    )


# ============================================================
# 突合せ溶接（完全溶込み）
# ============================================================


def check_groove_weld_note() -> str:
    """突合せ溶接（完全溶込み）に関する注記

    完全溶込み突合せ溶接は母材と同等の強度を持つとみなす。
    したがって、溶接部単独の検定は不要であり、
    母材（部材）の検定をもって接合部の検定とする。

    出典: 鋼構造設計規準 7.3節
          「完全溶込みグルーブ溶接は、溶接金属の引張強さが
           母材のそれ以上であれば、母材と同等とみなしてよい。」
    """
    return (
        "完全溶込み突合せ溶接は母材と同等として扱う。"
        "母材の部材検定をもって接合部の検定とする。"
        "（出典: 鋼構造設計規準 7.3節）"
    )
