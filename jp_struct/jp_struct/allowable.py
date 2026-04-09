"""
許容応力度算定モジュール

鋼構造部材の許容応力度（引張・圧縮・曲げ・せん断）を算定する。

出典:
  - 建築基準法施行令 第90条（鋼材等の許容応力度）
  - 建築基準法施行令 第96条, 第98条
  - 昭55建告第1793号（圧縮材の許容座屈応力度）
  - H19国交告第594号（曲げ材の許容応力度）
  - H12建告第2464号（幅厚比による断面の種別）
  - 鋼構造設計規準 — 許容応力度設計法（日本建築学会, 2005/2019）

単位: N, mm, N/mm²
"""

import math

# --- 物性定数 ---
E_STEEL = 205_000.0  # ヤング係数 (N/mm²)  令97条
G_STEEL = 79_000.0  # せん断弾性係数 (N/mm²)


# ============================================================
# 基本許容応力度（長期）
# ============================================================


def calc_ft(F: float) -> float:
    """長期許容引張応力度

    出典: 令90条 表 — ft = F / 1.5

    Parameters:
        F: 基準強度 (N/mm²)
    Returns:
        ft: 長期許容引張応力度 (N/mm²)
    """
    return F / 1.5


def calc_fs(F: float) -> float:
    """長期許容せん断応力度

    出典: 令90条 表 — fs = F / (1.5 × √3)

    Parameters:
        F: 基準強度 (N/mm²)
    Returns:
        fs: 長期許容せん断応力度 (N/mm²)
    """
    return F / (1.5 * math.sqrt(3))


# ============================================================
# 圧縮座屈 — 許容圧縮応力度 fc
# ============================================================


def calc_fc(F: float, lk: float, i: float, E: float = E_STEEL) -> float:
    """長期許容圧縮応力度（座屈考慮）

    出典: 昭55建告第1793号
          鋼構造設計規準（日本建築学会, 2005）4.2節

    算定式:
      Λ = √(π²E / (0.6F))               …限界細長比
      λ ≤ Λ のとき:
        ν = 3/2 + 2/3 × (λ/Λ)²          …安全率
        fc = {1 − 0.4(λ/Λ)²} × F / ν
      λ > Λ のとき（弾性座屈域）:
        fc = (18/65) × F / (λ/Λ)²

    Parameters:
        F:  基準強度 (N/mm²)
        lk: 座屈長さ (mm) — 柱長さ × 座屈長さ係数
        i:  断面二次半径 (mm) — 座屈を検討する軸方向
        E:  ヤング係数 (N/mm²)

    Returns:
        fc: 長期許容圧縮応力度 (N/mm²)
    """
    if i <= 0:
        raise ValueError(f"断面二次半径 i は正の値が必要: {i}")

    lam = lk / i  # 細長比 λ
    Lam = math.sqrt(math.pi**2 * E / (0.6 * F))  # 限界細長比 Λ

    ratio = lam / Lam

    if ratio <= 1.0:
        # 非弾性座屈域
        nu = 1.5 + (2.0 / 3.0) * ratio**2  # 安全率 ν
        fc = (1.0 - 0.4 * ratio**2) * F / nu
    else:
        # 弾性座屈域（Euler座屈）
        fc = (18.0 / 65.0) * F / ratio**2

    return fc


# ============================================================
# 横座屈 — 許容曲げ応力度 fb
# ============================================================


def calc_fb(
    F: float,
    lb: float,
    h: float,
    Af: float,
    iy: float,
    C: float = 1.0,
    E: float = E_STEEL,
) -> float:
    """長期許容曲げ応力度（横座屈考慮）— H形鋼用

    出典: H19国交告第594号
          鋼構造設計規準（日本建築学会, 2005）5.2節

    2つの評価式の大きい方を採用し、ft を上限とする:
      fb = min(ft, max(fb1, fb2))

    式1 (弱軸細長比ベース):
      λb = lb / (iy × √C)
      Λ  = √(π²E / (0.6F))
      λb ≤ Λ: ν = 3/2 + 2/3×(λb/Λ)²
               fb1 = {1 − 0.4(λb/Λ)²} × F / ν
      λb > Λ: fb1 = (18/65) × F / (λb/Λ)²

    式2 (弾性横座屈の簡易式):
      fb2 = 89,000 × C / (lb × h / Af)

      89,000 の根拠: π²E/(4√3) ≈ 89,200 を丸めた値
      (鋼構造設計規準 式5.5 参照)

    Parameters:
        F:  基準強度 (N/mm²)
        lb: 横補剛間距離 (mm)
        h:  梁せい (mm)
        Af: 圧縮フランジ面積 = B × tf (mm²)
        iy: 弱軸断面二次半径 (mm)
        C:  モーメント補正係数 (default=1.0 — 等曲げ、安全側)
            等モーメント: C=1.0
            逆対称曲げ:   C=2.3 (片端ピン: 1.75 等)
        E:  ヤング係数 (N/mm²)

    Returns:
        fb: 長期許容曲げ応力度 (N/mm²)
    """
    ft = F / 1.5  # 上限値

    if lb <= 0:
        return ft

    # --- 式1: 弱軸細長比ベース ---
    if C <= 0:
        C = 1.0
    lambda_b = lb / (iy * math.sqrt(C))
    Lambda = math.sqrt(math.pi**2 * E / (0.6 * F))
    ratio = lambda_b / Lambda

    if ratio <= 1.0:
        nu = 1.5 + (2.0 / 3.0) * ratio**2
        fb1 = (1.0 - 0.4 * ratio**2) * F / nu
    else:
        fb1 = (18.0 / 65.0) * F / ratio**2

    # --- 式2: 弾性横座屈の簡易式 ---
    alpha = lb * h / Af  # 横座屈パラメータ (無次元)
    if alpha > 0:
        fb2 = 89_000.0 * C / alpha
    else:
        fb2 = ft

    fb = max(fb1, fb2)
    return min(fb, ft)


