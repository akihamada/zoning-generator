#!/usr/bin/env python3
"""
BH（ビルトアップH形鋼 / 溶接組立H形鋼）の断面性能計算スクリプト

フィレット（R部）が無いため、板厚のみから断面性能を正確に算定できる。

使い方:
  python scripts/calc_bh_properties.py

出力: data/bh_sections.json

出典:
  断面性能の計算式は材料力学の基本式による。
  BH断面は JIS 規格外であり、設計者が任意に寸法を指定する。
  ここでは実務で多用される代表的な10サイズを収録する。
"""

import json
import math
import os

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")

# 代表的なBH断面 10種
# (name, H, B, tw, tf)
BH_SECTIONS = [
    ("BH-300x150x6x9", 300, 150, 6, 9),
    ("BH-350x175x6x9", 350, 175, 6, 9),
    ("BH-400x200x9x12", 400, 200, 9, 12),
    ("BH-400x200x9x16", 400, 200, 9, 16),
    ("BH-450x200x9x12", 450, 200, 9, 12),
    ("BH-500x200x9x16", 500, 200, 9, 16),
    ("BH-500x200x9x19", 500, 200, 9, 19),
    ("BH-600x200x12x19", 600, 200, 12, 19),
    ("BH-600x200x12x22", 600, 200, 12, 22),
    ("BH-700x250x12x25", 700, 250, 12, 25),
]


def calc_bh_props(H, B, tw, tf):
    """BH断面の断面性能を算定する

    フィレット無しのH形断面として計算。

    計算式:
      hw = H − 2tf（クリアウェブ高さ）
      A  = 2·B·tf + hw·tw
      Ix = tw·hw³/12 + 2·(B·tf³/12 + B·tf·((H−tf)/2)²)
      Iy = 2·tf·B³/12 + hw·tw³/12
      Zx = 2·Ix/H
      Zy = 2·Iy/B
      ix = √(Ix/A)
      iy = √(Iy/A)
    """
    hw = H - 2 * tf
    A = 2 * B * tf + hw * tw
    Ix = tw * hw**3 / 12 + 2 * (B * tf**3 / 12 + B * tf * ((H - tf) / 2) ** 2)
    Iy = 2 * tf * B**3 / 12 + hw * tw**3 / 12
    Zx = Ix / (H / 2)
    Zy = Iy / (B / 2)
    ix = math.sqrt(Ix / A)
    iy = math.sqrt(Iy / A)

    return {
        "A": round(A, 1),
        "Ix": round(Ix, 0),
        "Iy": round(Iy, 0),
        "Zx": round(Zx, 0),
        "Zy": round(Zy, 0),
        "ix": round(ix, 1),
        "iy": round(iy, 1),
    }


def main():
    results = []
    print("=== BH断面 断面性能一覧 ===\n")
    print(f"{'断面名':<25} {'A':>8} {'Ix':>14} {'Iy':>12} {'Zx':>10} {'Zy':>8} {'ix':>6} {'iy':>6}")
    print("-" * 95)

    for name, H, B, tw, tf in BH_SECTIONS:
        props = calc_bh_props(H, B, tw, tf)
        entry = {"name": name, "H": H, "B": B, "tw": tw, "tf": tf}
        entry.update(props)
        results.append(entry)

        print(
            f"{name:<25} {props['A']:>8.1f} {props['Ix']:>14.0f} "
            f"{props['Iy']:>12.0f} {props['Zx']:>10.0f} {props['Zy']:>8.0f} "
            f"{props['ix']:>6.1f} {props['iy']:>6.1f}"
        )

    # JSON出力
    os.makedirs(DATA_DIR, exist_ok=True)
    filepath = os.path.join(DATA_DIR, "bh_sections.json")
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    print(f"\n出力: {filepath} ({len(results)} 件)")


if __name__ == "__main__":
    main()
