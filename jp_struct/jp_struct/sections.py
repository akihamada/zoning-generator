"""
断面データベースローダ + dataclass 定義

出典:
  - JIS G 3192（熱間圧延H形鋼の形状・寸法・質量及びその許容差）
  - JIS G 3466（一般構造用角形鋼管）
  - JIS G 3101, JIS G 3136（鋼材規格）
  - 国土交通大臣認定（BCR295, BCP235, BCP325）

単位: N, mm, N/mm²
"""

from dataclasses import dataclass
from typing import Optional
import json
import os
import math

# --- データファイルのパス ---
_DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")


# ============================================================
# dataclass 定義
# ============================================================


@dataclass(frozen=True)
class HSection:
    """圧延H形鋼の断面諸元

    出典: JIS G 3192
    """

    name: str
    H: float  # 梁せい (mm)
    B: float  # フランジ幅 (mm)
    tw: float  # ウェブ厚 (mm)
    tf: float  # フランジ厚 (mm)
    r: float  # フィレット半径 (mm)
    A: float  # 断面積 (mm²)
    Ix: float  # 強軸断面二次モーメント (mm⁴)
    Iy: float  # 弱軸断面二次モーメント (mm⁴)
    Zx: float  # 強軸断面係数 (mm³)
    Zy: float  # 弱軸断面係数 (mm³)
    ix: float  # 強軸断面二次半径 (mm)
    iy: float  # 弱軸断面二次半径 (mm)

    @property
    def hw(self) -> float:
        """ウェブ高さ = H - 2tf (mm)"""
        return self.H - 2 * self.tf

    @property
    def Af(self) -> float:
        """圧縮フランジ面積 = B × tf (mm²)"""
        return self.B * self.tf

    @property
    def section_type(self) -> str:
        return "H"


@dataclass(frozen=True)
class BHSection:
    """ビルトアップH形鋼（溶接組立H形鋼）の断面諸元

    圧延H形鋼と異なりフィレット（R部）が無い。
    断面性能は板厚のみから計算される。
    """

    name: str
    H: float  # 梁せい (mm)
    B: float  # フランジ幅 (mm)
    tw: float  # ウェブ厚 (mm)
    tf: float  # フランジ厚 (mm)
    A: float  # 断面積 (mm²)
    Ix: float  # 強軸断面二次モーメント (mm⁴)
    Iy: float  # 弱軸断面二次モーメント (mm⁴)
    Zx: float  # 強軸断面係数 (mm³)
    Zy: float  # 弱軸断面係数 (mm³)
    ix: float  # 強軸断面二次半径 (mm)
    iy: float  # 弱軸断面二次半径 (mm)

    @property
    def hw(self) -> float:
        """ウェブ高さ = H - 2tf (mm)"""
        return self.H - 2 * self.tf

    @property
    def Af(self) -> float:
        """圧縮フランジ面積 = B × tf (mm²)"""
        return self.B * self.tf

    @property
    def r(self) -> float:
        """BHにはフィレットなし"""
        return 0.0

    @property
    def section_type(self) -> str:
        return "BH"


@dataclass(frozen=True)
class BoxSection:
    """角形鋼管（正方形）の断面諸元

    出典: JIS G 3466, 国土交通大臣認定（BCR/BCP）

    角R（コーナー半径）は無視した計算値。
    実製品は冷間成形による角Rがあるため、実断面積はやや小さい。
    """

    name: str
    B: float  # 辺長 (mm) ※正方形断面
    t: float  # 板厚 (mm)
    A: float  # 断面積 (mm²)
    Ix: float  # 断面二次モーメント (mm⁴)
    Iy: float  # 断面二次モーメント (mm⁴) ※正方形なので Ix = Iy
    Zx: float  # 断面係数 (mm³)
    Zy: float  # 断面係数 (mm³)
    ix: float  # 断面二次半径 (mm)
    iy: float  # 断面二次半径 (mm)

    @property
    def section_type(self) -> str:
        return "BOX"


@dataclass(frozen=True)
class SteelMaterial:
    """鋼材の材料特性

    出典: JIS G 3101 (SS400), JIS G 3136 (SN400/490),
          国土交通大臣認定 (BCR295, BCP235, BCP325),
          JIS G 3466 (STKR400/490)
    """

    name: str
    standard: str
    F_by_thickness: list  # [{"t_max": mm, "F": N/mm²}, ...]
    E: float  # ヤング係数 (N/mm²) — 鋼材共通 205,000
    G: float  # せん断弾性係数 (N/mm²) — 鋼材共通 79,000
    density: float  # 密度 (kg/m³)
    note: str


# ============================================================
# BH断面の性能計算ユーティリティ
# ============================================================


def calc_bh_properties(H: float, B: float, tw: float, tf: float) -> dict:
    """BH断面の断面性能を寸法から計算する（フィレット無し）

    Parameters:
        H:  梁せい (mm)
        B:  フランジ幅 (mm)
        tw: ウェブ厚 (mm)
        tf: フランジ厚 (mm)

    Returns:
        dict: A, Ix, Iy, Zx, Zy, ix, iy
    """
    hw = H - 2 * tf
    A = 2 * B * tf + hw * tw
    Ix = tw * hw**3 / 12 + 2 * (B * tf**3 / 12 + B * tf * ((H - tf) / 2) ** 2)
    Iy = 2 * tf * B**3 / 12 + hw * tw**3 / 12
    Zx = Ix / (H / 2)
    Zy = Iy / (B / 2)
    ix = math.sqrt(Ix / A)
    iy = math.sqrt(Iy / A)
    return {"A": A, "Ix": Ix, "Iy": Iy, "Zx": Zx, "Zy": Zy, "ix": ix, "iy": iy}


# ============================================================
# データベースローダ
# ============================================================


def _load_json(filename: str) -> list:
    """data/ ディレクトリからJSONを読み込む"""
    filepath = os.path.join(_DATA_DIR, filename)
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)


def load_h_sections() -> list[HSection]:
    """JIS H形鋼データベースを読み込む"""
    raw = _load_json("jis_g3192_h.json")
    return [HSection(**d) for d in raw]


def load_bh_sections() -> list[BHSection]:
    """BH（溶接組立H形鋼）データベースを読み込む"""
    raw = _load_json("bh_sections.json")
    return [BHSection(**d) for d in raw]


def load_box_sections(material_type: str = "bcr295") -> list[BoxSection]:
    """角形鋼管データベースを読み込む

    Parameters:
        material_type: "bcr295", "bcp235", "bcp325" のいずれか
    """
    filename_map = {
        "bcr295": "bcr295.json",
        "bcp235": "bcp235.json",
        "bcp325": "bcp325.json",
    }
    filename = filename_map.get(material_type.lower())
    if filename is None:
        raise ValueError(
            f"未対応の材種: {material_type}。"
            f"対応: {list(filename_map.keys())}"
        )
    raw = _load_json(filename)
    return [BoxSection(**d) for d in raw]


def load_materials() -> list[SteelMaterial]:
    """鋼材データベースを読み込む"""
    raw = _load_json("steel_materials.json")
    results = []
    for d in raw:
        results.append(
            SteelMaterial(
                name=d["name"],
                standard=d["standard"],
                F_by_thickness=d["F_by_thickness"],
                E=d["E"],
                G=d["G"],
                density=d["density"],
                note=d["note"],
            )
        )
    return results


# ============================================================
# 便利関数（名前引き）
# ============================================================


def get_h_section(name: str) -> HSection:
    """名前でH形鋼を検索"""
    for s in load_h_sections():
        if s.name == name:
            return s
    raise ValueError(f"H形鋼 '{name}' が見つかりません")


def get_bh_section(name: str) -> BHSection:
    """名前でBH断面を検索"""
    for s in load_bh_sections():
        if s.name == name:
            return s
    raise ValueError(f"BH断面 '{name}' が見つかりません")


def get_box_section(name: str, material_type: str = "bcr295") -> BoxSection:
    """名前で角形鋼管を検索"""
    for s in load_box_sections(material_type):
        if s.name == name:
            return s
    raise ValueError(f"角形鋼管 '{name}' が見つかりません (材種: {material_type})")


def get_material(name: str) -> SteelMaterial:
    """名前で鋼材を検索"""
    for m in load_materials():
        if m.name == name:
            return m
    raise ValueError(f"鋼材 '{name}' が見つかりません")


def get_F(material: SteelMaterial, t: float) -> float:
    """板厚に応じた基準強度 F (N/mm²) を返す

    出典: JIS G 3101 表2, JIS G 3136 表2, 各認定書

    Parameters:
        material: 鋼材データ
        t: 板厚 (mm) — フランジ厚を想定

    Returns:
        F: 基準強度 (N/mm²)

    Raises:
        ValueError: 板厚が全ての範囲を超える場合
    """
    for entry in material.F_by_thickness:
        if t <= entry["t_max"]:
            return float(entry["F"])
    raise ValueError(
        f"鋼材 '{material.name}' の板厚 {t}mm に対応する基準強度がありません。"
        f"最大対応板厚: {material.F_by_thickness[-1]['t_max']}mm"
    )
