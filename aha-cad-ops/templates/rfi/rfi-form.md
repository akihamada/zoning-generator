# RFI — Request for Information / 質問票テンプレート v1

> **使い方** / Usage
> - VN側オペが不明点を発見した時点で本ファイルを複製
> - ファイル名：`RFI-<案件コード>-<YYYYMMDD>-<連番>.md`
> - Slack の該当チャンネルにもサマリを投下（全文はリポジトリ内）
> - PM は **翌朝レビュー時までに** 回答、High 優先度は **当日中**

---

## 1. 基本情報 / Metadata

| 項目 | Item | 内容 / Content |
|---|---|---|
| RFI ID |  |  |
| 案件コード / Project Code |  |  |
| 発行日 / Issue Date (ICT) |  |  |
| 発行者 / Raised by (VN) |  |  |
| 優先度 / Priority | — | High / Medium / Low |
| 期限 / Response Due |  |  |

### 優先度定義 / Priority Definition

- **High**：回答がないと作業停止、出図遅延リスクあり。**当日中回答**（Same-day response）
- **Medium**：次工程に影響。**翌朝レビュー時回答**（Next-morning response）
- **Low**：情報確認・将来作業向け。**週次まとめ回答**可（Weekly batch response）

## 2. カテゴリ / Category

- [ ] 設計意図 / Design intent
- [ ] 仕様 / Specification
- [ ] 寸法 / Dimensions
- [ ] ディテール / Detail
- [ ] 規約 / Standards (naming / layer / notation)
- [ ] ツール / Tools (Revit / AutoCAD / Rhino)
- [ ] その他 / Other: ______

## 3. 影響範囲 / Affected Scope

| 図面番号 / Drawing No. | 影響 / Impact |
|---|---|
|  |  |

関連タスク / Related task: `TB-______`

## 4. 質問 / Question

**背景** / Background:
（何をしていて、どこで不明点に遭遇したか）

**質問** / Question:
（具体的に。できれば Yes/No または選択肢形式）

**添付** / Attachments:
- スクリーンショット：`rfi-attachments/RFI-___/`
- 該当図面の該当箇所ハイライト

## 5. 自己判断案 / Attempted Interpretation

質問者の現時点での解釈・候補：

**案A** / Option A:

**案B** / Option B:

**推奨** / Preferred: A / B / 判断できない（Cannot decide）

## 6. 未解決時の影響 / Impact if Unresolved

- 作業停止する要素 / Blocked elements:
- 代替で進められる作業 / Workarounds available:
- 遅延リスク / Delay risk (hours):

---

## 7. PM 回答 / PM Response

| 項目 | Item | 内容 / Content |
|---|---|---|
| 回答者 / Responded by |  |  |
| 回答日時 / Responded at (JST) |  |  |

**回答** / Answer:


**根拠** / Reasoning:
（どの仕様書・ディテール・過去案件を根拠に判断したか）


**追加指示** / Additional instructions:


**規約・チェックリストへの反映要否** / Update standards / checklists?
- [ ] 必要 / Required → 反映先: `standards/______` / `checklists/L______`
- [ ] 不要 / Not required

## 8. 決着 / Resolution

- [ ] VN側が回答を確認・作業再開 / VN confirmed and resumed
- [ ] 次の指示書に反映済 / Reflected in next task brief
- [ ] `feedback-log/common-mistakes.md` に記録 / Logged to common-mistakes

**クローズ日時** / Closed at:
