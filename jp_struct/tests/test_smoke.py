#!/usr/bin/env python3
"""
jp_struct スモークテスト

全モジュールの基本機能を確認する。
実行: python tests/test_smoke.py (jp_struct/ ディレクトリから)
"""

import sys
import os
import math

# パス設定: jp_struct/ プロジェクトルートを PYTHONPATH に追加
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))


def test_load_h_sections():
    """JIS H形鋼データベースの読み込み"""
    from jp_struct.sections import load_h_sections

    sections = load_h_sections()
    assert len(sections) == 23, f"H形鋼数: {len(sections)} (期待: 23)"
    # H-400x200x8x13 が含まれることを確認
    names = [s.name for s in sections]
    assert "H-400x200x8x13" in names, "H-400x200x8x13 が見つかりません"
    # 断面性能の妥当性チェック
    h400 = [s for s in sections if s.name == "H-400x200x8x13"][0]
    assert h400.H == 400
    assert h400.B == 200
    assert h400.A > 0
    assert h400.Ix > h400.Iy, "Ix > Iy (強軸 > 弱軸)"
    assert h400.ix > h400.iy, "ix > iy"
    print(f"  OK: H形鋼 {len(sections)} 件読込")


def test_load_bh_sections():
    """BH断面データベースの読み込み"""
    from jp_struct.sections import load_bh_sections

    sections = load_bh_sections()
    assert len(sections) == 10, f"BH断面数: {len(sections)} (期待: 10)"
    bh500 = [s for s in sections if "500x200x9x16" in s.name][0]
    assert bh500.H == 500
    assert bh500.section_type == "BH"
    assert bh500.r == 0.0, "BHにはフィレットなし"
    print(f"  OK: BH断面 {len(sections)} 件読込")


def test_load_box_sections():
    """角形鋼管データベースの読み込み"""
    from jp_struct.sections import load_box_sections

    for mat_type in ("bcr295", "bcp235", "bcp325"):
        sections = load_box_sections(mat_type)
        assert len(sections) > 0, f"{mat_type} が空"
        # 正方形断面なので Ix == Iy
        for s in sections:
            assert abs(s.Ix - s.Iy) < 1, f"{s.name}: Ix != Iy"
            assert s.section_type == "BOX"
    print(f"  OK: 角形鋼管 BCR295/BCP235/BCP325 読込")


def test_load_materials():
    """鋼材データベースの読み込み"""
    from jp_struct.sections import load_materials, get_F, get_material

    materials = load_materials()
    assert len(materials) >= 6, f"鋼材数: {len(materials)}"
    # SS400 の基準強度
    ss400 = get_material("SS400")
    F = get_F(ss400, 16)  # tf=16mm → F=235
    assert F == 235, f"SS400 F={F} (期待: 235)"
    # SN490B の基準強度（板厚40mm以下）
    sn490b = get_material("SN490B")
    F = get_F(sn490b, 25)
    assert F == 325, f"SN490B F={F} (期待: 325)"
    # BCR295
    bcr = get_material("BCR295")
    F = get_F(bcr, 12)
    assert F == 295, f"BCR295 F={F} (期待: 295)"
    print(f"  OK: 鋼材 {len(materials)} 件読込、基準強度取得")


def test_calc_ft_fs():
    """許容引張・せん断応力度"""
    from jp_struct.allowable import calc_ft, calc_fs

    F = 235  # SS400
    ft = calc_ft(F)
    fs = calc_fs(F)
    assert abs(ft - 235 / 1.5) < 0.01, f"ft={ft}"
    assert abs(fs - 235 / (1.5 * math.sqrt(3))) < 0.01, f"fs={fs}"
    print(f"  OK: ft={ft:.1f}, fs={fs:.1f} N/mm²")


def test_calc_fc():
    """許容圧縮応力度（座屈）"""
    from jp_struct.allowable import calc_fc

    F = 235
    # 短い柱（λ小） → fc ≈ ft に近い
    fc_short = calc_fc(F, lk=1000, i=50)  # λ=20
    assert fc_short > 100, f"短柱 fc={fc_short}"
    # 長い柱（λ大） → fc は大幅に低下
    fc_long = calc_fc(F, lk=10000, i=50)  # λ=200
    assert fc_long < fc_short, "長柱は fc が低下するはず"
    assert fc_long > 0, "fc > 0"
    # 限界細長比 Λ の確認
    Lambda = math.sqrt(math.pi**2 * 205000 / (0.6 * 235))
    assert abs(Lambda - 120.0) < 5, f"Λ={Lambda}"
    print(f"  OK: fc(λ=20)={fc_short:.1f}, fc(λ=200)={fc_long:.1f} N/mm²")


