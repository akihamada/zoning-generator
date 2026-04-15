# Drawing List / 図面リスト テンプレート v1

> **使い方** / Usage
> - 案件キックオフ時に本ファイルを `projects/[案件コード]/01_Drawing-List.md` へ複製
> - 30% マイルストーン時点で全シートを記入（`checklists/L2-milestone-30-60-90.md` 参照）
> - 図面番号は `standards/file-naming.md` の連番ブロック規則に準拠
> - 更新時は Revision を上げ、変更理由を下部ログに記載

## 案件情報 / Project Info

| 項目 | 内容 |
|---|---|
| 案件名 / Project Name |  |
| 案件コード / Project Code |  |
| クライアント / Client |  |
| 用途 / Use |  |
| 延床 / GFA (m²) |  |
| 階数 / Floors |  |
| 構造 / Structure |  |
| AHA要素 / AHA Items | 3DP / IRR / KIN / SEN / ART / HIS |
| フェーズ / Phase | DD（実施設計） |

## 図面リスト / Drawing List

図面番号は `<Project>-AHA-<Vol>-<Level>-<Type>-<Role>-<Number>` 形式。下表では `<Project>` を `XXXX` と表示。

### 000 系 — 共通・凡例 / General

| 図面番号 | 図面名 JP | Title EN | Scale | Size | Status | Rev | Issue Date | Owner |
|---|---|---|---|---|---|---|---|---|
| XXXX-AHA-ZZ-ZZ-DR-A-0001 | 図面リスト | Drawing List | — | A3 | S0 | P01 |  |  |
| XXXX-AHA-ZZ-ZZ-DR-A-0002 | 一般注記 | General Notes | — | A1 | S0 | P01 |  |  |
| XXXX-AHA-ZZ-ZZ-DR-A-0003 | 共通凡例 | Legend & Symbols | — | A1 | S0 | P01 |  |  |

### 100 系 — 配置・外構 / Site

| 図面番号 | 図面名 JP | Title EN | Scale | Size | Status | Rev | Issue Date | Owner |
|---|---|---|---|---|---|---|---|---|
| XXXX-AHA-ZZ-ZZ-DR-A-0101 | 配置図 | Site Plan | 1:500 | A1 | S0 | P01 |  |  |
| XXXX-AHA-ZZ-ZZ-DR-A-0102 | 外構詳細 | Site Details | 1:100 | A1 | S0 | P01 |  |  |

### 200 系 — 平面 / Plans

| 図面番号 | 図面名 JP | Title EN | Scale | Size | Status | Rev | Issue Date | Owner |
|---|---|---|---|---|---|---|---|---|
| XXXX-AHA-ZZ-00-DR-A-0201 | 1階平面図 | 1F Plan | 1:100 | A1 | S0 | P01 |  |  |
| XXXX-AHA-ZZ-01-DR-A-0202 | 2階平面図 | 2F Plan | 1:100 | A1 | S0 | P01 |  |  |
| XXXX-AHA-ZZ-RF-DR-A-0210 | 屋根伏図 | Roof Plan | 1:100 | A1 | S0 | P01 |  |  |

### 300 系 — 立面 / Elevations

| 図面番号 | 図面名 JP | Title EN | Scale | Size | Status | Rev | Issue Date | Owner |
|---|---|---|---|---|---|---|---|---|
| XXXX-AHA-ZZ-ZZ-DR-A-0301 | 東立面図 | East Elevation | 1:100 | A1 | S0 | P01 |  |  |
| XXXX-AHA-ZZ-ZZ-DR-A-0302 | 西立面図 | West Elevation | 1:100 | A1 | S0 | P01 |  |  |
| XXXX-AHA-ZZ-ZZ-DR-A-0303 | 南立面図 | South Elevation | 1:100 | A1 | S0 | P01 |  |  |
| XXXX-AHA-ZZ-ZZ-DR-A-0304 | 北立面図 | North Elevation | 1:100 | A1 | S0 | P01 |  |  |

### 400 系 — 断面 / Sections

| 図面番号 | 図面名 JP | Title EN | Scale | Size | Status | Rev | Issue Date | Owner |
|---|---|---|---|---|---|---|---|---|
| XXXX-AHA-ZZ-ZZ-DR-A-0401 | A-A' 断面図 | Section A-A' | 1:100 | A1 | S0 | P01 |  |  |
| XXXX-AHA-ZZ-ZZ-DR-A-0402 | B-B' 断面図 | Section B-B' | 1:100 | A1 | S0 | P01 |  |  |

### 500 系 — 矩計・詳細断面 / Wall Sections

| 図面番号 | 図面名 JP | Title EN | Scale | Size | Status | Rev | Issue Date | Owner |
|---|---|---|---|---|---|---|---|---|
| XXXX-AHA-ZZ-ZZ-DR-A-0501 | 矩計図（外壁標準部） | Wall Section (Std) | 1:20 | A1 | S0 | P01 |  |  |

### 600 系 — 部分詳細 / Details

（60% 時点で詳細化）

### 700 系 — 建具・仕上表 / Schedules

| 図面番号 | 図面名 JP | Title EN | Scale | Size | Status | Rev | Issue Date | Owner |
|---|---|---|---|---|---|---|---|---|
| XXXX-AHA-ZZ-ZZ-SH-A-0701 | 建具表 | Door & Window Schedule | — | A1 | S0 | P01 |  |  |
| XXXX-AHA-ZZ-ZZ-SH-A-0702 | 仕上表 | Finish Schedule | — | A1 | S0 | P01 |  |  |

### 800 系 — 家具・造作 / Furniture

（該当時）

### 900 系 — AHA 特殊要素 / AHA-Specific

該当要素がある場合のみ以下を追加。Role コードは `3DP`, `IRR`, `KIN`, `SEN`, `ART`, `HIS` から選択。

| 図面番号 | 図面名 JP | Title EN | Scale | Size | Status | Rev | Issue Date | Owner |
|---|---|---|---|---|---|---|---|---|
| XXXX-AHA-ZZ-ZZ-DR-3DP-0901 | 3Dプリント壁部材図 | 3D Print Wall Components | 1:50 | A1 | S0 | P01 |  |  |

## 集計 / Summary

| 分類 | 枚数 / Count |
|---|---|
| 000 系（共通） |  |
| 100 系（配置） |  |
| 200 系（平面） |  |
| 300 系（立面） |  |
| 400 系（断面） |  |
| 500 系（矩計） |  |
| 600 系（詳細） |  |
| 700 系（建具・仕上） |  |
| 800 系（造作） |  |
| 900 系（AHA特殊） |  |
| **合計** |  |

## 更新履歴 / Revision Log

| Rev | Date | Description | Updated by |
|---|---|---|---|
| P01 |  | Initial | PM |
