# jp_struct — 日本建築基準法 許容応力度設計 構造検定モジュール

令82条に基づくルート1〜2の許容応力度検定を行うPythonモジュール。
Rhino8 / Grasshopper / Karamba3D と連携して、形態探索から日本基準適合チェックまで一気通貫で行うことを目的とする。

## バージョン

`0.2.0-alpha` — Task 1 完了

## ディレクトリ構成

```
jp_struct/
├── data/
│   ├── jis_g3192_h.json       # JIS H形鋼DB (23サイズ)
│   ├── bh_sections.json       # BH断面DB (10サイズ)
│   ├── steel_materials.json   # 鋼材DB (SS400, SN400A/B/C, SN490B/C, BCR295, BCP235, BCP325, STKR400/490)
│   ├── bcr295.json            # BCR295 角形鋼管DB (23サイズ)
│   ├── bcp235.json            # BCP235 角形鋼管DB (23サイズ)
│   └── bcp325.json            # BCP325 角形鋼管DB (23サイズ)
├── jp_struct/
│   ├── __init__.py
│   ├── sections.py            # DBローダ + HSection/BHSection/BoxSection/SteelMaterial dataclass
│   ├── allowable.py           # 許容応力度算定 (fc座屈, fb横座屈, 幅厚比H/BOX)
│   ├── check.py               # 部材検定本体 (MemberInput → CheckResult, 断面型ディスパッチ)
│   └── loads.py               # 令82条 荷重組合せ
├── hops/
│   └── hops_server.py         # Flask + ghhops-server (H/BH/BOX対応)
├── gh_examples/
│   ├── gh_python_example.py
│   └── karamba_bridge_example.py
├── scripts/
│   ├── generate_data.py       # 全JSONデータ生成スクリプト
│   └── calc_bh_properties.py  # BH断面性能計算スクリプト
├── tests/
│   └── test_smoke.py          # スモークテスト (16テスト)
├── requirements.txt
└── README.md
```

## 単位系

内部は全て **SI単位系**:
- 力: N
- 長さ: mm
- 応力: N/mm² (= MPa)
- モーメント: N·mm

kN / kN·m 系との変換は入出力の境界で行う（例: Karamba3D ブリッジ参照）。

## 出典・法令根拠

| モジュール | 主な出典 |
|-----------|---------|
| `allowable.py` fc | 昭55建告第1793号（圧縮座屈） |
| `allowable.py` fb | H19国交告第594号（横座屈）, 鋼構造設計規準 5.2節 |
| `allowable.py` ft, fs | 令90条（鋼材の許容応力度） |
| `allowable.py` 幅厚比 | H12建告第2464号（幅厚比区分 FA/FB/FC/FD） |
| `check.py` | 鋼構造設計規準 6.1節（組合せ応力の検定） |
| `loads.py` | 令82条（荷重組合せ） |
| `sections.py` | JIS G 3192, JIS G 3466, JIS G 3101, JIS G 3136 |

## クイックスタート

### インストール

```bash
cd jp_struct/
pip install -r requirements.txt
```

### テスト実行

```bash
cd jp_struct/
python tests/test_smoke.py
```

### Python から使う

```python
from jp_struct.sections import get_h_section, get_material
from jp_struct.check import MemberInput, check_member

# H-400x200x8x13, SN400B の梁
sec = get_h_section("H-400x200x8x13")
mat = get_material("SN400B")

inp = MemberInput(
    member_id="B1",
    section=sec,
    material=mat,
    L=6000,        # 部材長 6m
    lb=3000,       # 横補剛間距離 3m
    Mx=200e6,      # 200 kN·m
    Vy=100e3,      # 100 kN
    duration="long",
)

result = check_member(inp)
print(f"検定比: {result.ratio_max:.3f} → {result.judge}")
```

### 角形鋼管柱の検定

```python
from jp_struct.sections import get_box_section, get_material
from jp_struct.check import MemberInput, check_member

sec = get_box_section("□-300x300x12", "bcr295")
mat = get_material("BCR295")

inp = MemberInput(
    member_id="C1",
    section=sec, material=mat,
    L=4000, lb=4000,
    N=-800e3,     # 圧縮 800kN
    Mx=50e6,      # 50 kN·m
    duration="long",
)

result = check_member(inp)
print(f"検定比: {result.ratio_max:.3f} → {result.judge}")
print(f"幅厚比区分: {result.wt_rank}")
```

### Hops サーバ起動

```bash
cd jp_struct/
python hops/hops_server.py
```

## 開発ロードマップ

| Task | 内容 | 状態 |
|------|------|------|
| α版 | H形鋼検定・許容応力度・荷重組合せ | :white_check_mark: 完了 |
| Task 1 | BH断面 + BCR/BCP角形鋼管DB + 幅厚比(BOX) + 断面型ディスパッチ | :white_check_mark: 完了 |
| Task 2 | 接合部検定（高力ボルト + 溶接） | 未着手 |
| Task 3 | 検定表XLSX自動出力 | 未着手 |
| Task 4 | Hopsエンドポイント拡張 | 未着手 |

## 設計原則

- **法令遵守**: 検定式に出典を明記
- **単位の一貫性**: 内部SI（N, mm）
- **dataclassベース**: `MemberInput` / `CheckResult`
- **テストファースト**: `tests/` にスモークテスト
- **日本語コメント**: 構造設計者向け

## 環境

- Python 3.11+
- 依存: flask, ghhops-server, openpyxl
- 対象: Rhino8 / Grasshopper (CPython3)

## ライセンス

AHA (Aki Hamada Architects) 内部利用
