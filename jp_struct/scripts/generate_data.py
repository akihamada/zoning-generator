#!/usr/bin/env python3
"""
JIS H形鋼・鋼材データベース生成スクリプト

断面性能はフィレット(R部)を含まない計算値。
圧延H形鋼の実際の断面性能は JIS G 3192 の規格表を参照のこと。
"""
import json
import math
import os

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")


def calc_h_props(H, B, tw, tf):
    """H形鋼の断面性能を計算（フィレット無視）"""
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


def calc_box_props(B, t):
    """正方形角形鋼管の断面性能を計算（角Rなし）"""
    A = B**2 - (B - 2 * t) ** 2  # = 4*t*(B - t)
    Ix = (B**4 - (B - 2 * t) ** 4) / 12
    Iy = Ix  # 正方形
    Zx = Ix / (B / 2)
    Zy = Iy / (B / 2)
    ix = math.sqrt(Ix / A)
    iy = ix
    return {
        "A": round(A, 1),
        "Ix": round(Ix, 0),
        "Iy": round(Iy, 0),
        "Zx": round(Zx, 0),
        "Zy": round(Zy, 0),
        "ix": round(ix, 1),
        "iy": round(iy, 1),
    }


# --- JIS G 3192 H形鋼 (23サイズ) ---
# (name, H, B, tw, tf, r)
JIS_H_SECTIONS = [
    ("H-100x100x6x8", 100, 100, 6, 8, 8),
    ("H-125x125x6.5x9", 125, 125, 6.5, 9, 8),
    ("H-150x75x5x7", 150, 75, 5, 7, 8),
    ("H-150x150x7x10", 150, 150, 7, 10, 8),
    ("H-175x90x5x8", 175, 90, 5, 8, 8),
    ("H-200x100x5.5x8", 200, 100, 5.5, 8, 11),
    ("H-200x200x8x12", 200, 200, 8, 12, 13),
    ("H-248x124x5x8", 248, 124, 5, 8, 10),
    ("H-250x250x9x14", 250, 250, 9, 14, 13),
    ("H-298x149x5.5x8", 298, 149, 5.5, 8, 13),
    ("H-300x150x6.5x9", 300, 150, 6.5, 9, 13),
    ("H-300x300x10x15", 300, 300, 10, 15, 18),
    ("H-346x174x6x9", 346, 174, 6, 9, 13),
    ("H-350x175x7x11", 350, 175, 7, 11, 13),
    ("H-350x350x12x19", 350, 350, 12, 19, 18),
    ("H-396x199x7x11", 396, 199, 7, 11, 16),
    ("H-400x200x8x13", 400, 200, 8, 13, 16),
    ("H-400x400x13x21", 400, 400, 13, 21, 22),
    ("H-450x200x9x14", 450, 200, 9, 14, 18),
    ("H-500x200x10x16", 500, 200, 10, 16, 20),
    ("H-588x300x12x20", 588, 300, 12, 20, 28),
    ("H-600x200x11x17", 600, 200, 11, 17, 22),
    ("H-700x300x13x24", 700, 300, 13, 24, 28),
]