def test_calc_fb():
    """許容曲げ応力度（横座屈）"""
    from jp_struct.allowable import calc_fb

    F = 235
    ft = F / 1.5
    # 横補剛が十分（lb小） → fb ≈ ft
    fb_short = calc_fb(F, lb=1000, h=400, Af=200 * 13, iy=45)
    assert fb_short > 100, f"短スパン fb={fb_short}"
    # 横補剛が不十分（lb大） → fb 低下
    fb_long = calc_fb(F, lb=8000, h=400, Af=200 * 13, iy=45)
    assert fb_long < fb_short, "横補剛不十分で fb が低下するはず"
    assert fb_long > 0
    # fb ≤ ft の確認
    assert fb_short <= ft + 0.01, "fb ≤ ft"
    print(f"  OK: fb(lb=1m)={fb_short:.1f}, fb(lb=8m)={fb_long:.1f} N/mm²")


def test_width_thickness_h():
    """幅厚比区分（H形鋼）"""
    from jp_struct.allowable import width_thickness_rank_h

    # H-400x200x8x13, SS400
    wt = width_thickness_rank_h(B=200, tf=13, tw=8, H=400, F=235)
    assert wt["rank"] in ("FA", "FB", "FC", "FD"), f"不正な区分: {wt['rank']}"
    assert wt["flange_ratio"] > 0
    assert wt["web_ratio"] > 0
    print(f"  OK: H-400x200x8x13 幅厚比区分={wt['rank']} "
          f"(フランジ b/tf={wt['flange_ratio']}, ウェブ hw/tw={wt['web_ratio']})")


def test_width_thickness_box():
    """幅厚比区分（角形鋼管）"""
    from jp_struct.allowable import width_thickness_rank_box

    # □-300x300x12, BCR295
    wt = width_thickness_rank_box(B=300, t=12, F=295)
    assert wt["rank"] in ("FA", "FB", "FC", "FD"), f"不正な区分: {wt['rank']}"
    assert wt["ratio"] > 0
    print(f"  OK: □-300x300x12 幅厚比区分={wt['rank']} (B/t={wt['ratio']})")


def test_check_member_h():
    """部材検定（H形鋼梁）"""
    from jp_struct.sections import get_h_section, get_material
    from jp_struct.check import MemberInput, check_member

    sec = get_h_section("H-400x200x8x13")
    mat = get_material("SN400B")

    inp = MemberInput(
        member_id="B1",
        section=sec,
        material=mat,
        L=6000,
        lb=3000,  # 横補剛間距離 3m
        N=0,
        Mx=200e6,  # 200 kN·m = 200×10⁶ N·mm
        Vy=100e3,  # 100 kN
        duration="long",
    )
    result = check_member(inp)

    assert result.judge in ("OK", "NG")
    assert result.ratio_max >= 0
    assert result.fb > 0
    assert result.fs > 0
    assert result.wt_rank in ("FA", "FB", "FC", "FD")
    print(f"  OK: 梁B1 検定比={result.ratio_max:.3f} 判定={result.judge} "
          f"(σb={result.sigma_b:.1f}, fb={result.fb:.1f})")


def test_check_member_bh():
    """部材検定（BH断面梁）"""
    from jp_struct.sections import get_bh_section, get_material
    from jp_struct.check import MemberInput, check_member

    sec = get_bh_section("BH-500x200x9x16")
    mat = get_material("SN400B")

    inp = MemberInput(
        member_id="B2",
        section=sec,
        material=mat,
        L=8000,
        lb=4000,
        N=0,
        Mx=300e6,
        Vy=120e3,
        duration="long",
    )
    result = check_member(inp)

    assert result.judge in ("OK", "NG")
    assert result.fb > 0
    print(f"  OK: BH梁B2 検定比={result.ratio_max:.3f} 判定={result.judge}")


def test_check_member_box():
    """部材検定（角形鋼管柱）"""
    from jp_struct.sections import get_box_section, get_material
    from jp_struct.check import MemberInput, check_member

    sec = get_box_section("□-300x300x12", "bcr295")
    mat = get_material("BCR295")

    inp = MemberInput(
        member_id="C1",
        section=sec,
        material=mat,
        L=4000,
        lb=4000,
        N=-800e3,  # 圧縮 800 kN
        Mx=50e6,   # 50 kN·m
        Vy=30e3,   # 30 kN
        duration="long",
    )
    result = check_member(inp)

    assert result.judge in ("OK", "NG")
    assert result.fc > 0
    assert result.wt_rank in ("FA", "FB", "FC", "FD")
    print(f"  OK: 柱C1 検定比={result.ratio_max:.3f} 判定={result.judge} "
          f"(σc={result.sigma_c:.1f}, fc={result.fc:.1f})")


