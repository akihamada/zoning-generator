"""
部材検定モジュール — 許容応力度設計による鋼構造部材の検定

MemberInput を受け取り、許容応力度と作用応力度を比較して
CheckResult を返す。

出典:
  - 建築基準法施行令 第82条（許容応力度計算）
  - 鋼構造設計規準 — 許容応力度設計法（日本建築学会, 2005/2019）
  - 昭55建告第1793号（圧縮座屈）
  - H19国交告第594号（曲げの横座屈）
  - H12建告第2464号（幅厚比区分）

検定式（鋼構造設計規準 6.1節）:
  曲げ＋軸力の組合せ応力に対する検定比:
    σc/fc + σb/fb ≤ 1.0   （圧縮＋曲げ）
    σt/ft + σb/fb ≤ 1.0   （引張＋曲げ）
    τ/fs ≤ 1.0             （せん断）

  ここで σ, τ は作用応力度、fc, fb, ft, fs は許容応力度。

単位: N, mm, N/mm²
"""

from dataclasses import dataclass, field
from typing import Optional, Union

from jp_struct.sections import (
    HSection,
    BHSection,
    BoxSection,
    SteelMaterial,
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


@dataclass
class MemberInput:
    """部材検定の入力データ

    Attributes:
        member_id:   部材ID（任意の識別子）
        section:     断面データ (HSection, BHSection, or BoxSection)
        material:    鋼材データ (SteelMaterial)
        L:           部材長さ (mm)
        lb:          横補剛間距離 (mm) — 梁の横座屈検討用
        lkx:         強軸まわり座屈長さ (mm) — 柱の座屈検討用（省略時 = L）
        lky:         弱軸まわり座屈長さ (mm) — 柱の座屈検討用（省略時 = L）
        N:           軸力 (N) — 正:引張、負:圧縮
        Mx:          強軸曲げモーメント (N·mm)
        Vy:          せん断力 (N)
        C:           モーメント補正係数 (default=1.0)
        duration:    "long" (長期) or "short" (短期)
    """

    member_id: str
    section: Union[HSection, BHSection, BoxSection]
    material: SteelMaterial
    L: float
    lb: float
    lkx: Optional[float] = None
    lky: Optional[float] = None
    N: float = 0.0
    Mx: float = 0.0
    Vy: float = 0.0
    C: float = 1.0
    duration: str = "long"


@dataclass
class CheckResult:
    """部材検定の結果

    Attributes:
        member_id:        部材ID
        section_name:     断面名
        material_name:    鋼材名
        F:                基準強度 (N/mm²)
        duration:         "long" or "short"

        sigma_c:          作用圧縮応力度 (N/mm²) ※圧縮時のみ
        sigma_t:          作用引張応力度 (N/mm²) ※引張時のみ
        sigma_b:          作用曲げ応力度 (N/mm²)
        tau:              作用せん断応力度 (N/mm²)

        fc:               許容圧縮応力度 (N/mm²)
        ft:               許容引張応力度 (N/mm²)
        fb:               許容曲げ応力度 (N/mm²)
        fs:               許容せん断応力度 (N/mm²)

        lambda_x:         強軸細長比
        lambda_y:         弱軸細長比
        wt_rank:          幅厚比区分 ("FA"/"FB"/"FC"/"FD")

        ratio_combined:   組合せ検定比 (σ/f_axial + σb/fb)
        ratio_shear:      せん断検定比 (τ/fs)
        ratio_max:        最大検定比
        judge:            判定 ("OK" or "NG")
    """

    member_id: str
    section_name: str
    material_name: str
    F: float
    duration: str

    sigma_c: float = 0.0
    sigma_t: float = 0.0
    sigma_b: float = 0.0
    tau: float = 0.0

    fc: float = 0.0
    ft: float = 0.0
    fb: float = 0.0
    fs: float = 0.0

    lambda_x: float = 0.0
    lambda_y: float = 0.0
    wt_rank: str = ""

    ratio_combined: float = 0.0
    ratio_shear: float = 0.0
    ratio_max: float = 0.0
    judge: str = ""


def _get_representative_thickness(section) -> float:
    """断面から代表板厚（フランジ厚相当）を取得する"""
    if hasattr(section, "tf"):
        return section.tf
    elif hasattr(section, "t"):
        return section.t
    else:
        raise ValueError(f"断面型 {type(section)} から板厚を取得できません")


def _check_h_like(inp: MemberInput) -> CheckResult:
    """H形鋼・BH断面の検定

    出典: 鋼構造設計規準 6.1節
    """
    sec = inp.section  # HSection or BHSection
    mat = inp.material

    # --- 基準強度 ---
    t_rep = sec.tf
    F = get_F(mat, t_rep)

    # 短期は長期の1.5倍（令90条）
    duration_factor = 1.5 if inp.duration == "short" else 1.0

    # --- 許容応力度（長期ベースで算定し、短期は1.5倍） ---
    lkx = inp.lkx if inp.lkx is not None else inp.L
    lky = inp.lky if inp.lky is not None else inp.L

    ft_val = calc_ft(F) * duration_factor
    fs_val = calc_fs(F) * duration_factor
    fc_val = calc_fc(F, lky, sec.iy) * duration_factor  # 弱軸座屈が支配的
    fb_val = calc_fb(F, inp.lb, sec.H, sec.Af, sec.iy, inp.C) * duration_factor

    # 強軸座屈も確認（fc は小さい方を採用）
    fc_x = calc_fc(F, lkx, sec.ix) * duration_factor
    fc_val = min(fc_val, fc_x)

    # --- 細長比 ---
    lambda_x = lkx / sec.ix if sec.ix > 0 else 0
    lambda_y = lky / sec.iy if sec.iy > 0 else 0

    # --- 幅厚比区分 ---
    is_column = abs(inp.N) > 0 and inp.N < 0
    wt = width_thickness_rank_h(
        sec.B, sec.tf, sec.tw, sec.H, F, is_column=is_column
    )
    wt_rank = wt["rank"]

    # --- 作用応力度 ---
    sigma_b = abs(inp.Mx) / sec.Zx if sec.Zx > 0 else 0
    tau = abs(inp.Vy) / (sec.H * sec.tw) if (sec.H * sec.tw) > 0 else 0

    sigma_c = 0.0
    sigma_t = 0.0
    if inp.N < 0:
        # 圧縮
        sigma_c = abs(inp.N) / sec.A
    elif inp.N > 0:
        # 引張
        sigma_t = inp.N / sec.A

    # --- 検定比 ---
    # 組合せ応力（鋼構造設計規準 6.1節）
    if sigma_c > 0 and fc_val > 0:
        ratio_combined = sigma_c / fc_val + sigma_b / fb_val if fb_val > 0 else 999
    elif sigma_t > 0 and ft_val > 0:
        ratio_combined = sigma_t / ft_val + sigma_b / fb_val if fb_val > 0 else 999
    else:
        ratio_combined = sigma_b / fb_val if fb_val > 0 else 0

    ratio_shear = tau / fs_val if fs_val > 0 else 0
    ratio_max = max(ratio_combined, ratio_shear)
    judge = "OK" if ratio_max <= 1.0 else "NG"

    return CheckResult(
        member_id=inp.member_id,
        section_name=sec.name,
        material_name=mat.name,
        F=F,
        duration=inp.duration,
        sigma_c=round(sigma_c, 2),
        sigma_t=round(sigma_t, 2),
        sigma_b=round(sigma_b, 2),
        tau=round(tau, 2),
        fc=round(fc_val, 2),
        ft=round(ft_val, 2),
        fb=round(fb_val, 2),
        fs=round(fs_val, 2),
        lambda_x=round(lambda_x, 2),
        lambda_y=round(lambda_y, 2),
        wt_rank=wt_rank,
        ratio_combined=round(ratio_combined, 4),
        ratio_shear=round(ratio_shear, 4),
        ratio_max=round(ratio_max, 4),
        judge=judge,
    )


def _check_box(inp: MemberInput) -> CheckResult:
    """角形鋼管の検定

    角形鋼管柱は横座屈しないため fb = ft とする。
    （閉断面はねじり剛性が高く、横座屈の検討が不要）

    出典: 鋼構造設計規準 5.3節
          H12建告第2464号（幅厚比）
    """
    sec = inp.section  # BoxSection
    mat = inp.material

    # --- 基準強度 ---
    t_rep = sec.t
    F = get_F(mat, t_rep)

    duration_factor = 1.5 if inp.duration == "short" else 1.0

    # --- 許容応力度 ---
    lkx = inp.lkx if inp.lkx is not None else inp.L
    lky = inp.lky if inp.lky is not None else inp.L

    ft_val = calc_ft(F) * duration_factor
    fs_val = calc_fs(F) * duration_factor

    # 角形鋼管は正方形のため ix = iy → 座屈は同一
    fc_val = calc_fc(F, lkx, sec.ix) * duration_factor

    # 角形鋼管（閉断面）は横座屈しない → fb = ft
    fb_val = ft_val

    # --- 細長比 ---
    lambda_x = lkx / sec.ix if sec.ix > 0 else 0
    lambda_y = lky / sec.iy if sec.iy > 0 else 0

    # --- 幅厚比区分 ---
    wt = width_thickness_rank_box(sec.B, sec.t, F)
    wt_rank = wt["rank"]

    # --- 作用応力度 ---
    sigma_b = abs(inp.Mx) / sec.Zx if sec.Zx > 0 else 0
    # 角形鋼管のせん断: 2面のウェブで負担（概算: τ = V / (2 × B × t)）
    Aw = 2 * sec.B * sec.t  # せん断有効面積（2面）
    tau = abs(inp.Vy) / Aw if Aw > 0 else 0

    sigma_c = 0.0
    sigma_t = 0.0
    if inp.N < 0:
        sigma_c = abs(inp.N) / sec.A
    elif inp.N > 0:
        sigma_t = inp.N / sec.A

    # --- 検定比 ---
    if sigma_c > 0 and fc_val > 0:
        ratio_combined = sigma_c / fc_val + sigma_b / fb_val if fb_val > 0 else 999
    elif sigma_t > 0 and ft_val > 0:
        ratio_combined = sigma_t / ft_val + sigma_b / fb_val if fb_val > 0 else 999
    else:
        ratio_combined = sigma_b / fb_val if fb_val > 0 else 0

    ratio_shear = tau / fs_val if fs_val > 0 else 0
    ratio_max = max(ratio_combined, ratio_shear)
    judge = "OK" if ratio_max <= 1.0 else "NG"

    return CheckResult(
        member_id=inp.member_id,
        section_name=sec.name,
        material_name=mat.name,
        F=F,
        duration=inp.duration,
        sigma_c=round(sigma_c, 2),
        sigma_t=round(sigma_t, 2),
        sigma_b=round(sigma_b, 2),
        tau=round(tau, 2),
        fc=round(fc_val, 2),
        ft=round(ft_val, 2),
        fb=round(fb_val, 2),
        fs=round(fs_val, 2),
        lambda_x=round(lambda_x, 2),
        lambda_y=round(lambda_y, 2),
        wt_rank=wt_rank,
        ratio_combined=round(ratio_combined, 4),
        ratio_shear=round(ratio_shear, 4),
        ratio_max=round(ratio_max, 4),
        judge=judge,
    )


def check_member(inp: MemberInput) -> CheckResult:
    """部材検定のメインエントリポイント

    断面の型に応じて適切な検定ルーチンにディスパッチする。

    Parameters:
        inp: MemberInput — 部材の入力データ

    Returns:
        CheckResult — 検定結果
    """
    sec = inp.section
    if isinstance(sec, (HSection, BHSection)):
        return _check_h_like(inp)
    elif isinstance(sec, BoxSection):
        return _check_box(inp)
    else:
        raise TypeError(
            f"未対応の断面型: {type(sec).__name__}。"
            f"対応: HSection, BHSection, BoxSection"
        )