# ============================================================
# 幅厚比区分 — H形鋼
# ============================================================

# 幅厚比区分の係数
# 出典: H12建告第2464号 別表
#
# フランジ突出板 (半幅: b = (B − tw)/2 に対する b/tf の制限)
_WT_FLANGE_H = {
    "FA": 0.40,
    "FB": 0.52,
    "FC": 0.74,
}

# ウェブ中間板 (クリアウェブ高さ hw = H − 2tf に対する hw/tw の制限)
# 曲げ部材（ウェブが曲げを受ける場合）
_WT_WEB_BENDING = {
    "FA": 1.60,
    "FB": 2.24,
    "FC": 3.20,
}

# 圧縮部材（ウェブが一様圧縮を受ける場合）
_WT_WEB_COMPRESSION = {
    "FA": 0.56,
    "FB": 0.73,
    "FC": 1.04,
}


def width_thickness_rank_h(
    B: float,
    tf: float,
    tw: float,
    H: float,
    F: float,
    is_column: bool = False,
    E: float = E_STEEL,
) -> dict:
    """H形鋼の幅厚比による断面区分を判定する

    出典: H12建告第2464号（鋼材等の幅厚比の区分）
          鋼構造設計規準（日本建築学会, 2005）表4.1, 表5.1

    Parameters:
        B:  フランジ幅 (mm)
        tf: フランジ厚 (mm)
        tw: ウェブ厚 (mm)
        H:  梁せい (mm)
        F:  基準強度 (N/mm²)
        is_column: True の場合、ウェブは圧縮部材として判定
        E:  ヤング係数 (N/mm²)

    Returns:
        dict: {
            "flange_ratio": フランジ幅厚比,
            "flange_rank": フランジの区分 ("FA"/"FB"/"FC"/"FD"),
            "web_ratio": ウェブ幅厚比,
            "web_rank": ウェブの区分 ("FA"/"FB"/"FC"/"FD"),
            "rank": 総合区分（低い方に合わせる）
        }
    """
    sqrt_EF = math.sqrt(E / F)

    # フランジ幅厚比
    b = (B - tw) / 2  # フランジ突出幅
    flange_ratio = b / tf

    flange_rank = "FD"
    for rank in ("FA", "FB", "FC"):
        if flange_ratio <= _WT_FLANGE_H[rank] * sqrt_EF:
            flange_rank = rank
            break

    # ウェブ幅厚比
    hw = H - 2 * tf  # クリアウェブ高さ
    web_ratio = hw / tw

    wt_web = _WT_WEB_COMPRESSION if is_column else _WT_WEB_BENDING
    web_rank = "FD"
    for rank in ("FA", "FB", "FC"):
        if web_ratio <= wt_web[rank] * sqrt_EF:
            web_rank = rank
            break

    # 総合区分: フランジとウェブの低い方
    rank_order = {"FA": 0, "FB": 1, "FC": 2, "FD": 3}
    overall_idx = max(rank_order[flange_rank], rank_order[web_rank])
    overall_rank = {v: k for k, v in rank_order.items()}[overall_idx]

    return {
        "flange_ratio": round(flange_ratio, 2),
        "flange_rank": flange_rank,
        "web_ratio": round(web_ratio, 2),
        "web_rank": web_rank,
        "rank": overall_rank,
    }


# ============================================================
# 幅厚比区分 — 角形鋼管
# ============================================================

# 角形鋼管の幅厚比制限
# 出典: H12建告第2464号 別表
# 角形鋼管の各辺は「中間板（両端支持）」として扱う
# 板幅 = B − 2t (内法), 幅厚比 = (B − 2t) / t
#
# ただし角形鋼管柱の場合、軸力＋曲げの組合せ応力を受けるため、
# 圧縮部材としての制限値を適用する。
_WT_BOX = {
    "FA": 0.56,
    "FB": 0.73,
    "FC": 1.04,
}


def width_thickness_rank_box(
    B: float,
    t: float,
    F: float,
    E: float = E_STEEL,
) -> dict:
    """角形鋼管の幅厚比による断面区分を判定する

    出典: H12建告第2464号
          鋼構造設計規準（日本建築学会, 2005）表4.1

    角形鋼管の各辺は「中間板（両端支持、一様圧縮）」として扱う。
    板幅 = B − 2t（角Rを無視した内法寸法）

    Parameters:
        B: 辺長 (mm)
        t: 板厚 (mm)
        F: 基準強度 (N/mm²)
        E: ヤング係数 (N/mm²)

    Returns:
        dict: {
            "ratio": 幅厚比,
            "rank": 区分 ("FA"/"FB"/"FC"/"FD"),
            "limit_FA": FA限界値,
            "limit_FB": FB限界値,
            "limit_FC": FC限界値,
        }
    """
    sqrt_EF = math.sqrt(E / F)
    plate_width = B - 2 * t  # 内法板幅
    ratio = plate_width / t

    rank = "FD"
    for r in ("FA", "FB", "FC"):
        if ratio <= _WT_BOX[r] * sqrt_EF:
            rank = r
            break

    return {
        "ratio": round(ratio, 2),
        "rank": rank,
        "limit_FA": round(_WT_BOX["FA"] * sqrt_EF, 2),
        "limit_FB": round(_WT_BOX["FB"] * sqrt_EF, 2),
        "limit_FC": round(_WT_BOX["FC"] * sqrt_EF, 2),
    }