def test_check_member_column_h():
    """部材検定（H形鋼柱 — 圧縮＋曲げ）"""
    from jp_struct.sections import get_h_section, get_material
    from jp_struct.check import MemberInput, check_member

    sec = get_h_section("H-300x300x10x15")
    mat = get_material("SN400B")

    inp = MemberInput(
        member_id="C2",
        section=sec,
        material=mat,
        L=4000,
        lb=4000,
        N=-500e3,  # 圧縮 500 kN
        Mx=80e6,   # 80 kN·m
        Vy=40e3,   # 40 kN
        duration="long",
    )
    result = check_member(inp)

    assert result.judge in ("OK", "NG")
    assert result.sigma_c > 0, "圧縮応力度が計算されるはず"
    assert result.fc > 0
    print(f"  OK: 柱C2 検定比={result.ratio_max:.3f} 判定={result.judge}")


def test_check_short_term():
    """短期検定（地震時）"""
    from jp_struct.sections import get_h_section, get_material
    from jp_struct.check import MemberInput, check_member

    sec = get_h_section("H-400x200x8x13")
    mat = get_material("SN400B")

    # 長期
    inp_long = MemberInput(
        member_id="B3-L", section=sec, material=mat,
        L=6000, lb=3000, Mx=200e6, Vy=100e3, duration="long",
    )
    # 短期（同じ応力）
    inp_short = MemberInput(
        member_id="B3-S", section=sec, material=mat,
        L=6000, lb=3000, Mx=200e6, Vy=100e3, duration="short",
    )
    r_long = check_member(inp_long)
    r_short = check_member(inp_short)

    # 短期は許容応力度が1.5倍 → 検定比が小さくなる
    assert r_short.ratio_max < r_long.ratio_max, \
        f"短期({r_short.ratio_max}) < 長期({r_long.ratio_max}) のはず"
    assert r_short.fb > r_long.fb, "短期fb > 長期fb"
    print(f"  OK: 長期検定比={r_long.ratio_max:.3f}, 短期検定比={r_short.ratio_max:.3f}")


def test_loads():
    """荷重組合せ"""
    from jp_struct.loads import STANDARD_COMBINATIONS

    assert len(STANDARD_COMBINATIONS) >= 5, f"組合せ数: {len(STANDARD_COMBINATIONS)}"
    # 長期常時の確認
    lc_long = [c for c in STANDARD_COMBINATIONS if c.duration == "long"]
    assert len(lc_long) >= 1
    # 短期地震の確認
    lc_eq = [c for c in STANDARD_COMBINATIONS if "地震" in c.name]
    assert len(lc_eq) >= 1
    for c in lc_eq:
        assert "K" in c.factors, f"{c.name} に地震荷重Kがない"
    print(f"  OK: 荷重組合せ {len(STANDARD_COMBINATIONS)} ケース")


def test_import_all():
    """全モジュールのインポート確認"""
    import jp_struct
    assert hasattr(jp_struct, "__version__")
    assert hasattr(jp_struct, "check_member")
    assert hasattr(jp_struct, "HSection")
    assert hasattr(jp_struct, "BHSection")
    assert hasattr(jp_struct, "BoxSection")
    assert hasattr(jp_struct, "width_thickness_rank_box")
    print(f"  OK: jp_struct v{jp_struct.__version__} インポート成功")


# ============================================================
# テスト実行
# ============================================================

def run_all():
    tests = [
        ("モジュールインポート", test_import_all),
        ("H形鋼DB読込", test_load_h_sections),
        ("BH断面DB読込", test_load_bh_sections),
        ("角形鋼管DB読込", test_load_box_sections),
        ("鋼材DB読込", test_load_materials),
        ("許容引張・せん断", test_calc_ft_fs),
        ("許容圧縮(座屈)", test_calc_fc),
        ("許容曲げ(横座屈)", test_calc_fb),
        ("幅厚比(H形鋼)", test_width_thickness_h),
        ("幅厚比(角形鋼管)", test_width_thickness_box),
        ("部材検定(H形鋼梁)", test_check_member_h),
        ("部材検定(BH梁)", test_check_member_bh),
        ("部材検定(角形鋼管柱)", test_check_member_box),
        ("部材検定(H形鋼柱)", test_check_member_column_h),
        ("短期検定", test_check_short_term),
        ("荷重組合せ", test_loads),
    ]

    print("=" * 60)
    print("jp_struct スモークテスト")
    print("=" * 60)

    passed = 0
    failed = 0
    for name, func in tests:
        try:
            print(f"\n[{name}]")
            func()
            passed += 1
        except Exception as e:
            print(f"  NG: {e}")
            failed += 1

    print("\n" + "=" * 60)
    print(f"結果: {passed} passed, {failed} failed / {len(tests)} total")
    print("=" * 60)

    return failed == 0


if __name__ == "__main__":
    success = run_all()
    sys.exit(0 if success else 1)
