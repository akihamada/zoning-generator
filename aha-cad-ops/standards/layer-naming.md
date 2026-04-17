# レイヤ命名規則 / Layer Naming Convention

> **一言で** / TL;DR
> 全レイヤは `<Discipline>-<Major>-<Minor>-<Status>` 形式（英大文字・ハイフン区切り）。
> 例：`A-WALL-EXTR-N`（Architecture・Wall・Exterior・New）
>
> **誰が読む**：越側オペ（作図時常時）／PM・設計リーダー（監修時）
>
> **ルール厳守**：独自レイヤ追加禁止 → 必要なら RFI

**準拠規格**：ISO 13567（Technical product documentation — Organization and naming of layers for CAD）をベースに、AHA運用に合わせて簡略化。

## 基本構造 / Base Structure

```
<Discipline>-<Major>-<Minor>-<Status>
```

例 / Example:
```
A-WALL-EXTR-N
A-DOOR-FRAM-E
S-COLM----N
M-DUCT-SUPL-N
X-IRRG-FULL-N
```

セパレータは **ハイフン**。使用しないフィールドは空（`-`連続）で詰める。全レイヤ名は **英大文字**、スペース・日本語禁止。

## Discipline（分野）1文字

| コード | 意味 |
|---|---|
| `A` | Architecture |
| `S` | Structure |
| `M` | Mechanical |
| `E` | Electrical |
| `P` | Plumbing |
| `L` | Landscape |
| `C` | Civil |
| `I` | Interior |
| `F` | Facade |
| `X` | Cross-discipline（分野横断） |

## Major Element（4文字）

### Architecture (`A-`)

| コード | 意味 |
|---|---|
| `WALL` | 壁 |
| `DOOR` | ドア建具 |
| `GLAZ` | 窓・ガラス建具 |
| `FLOR` | 床 |
| `CEIL` | 天井 |
| `ROOF` | 屋根 |
| `STAR` | 階段 |
| `RAIL` | 手摺・パラペット |
| `FURN` | 家具・造作 |
| `EQPM` | 機器 |
| `FNSH` | 仕上げ |
| `GRID` | 通り芯 |
| `DIMS` | 寸法 |
| `TEXT` | 文字・注記 |
| `SYMB` | 記号・マーカー |
| `HTCH` | ハッチ |

### Structure (`S-`)

| コード | 意味 |
|---|---|
| `COLM` | 柱 |
| `BEAM` | 梁 |
| `SLAB` | スラブ |
| `FNDN` | 基礎 |
| `BRAC` | ブレース |
| `JNTS` | 接合部 |

### MEP (`M-` / `E-` / `P-`)

| コード | 意味 |
|---|---|
| `DUCT` | ダクト |
| `PIPE` | 配管 |
| `EQPM` | 機器 |
| `LITE` | 照明 |
| `POWR` | 電源 |
| `DATA` | 通信・制御 |

## Minor Element（任意、4文字）

共通で使える細分化コード：

| コード | 意味 |
|---|---|
| `EXTR` | Exterior |
| `INTR` | Interior |
| `FULL` | Full height |
| `PART` | Partial height |
| `FRAM` | Frame |
| `LEAF` | Door leaf |
| `HARD` | Hardware |
| `HEAD` | Header |
| `SILL` | Sill |
| `SUPL` | Supply（給気・給水） |
| `RETN` | Return（還気） |
| `EXHS` | Exhaust |

## Status（状態）1文字

| コード | 意味 |
|---|---|
| `N` | New（新設） |
| `E` | Existing to remain（既存残置） |
| `D` | Demolish（解体） |
| `T` | Temporary（仮設） |
| `R` | Relocate（移設） |

## AHA 拡張メジャー要素

通常カテゴリで表現できないAHA特有要素は以下を使用（`X-` または `A-` 配下で使用可）：

| コード | 意味 |
|---|---|
| `3DPR` | 土系3Dプリント部材 |
| `IRRG` | 異形ジオメトリ（Rhino由来） |
| `KINT` | キネティック機構 |
| `SENS` | センサー・配線 |
| `ARTD` | デジタルアート統合要素 |
| `HIST` | 歴史保存要素 |

例：
```
A-3DPR-EXTR-N     ← 外装土系3Dプリント壁（新設）
X-IRRG-FULL-N     ← 分野横断の異形要素
X-KINT-FRAM-N     ← キネティック機構フレーム
X-HIST-WALL-E     ← 歴史保存壁（既存残置）
```

## 色・線種・線の太さ割当

色・線種・線の太さは **レイヤ名だけでは規定しない**。`drawing-notation.md` のペン割当表（Color-dependent Plot Style / CTB）で一元管理する。レイヤは「何の要素か」のみを表現し、表現ルールは別レイヤで管理。

## 禁止事項 / Prohibitions

- 全角文字・日本語レイヤ名
- スペース混入
- `Layer1`, `TEMP`, `XREF_*` 等の汎用名・自動生成名の残存
- 同一要素の分散（壁を `A-WALL` と `WALL_EXT` に分けない）
- 越側オペによる**独自レイヤ追加**（必要なら RFI 経由で申請）

## AutoCAD／Revit 対応

### AutoCAD
- レイヤテンプレート：`AHA_LayerTemplate.dwt` に本規則を事前登録
- 新規案件は必ず上記テンプレートから開始
- 外部参照（XREF）のレイヤは `XR|<元レイヤ名>` でプレフィックス

### Revit
- Revit はカテゴリベースのため、本規則は **Filter 名** と **Subcategory 名** に適用
- DWG Export 時のマッピング表：`AHA_RevitToDWG_LayerMap.txt`（別途整備）
- View Template で本規則に沿った Filter を設定

## 関連ファイル

- `standards/drawing-notation.md`
- `standards/file-naming.md`
- `standards/revit-family-rules.md`
