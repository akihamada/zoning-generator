# LOD Matrix / LOD 定義表 テンプレート v1

> **使い方** / Usage
> - 案件キックオフ時に本ファイルを `projects/[案件コード]/02_LOD-Matrix.md` へ複製
> - 要素ごとの目標 LOD を各フェーズで設定
> - AHA 特殊要素（3DP / IRR / KIN / SEN / ART / HIS）は通常より **1段階上** を目標とする
> - 参照：`standards/revit-family-rules.md` の LOD 定義

## 案件情報 / Project Info

| 項目 | 内容 |
|---|---|
| 案件コード / Project Code |  |
| 基本設計完了 / SD Complete |  |
| 実施着手 / DD Start |  |
| 30% マイルストーン |  |
| 60% マイルストーン |  |
| 90% マイルストーン |  |
| 出図予定 / Issue Date |  |

## LOD 定義（参考） / LOD Definition (Reference)

| LOD | 幾何 / Geometry | 情報 / Information | 典型用途 |
|---|---|---|---|
| 100 | 概念マッシング | 用途・面積のみ | 構想 |
| 200 | マッシング | 種別のみ | 基本設計 |
| 300 | スケマティック | 寸法確定 | 実施設計初期 |
| 350 | 接合部定義済 | 他工種インターフェース | 実施設計後半 |
| 400 | 製作対応 | 製作情報完備 | 施工図 |
| 500 | 竣工反映 | 実測値反映 | As-built |

## 要素別 LOD マトリクス / Element LOD Matrix

フェーズ列に目標 LOD を記入。空欄は対象外。

### 意匠 / Architecture

| 要素 / Element | SD完了 | DD 30% | DD 60% | DD 90% | 備考 |
|---|---|---|---|---|---|
| 外壁 / Exterior Walls | 200 | 300 | 350 | 400 |  |
| 内壁 / Interior Walls | 200 | 300 | 350 | 400 |  |
| 床 / Floors | 200 | 300 | 350 | 400 |  |
| 天井 / Ceilings | 200 | 300 | 350 | 400 |  |
| 屋根 / Roofs | 200 | 300 | 350 | 400 |  |
| 建具（ドア）/ Doors | 200 | 300 | 350 | 400 |  |
| 建具（窓）/ Windows | 200 | 300 | 350 | 400 |  |
| 階段 / Stairs | 200 | 300 | 350 | 400 |  |
| 手摺 / Railings | 200 | 300 | 350 | 400 |  |
| 家具・造作 / Furniture | — | 200 | 300 | 350 |  |
| 仕上げ / Finishes | 200 | 300 | 350 | 400 |  |

### 構造 / Structure

| 要素 / Element | SD完了 | DD 30% | DD 60% | DD 90% | 備考 |
|---|---|---|---|---|---|
| 柱 / Columns | 200 | 300 | 350 | 400 |  |
| 梁 / Beams | 200 | 300 | 350 | 400 |  |
| スラブ / Slabs | 200 | 300 | 350 | 400 |  |
| 基礎 / Foundations | 200 | 300 | 350 | 400 |  |
| ブレース / Bracing | — | 200 | 300 | 350 |  |

### 設備 / MEP

| 要素 / Element | SD完了 | DD 30% | DD 60% | DD 90% | 備考 |
|---|---|---|---|---|---|
| ダクト / Ducts | — | 200 | 300 | 350 |  |
| 配管 / Pipes | — | 200 | 300 | 350 |  |
| 機器 / Equipment | 100 | 200 | 300 | 350 |  |
| 照明 / Lighting | — | 200 | 300 | 350 |  |

### AHA 特殊要素 / AHA-Specific

**ポリシー**：通常要素より **1段階上** の LOD を目標とする。該当要素のみ記入。

| 要素 / Element | SD完了 | DD 30% | DD 60% | DD 90% | 備考 |
|---|---|---|---|---|---|
| 3Dプリント部材 / 3D Print | 300 | 350 | 400 | 400 | 材料配合・層厚・印字方向必須 |
| 異形ジオメトリ / Irregular | 300 | 350 | 400 | 400 | Rhino 原型管理必須 |
| キネティック / Kinetic | 200 | 300 | 350 | 400 | 機構図・電源・制御 |
| センサー / Sensor | — | 200 | 300 | 350 | 型番・配線・データ先 |
| デジタルアート / Art | — | 200 | 300 | 350 | インターフェース仕様 |
| 歴史保存 / Historic | 200 | 300 | 350 | 400 | 保存区分・許容乖離 |

## ファミリ管理 / Family Management

`standards/revit-family-rules.md` に沿ったファミリ命名・パラメータ必須。

| ファミリ名 / Family Name | カテゴリ / Category | LOD | 起源 / Source | 備考 |
|---|---|---|---|---|
|  |  |  |  |  |

## 更新履歴 / Revision Log

| Rev | Date | Description | Updated by |
|---|---|---|---|
| P01 |  | Initial | PM |
