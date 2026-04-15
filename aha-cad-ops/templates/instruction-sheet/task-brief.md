# Task Brief / 指示書テンプレート v1

> **使い方** / Usage
> - PMがタスクごとに本ファイルを複製し、`projects/[案件コード]/instructions/` に配置
> - 上段（1〜9）をPMが記入、下段（10〜11）をVN側が記入してPMへ返送
> - ファイル名：`TB-<案件コード>-<YYYYMMDD>-<連番>.md`（例：`TB-ARIA-20250414-001.md`）
> - 日英併記 / JP-EN bilingual

---

## 1. 基本情報 / Metadata

| 項目 | Item | 内容 / Content |
|---|---|---|
| Task ID |  |  |
| 案件コード / Project Code |  |  |
| 発行日 / Issue Date (JST) |  |  |
| 期限 / Due Date (JST) |  |  |
| 発行者 / Issued by (PM) |  |  |
| 担当者 / Assigned to (VN) |  |  |
| 優先度 / Priority | — | High / Medium / Low |

## 2. タスク種別 / Task Type

- [ ] 新規作図 / New drawing
- [ ] 改訂 / Revision
- [ ] ディテール作成 / Detail creation
- [ ] ファミリ作成・編集 / Family creation / edit
- [ ] スケジュール・表更新 / Schedule / table update
- [ ] その他 / Other: ______

## 3. スコープ / Scope

**何をするか** / What to do:
（一文で。例：「2階平面図に家具レイアウトを反映し、寸法を確定する」）

**何をしないか** / What NOT to do:
（例：「構造通り芯は変更しない」「他階には触らない」）

## 4. 対象図面 / Target Drawings

| 図面番号 / Drawing No. | 図面名 / Title | 現状 / Status |
|---|---|---|
|  |  | S0 / S1 / S2 / S3 / S4 / A1 |

## 5. 入力資料 / Inputs

必要な参照ファイル・資料を以下に列挙：

| 種別 / Type | パス or URL / Path | 備考 / Notes |
|---|---|---|
| 参考図 / Reference drawing |  |  |
| 仕様書 / Specification |  |  |
| 過去案件ディテール / Detail library ID |  |  |
| 構造・設備図 / Structural / MEP drawing |  |  |
| 議事録 / Meeting minutes |  |  |

## 6. 成果物 / Deliverables

- [ ] DWG ファイル（命名規則準拠）
- [ ] RVT ファイル（該当時）
- [ ] PDF（A1 / A2 / A3 指定：______）
- [ ] 変更箇所の改訂雲書き / Revision clouds
- [ ] その他 / Other: ______

**保存先** / Save location:
`projects/[案件コード]/04_Drawings/...`

## 7. LOD 目標 / LOD Target

| 要素 / Element | 現在LOD / Current | 目標LOD / Target |
|---|---|---|
|  |  |  |

参照：`projects/[案件コード]/02_LOD-Matrix.md`

## 8. 参照規約 / Standards References

以下の規約を遵守：

- [ ] `standards/file-naming.md` (ISO 19650-2)
- [ ] `standards/layer-naming.md` (ISO 13567)
- [ ] `standards/drawing-notation.md`
- [ ] `standards/revit-family-rules.md`（Revit 作業時）
- [ ] `checklists/L3-pre-issue.md`（出図関連）
- [ ] `checklists/L4-aha-specific.md` の該当セクション（AHA 特殊要素を含む場合）

## 9. 禁止事項 / Prohibitions

- 構造通り芯の独断変更禁止 / No unilateral changes to structural grid
- 独自レイヤ追加禁止（必要なら RFI） / No new layers without RFI
- Shared Parameters の独自追加禁止 / No custom Shared Parameters
- 原型 Rhino ファイルの直接編集禁止 / Do NOT edit Rhino master files
- 追加 / Additional: ______

---

## 10. VN 側セルフチェック / VN Self-Check

完了後、VN側オペが以下を記入してPMへ返送：

- [ ] 成果物を指定パスに保存した / Saved to specified path
- [ ] ファイル命名が `standards/file-naming.md` 準拠 / File names compliant
- [ ] 線・ペン・レイヤが `standards/` 準拠 / Lines / pens / layers compliant
- [ ] 寸法・記号・注記を確認した / Dimensions / symbols / notes verified
- [ ] `checklists/L3-pre-issue.md` の該当項目を確認した / L3 items checked
- [ ] 不明点は RFI で PM に照会した / All unclear points raised as RFI

**作業時間** / Hours spent: ______ h
**完了日時** / Completed at (ICT): ______
**コメント** / Notes:


## 11. PM レビュー / PM Review

- [ ] 指示通りに完了 / Completed as instructed
- [ ] 再作業必要 / Revision required → 指示内容: ______
- [ ] 部分完了・追加作業指示 / Partial, additional instructions: ______

**レビュー日時** / Reviewed at (JST): ______
**レビュー結果** / Result: Approved / Revision Required / Partial
**コメント** / Comments:


---

## 関連 / Related

- Drawing List: `projects/[案件コード]/01_Drawing-List.md`
- LOD Matrix: `projects/[案件コード]/02_LOD-Matrix.md`
- Instruction Log: `projects/[案件コード]/04_Instruction-Log.md`
- RFI Log: `projects/[案件コード]/05_RFI-Log.md`