# --- 鋼材DB ---
STEEL_MATERIALS = [
    {
        "name": "SS400",
        "standard": "JIS G 3101",
        "F_by_thickness": [
            {"t_max": 40, "F": 235},
            {"t_max": 75, "F": 215},
        ],
        "E": 205000,
        "G": 79000,
        "density": 7850,
        "note": "一般構造用圧延鋼材",
    },
    {
        "name": "SN400A",
        "standard": "JIS G 3136",
        "F_by_thickness": [
            {"t_max": 40, "F": 235},
            {"t_max": 100, "F": 215},
        ],
        "E": 205000,
        "G": 79000,
        "density": 7850,
        "note": "建築構造用圧延鋼材（非溶接部材用）",
        "weldable": False,
    },
    {
        "name": "SN400B",
        "standard": "JIS G 3136",
        "F_by_thickness": [
            {"t_max": 40, "F": 235},
            {"t_max": 100, "F": 215},
        ],
        "E": 205000,
        "G": 79000,
        "density": 7850,
        "note": "建築構造用圧延鋼材",
        "weldable": True,
    },
    {
        "name": "SN400C",
        "standard": "JIS G 3136",
        "F_by_thickness": [
            {"t_max": 40, "F": 235},
            {"t_max": 100, "F": 215},
        ],
        "E": 205000,
        "G": 79000,
        "density": 7850,
        "note": "建築構造用圧延鋼材（板厚方向特性保証）",
        "weldable": True,
        "through_thickness": True,
    },
    {
        "name": "SN490B",
        "standard": "JIS G 3136",
        "F_by_thickness": [
            {"t_max": 40, "F": 325},
            {"t_max": 100, "F": 295},
        ],
        "E": 205000,
        "G": 79000,
        "density": 7850,
        "note": "建築構造用圧延鋼材（高強度）",
        "weldable": True,
    },
    {
        "name": "SN490C",
        "standard": "JIS G 3136",
        "F_by_thickness": [
            {"t_max": 40, "F": 325},
            {"t_max": 100, "F": 295},
        ],
        "E": 205000,
        "G": 79000,
        "density": 7850,
        "note": "建築構造用圧延鋼材（高強度・板厚方向特性保証）",
        "weldable": True,
        "through_thickness": True,
    },
    {
        "name": "BCR295",
        "standard": "国土交通大臣認定",
        "F_by_thickness": [
            {"t_max": 30, "F": 295},
        ],
        "E": 205000,
        "G": 79000,
        "density": 7850,
        "note": "冷間ロール成形角形鋼管柱（Building Column Roll）",
        "weldable": True,
        "section_type": "box",
    },
    {
        "name": "BCP235",
        "standard": "国土交通大臣認定",
        "F_by_thickness": [
            {"t_max": 40, "F": 235},
        ],
        "E": 205000,
        "G": 79000,
        "density": 7850,
        "note": "冷間プレス成形角形鋼管柱（Building Column Press）",
        "weldable": True,
        "section_type": "box",
    },
    {
        "name": "BCP325",
        "standard": "国土交通大臣認定",
        "F_by_thickness": [
            {"t_max": 40, "F": 325},
        ],
        "E": 205000,
        "G": 79000,
        "density": 7850,
        "note": "冷間プレス成形角形鋼管柱（Building Column Press, 高強度）",
        "weldable": True,
        "section_type": "box",
    },
    {
        "name": "STKR400",
        "standard": "JIS G 3466",
        "F_by_thickness": [
            {"t_max": 12, "F": 235},
        ],
        "E": 205000,
        "G": 79000,
        "density": 7850,
        "note": "一般構造用角形鋼管",
        "weldable": True,
        "section_type": "box",
    },
    {
        "name": "STKR490",
        "standard": "JIS G 3466",
        "F_by_thickness": [
            {"t_max": 12, "F": 325},
        ],
        "E": 205000,
        "G": 79000,
        "density": 7850,
        "note": "一般構造用角形鋼管（高強度）",
        "weldable": True,
        "section_type": "box",
    },
]

# --- BCR295 角形鋼管断面 ---
# 代表的なサイズ (B x t) — 正方形のみ
BCR295_SIZES = [
    ("□-150x150x6", 150, 6),
    ("□-175x175x6", 175, 6),
    ("□-200x200x6", 200, 6),
    ("□-200x200x8", 200, 8),
    ("□-200x200x9", 200, 9),
    ("□-250x250x6", 250, 6),
    ("□-250x250x9", 250, 9),
    ("□-250x250x12", 250, 12),
    ("□-300x300x9", 300, 9),
    ("□-300x300x12", 300, 12),
    ("□-300x300x16", 300, 16),
    ("□-350x350x9", 350, 9),
    ("□-350x350x12", 350, 12),
    ("□-350x350x16", 350, 16),
    ("□-400x400x12", 400, 12),
    ("□-400x400x16", 400, 16),
    ("□-400x400x19", 400, 19),
    ("□-400x400x22", 400, 22),
    ("□-450x450x16", 450, 16),
    ("□-450x450x19", 450, 19),
    ("□-500x500x16", 500, 16),
    ("□-500x500x19", 500, 19),
    ("□-500x500x22", 500, 22),
]

