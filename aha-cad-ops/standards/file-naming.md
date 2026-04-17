# ファイル命名規則 / File Naming Convention

> **一言で** / TL;DR
> 全ファイルは `<Project>-<Originator>-<Volume>-<Level>-<Type>-<Role>-<Number>[-<Status>-<Rev>]` 形式。
> 例：`ARIA-AHA-ZZ-01-DR-A-0201-S2-P03.dwg`
>
> **誰が読む**：PM（案件コード決定時）／越側オペ（毎日参照）／若手（全体理解用）

**準拠規格**：ISO 19650-2（情報マネジメント／CDE）をベースに、AHA運用に合わせて拡張。

## 基本構造 / Base Structure

```
<Project>-<Originator>-<Volume>-<Level>-<Type>-<Role>-<Number>[-<Status>-<Revision>]
```

例 / Example:
```
ARIA-AHA-ZZ-01-DR-A-0101-S2-P01
```

## フィールド定義 / Field Definitions

| 位置 | フィールド | 内容 | 例 |
|---|---|---|---|
| 1 | Project | 案件コード（4文字以内、英大文字） | `ARIA`, `TGIN`, `MUSE` |
| 2 | Originator | 発信組織 | `AHA`（自社）／他はコンサル略号 |
| 3 | Volume/System | 棟／ゾーン番号、全体は `ZZ` | `ZZ`, `01`, `A` |
| 4 | Level/Location | 階／位置、全体は `ZZ`、地階は `B1`〜、GLは `00` | `ZZ`, `00`, `01`, `RF` |
| 5 | Type | 情報種別（下表） | `DR`, `M3`, `SH` |
| 6 | Role | 分野（下表） | `A`, `S`, `M`, `E`, `P` |
| 7 | Number | 連番（4桁） | `0101` |
| 8 | Status *(任意)* | 成熟度コード（下表） | `S2`, `A1` |
| 9 | Revision *(任意)* | `P`＋2桁（設計段階）、`C`＋2桁（施工段階） | `P01`, `C02` |

## Type（情報種別）コード

| コード | 意味 |
|---|---|
| `DR` | 2D Drawing（図面） |
| `M2` | 2D Model |
| `M3` | 3D Model（Rhino/Revit 原型含む） |
| `SH` | Schedule（建具表・仕上表・面積表等） |
| `SP` | Specification（仕様書） |
| `RP` | Report |
| `CM` | Communication（議事録・RFI） |
| `PH` | Photograph |
| `RD` | Render |
| `VS` | Visualization（VR／動画） |

## Role（分野）コード

| コード | 意味 |
|---|---|
| `A` | Architecture |
| `S` | Structure |
| `M` | Mechanical（空調・衛生） |
| `E` | Electrical |
| `P` | Plumbing |
| `L` | Landscape |
| `C` | Civil |
| `I` | Interior |
| `F` | Facade / Envelope |
| `X` | Cross-discipline（統合図） |

### AHA 拡張 Role

通常分野で表現できないAHA特殊要素は以下を Role 位置に使用：

| コード | 意味 |
|---|---|
| `3DP` | 土系3Dプリント関連 |
| `IRR` | 異形形態／自由曲面 |
| `KIN` | キネティック要素 |
| `SEN` | センサー統合 |
| `ART` | デジタルアート統合 |
| `HIS` | 歴史建築保存・修復 |

例：`ARIA-AHA-ZZ-01-DR-3DP-0101-S2-P01`

## Status（成熟度）コード — ISO 19650-2

| コード | 意味 |
|---|---|
| `S0` | Initial status / Work in Progress |
| `S1` | Suitable for Coordination |
| `S2` | Suitable for Information |
| `S3` | Suitable for Internal Review & Comment |
| `S4` | Suitable for Stage Approval |
| `A1` | Authorized for Construction |
| `B1` | Partial Sign-off |

## Number（連番）ブロック割当

実施設計図の連番は以下のブロックで割当、越側との共通理解を固定する。

| 範囲 | 用途 |
|---|---|
| 0000〜0099 | 図面リスト・共通凡例・General Notes |
| 0100〜0199 | 配置図・外構 |
| 0200〜0299 | 平面図 |
| 0300〜0399 | 立面図 |
| 0400〜0499 | 断面図 |
| 0500〜0599 | 矩計・詳細断面 |
| 0600〜0699 | 部分詳細・ディテール |
| 0700〜0799 | 建具表・仕上表 |
| 0800〜0899 | 家具・造作 |
| 0900〜0999 | AHA特殊要素（3DP／IRR／KIN／ART／HIS） |

## 運用ルール

- すべて **英大文字**、セパレータは **ハイフン** のみ
- スペース・日本語・機種依存文字は禁止
- 案件開始時に `projects/[案件コード]/CLAUDE.md` 内に Project Code を確定記載
- 案件固有の略号追加は PM 承認必須
- 過去版は `_archive/` フォルダへ移動し、ファイル名は**変更しない**（履歴トレーサビリティ）

## 越側オペへの指示例 / Instruction to VN Operator

```
> Save as: ARIA-AHA-ZZ-01-DR-A-0201-S2-P03.dwg
> Location: 04_Drawings/Plans/
> Do NOT change filename after PM approval.
> If you need a new code, raise RFI (do not invent).
```

## 関連ファイル

- `standards/layer-naming.md`
- `standards/drawing-notation.md`
- `CLAUDE.md`