# --- BCP235 角形鋼管断面 ---
BCP235_SIZES = [
    ("□-200x200x9", 200, 9),
    ("□-200x200x12", 200, 12),
    ("□-250x250x9", 250, 9),
    ("□-250x250x12", 250, 12),
    ("□-250x250x16", 250, 16),
    ("□-300x300x9", 300, 9),
    ("□-300x300x12", 300, 12),
    ("□-300x300x16", 300, 16),
    ("□-300x300x19", 300, 19),
    ("□-350x350x12", 350, 12),
    ("□-350x350x16", 350, 16),
    ("□-350x350x19", 350, 19),
    ("□-400x400x12", 400, 12),
    ("□-400x400x16", 400, 16),
    ("□-400x400x19", 400, 19),
    ("□-400x400x22", 400, 22),
    ("□-450x450x19", 450, 19),
    ("□-450x450x22", 450, 22),
    ("□-500x500x19", 500, 19),
    ("□-500x500x22", 500, 22),
    ("□-500x500x25", 500, 25),
    ("□-550x550x22", 550, 22),
    ("□-550x550x25", 550, 25),
]

# --- BCP325 角形鋼管断面 ---
BCP325_SIZES = [
    ("□-200x200x9", 200, 9),
    ("□-200x200x12", 200, 12),
    ("□-250x250x9", 250, 9),
    ("□-250x250x12", 250, 12),
    ("□-250x250x16", 250, 16),
    ("□-300x300x9", 300, 9),
    ("□-300x300x12", 300, 12),
    ("□-300x300x16", 300, 16),
    ("□-300x300x19", 300, 19),
    ("□-350x350x12", 350, 12),
    ("□-350x350x16", 350, 16),
    ("□-350x350x19", 350, 19),
    ("□-400x400x12", 400, 12),
    ("□-400x400x16", 400, 16),
    ("□-400x400x19", 400, 19),
    ("□-400x400x22", 400, 22),
    ("□-450x450x19", 450, 19),
    ("□-450x450x22", 450, 22),
    ("□-500x500x19", 500, 19),
    ("□-500x500x22", 500, 22),
    ("□-500x500x25", 500, 25),
    ("□-550x550x22", 550, 22),
    ("□-550x550x25", 550, 25),
]


def generate_h_json():
    """JIS H形鋼データを生成"""
    results = []
    for name, H, B, tw, tf, r in JIS_H_SECTIONS:
        props = calc_h_props(H, B, tw, tf)
        entry = {"name": name, "H": H, "B": B, "tw": tw, "tf": tf, "r": r}
        entry.update(props)
        results.append(entry)
    return results


def generate_box_json(sizes):
    """角形鋼管データを生成"""
    results = []
    for name, B, t in sizes:
        props = calc_box_props(B, t)
        entry = {"name": name, "B": B, "t": t}
        entry.update(props)
        results.append(entry)
    return results


def write_json(filename, data, description=""):
    filepath = os.path.join(DATA_DIR, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"  生成: {filepath} ({len(data)} 件) {description}")


def main():
    os.makedirs(DATA_DIR, exist_ok=True)
    print("=== jp_struct データベース生成 ===\n")

    write_json("jis_g3192_h.json", generate_h_json(), "JIS H形鋼")
    write_json("steel_materials.json", STEEL_MATERIALS, "鋼材")
    write_json("bcr295.json", generate_box_json(BCR295_SIZES), "BCR295角形鋼管")
    write_json("bcp235.json", generate_box_json(BCP235_SIZES), "BCP235角形鋼管")
    write_json("bcp325.json", generate_box_json(BCP325_SIZES), "BCP325角形鋼管")

    print("\n完了")


if __name__ == "__main__":
    main()
