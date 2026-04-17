# AHA CAD Operations — 運用ガイド

> **Aki Hamada Architects（AHA）× ベトナムCADオペレーター外注** を支える管理システム。
> 若手でも迷わず実施設計図の品質を担保できるよう、指示・チェック・標準・ディテールを一箇所にまとめている。

---

## このシステムで何ができるか

- ✅ **指示の精度を仕組みで担保**：1タスク1指示書、日英併記、セルフチェック付き
- ✅ **品質の階層管理**：L1〜L4 チェックリストで段階ごとの抜けを防ぐ
- ✅ **暗黙知を形式知化**：社内標準・ディテール・過去案件を検索可能に
- ✅ **越側オンボーディング**：英語の標準ガイドで初日から動ける
- ✅ **AHA特性の織り込み**：土3DP／異形／キネティック／アート統合／歴史保存を別枠で管理

---

## 5分で全体像

```
aha-cad-ops/
├── README.md          ← 📖 あなたは今ここ（人間向け）
├── CLAUDE.md          ← 🤖 Claude Code 用の文脈
│
├── standards/         ← 📐 社内標準（命名・表記・ファミリ）
├── checklists/        ← ✅ L1〜L4 品質チェック
├── templates/         ← 📋 指示書・RFI・図面リスト・LOD表
├── detail-library/    ← 🗂️ 再利用ディテールDB
├── onboarding-vn/     ← 🇻🇳 越側オペ向け英語資料
│
├── projects/          ← 🏗️ 案件別ワークスペース
│   └── SAMPLE-001/    ← 📝 新規案件の雛形
│
├── feedback-log/      ← 📊 頻出ミス・現場フィードバック
└── scripts/           ← 🔧 Dynamo / GH 自動化
```

**パスの記述ルール**：本システム内の文書では、すべてのパスは **`aha-cad-ops/` からの相対パス** で表記する（例：`standards/file-naming.md`）。

---

## 役割別スタートガイド

自分の役割を選んで開始。

### 👤 日本側PM — 案件の要

**新規案件のキックオフ手順**

1. `checklists/L1-basic-to-detail.md` を開く
2. 案件コードを決定（4文字英大文字、例：`ARIA`）
3. サンプル案件をコピー：
   ```
   cp -r projects/SAMPLE-001 projects/<CODE>
   ```
4. `projects/<CODE>/CLAUDE.md` に案件情報記入
5. `01_Drawing-List.md` / `02_LOD-Matrix.md` を埋める
6. キックオフ会議実施（`03_Kickoff-Notes.md` に記録）
7. L1 完了サインを取得
8. 越側オペに `onboarding-vn/` を送付

**毎日の指示サイクル**

| 時刻（JST） | やること |
|---|---|
| 17:00 | 今日の VN 成果物をレビュー → `04_Instruction-Log.md` 更新 |
| 18:00 | 明日の指示を `templates/instruction-sheet/task-brief.md` から複製・記入 |
| 18:00 | `projects/<CODE>/instructions/TB-<CODE>-<日付>-<連番>.md` で保存、Slack 通知 |
| 17-18 | overlap time で VN の緊急 RFI に対応（このウィンドウが唯一のリアルタイム） |
| 翌 09:00 | VN 返却物を確認 → task-brief の PM Review 欄記入 |
| 翌 09-11 | High 優先度 RFI に回答、`05_RFI-Log.md` 更新 |

**マイルストーンで**

- 30%・60%・90% → `checklists/L2-milestone-30-60-90.md`
- 出図3日前 → `checklists/L3-pre-issue.md`（全項目 PASS 必須）
- AHA特殊要素 → `checklists/L4-aha-specific.md`（常時参照）

---

### 🎨 設計リーダー — AHAらしさの守護者

**キックオフで決めること**

- [ ] この案件に含まれる AHA 特殊要素（3DP / IRR / KIN / SEN / ART / HIS）
- [ ] `checklists/L4-aha-specific.md` のどのセクションが適用されるか
- [ ] `detail-library/index.md` から再利用候補を抽出
- [ ] AHA 特殊要素の LOD は通常より **1段階上** に設定（`02_LOD-Matrix.md`）

**マイルストーンごと**

- 30 / 60 / 90% で L4 該当項目を確認
- L3 で AHA 要素の全 PASS を承認
- 案件終了後、再利用ディテールを `detail-library/items/` に登録

---

### 🌱 若手スタッフ — この仕組みの主役

**最初に読む順番**（合計約1.5時間）

1. この README を全部（5 min）
2. `CLAUDE.md` の「AHAの設計特性」（5 min）
3. `standards/` 4ファイル全部（30 min）
4. `checklists/` L1〜L4（30 min）
5. `templates/` を眺める（10 min）
6. `detail-library/index.md`（5 min）

**日々の学習ループ**

- パイロット案件で PM や設計リーダーを shadow
- `checklists/L3-pre-issue.md` を自分で実行する練習
- `detail-library/` から類似ディテールを探す
- `feedback-log/common-mistakes.md` を週1回眺める（他人のミスから学ぶ）
- 疑問は RFI 形式で書いて PM に提出（フォーマット練習にも有効）

---

### 🇻🇳 越側 CAD オペ

→ **`onboarding-vn/README.md` を開いてください。**

---

## 標準ワークフロー

### 案件ライフサイクル

```
[基本設計完了]
      │
      ▼
  L1: 基本→実施移行
  ・スコープ凍結 ・入力資料固定 ・体制整備 ・AHA要素特定
      │
      ▼
[実施設計開始]
      │
      ├─ 30% ゲート → L2 30% セクション（図枠・通り芯・骨格）
      ├─ 60% ゲート → L2 60% セクション（寸法・表・ディテール）
      ├─ 90% ゲート → L2 90% セクション（最終クラッシュ・整合）
      │
      ▼
[出図3日前]
      │
      ▼
  L3: 出図前最終（線・寸法・整合・PDF・命名・L4全PASS）
      │
      ▼
[出図]
      │
      ▼
[施工フィードバック] → feedback-log/monitoring-findings.md
                       → 次案件に反映
```

### 日本-越の日次サイクル

```
JST      ICT
─────    ─────
17:00    15:00   PM: 今日のVN成果をレビュー
18:00    16:00   PM: 明日の task-brief を発行（Slack 通知）
                 VN: ブリーフ確認、緊急RFIはこのタイミング
18-19    16-17   ★ overlap time（唯一のリアルタイム窓） ★
19:00    17:00   PM EOD / VN EOD

翌日
09:00    07:00   PM: VN 返却物を確認、High RFI に回答
11:00    09:00   VN: PM 回答受領、次に進む
```

---

## よくある質問

**Q1. 新規案件を始めるには？**
→ 上の「日本側PM → 新規案件のキックオフ手順」を順番に実施。`projects/SAMPLE-001/` のクローンから始めれば迷わない。

**Q2. 指示書は毎回1から書くの？**
→ いいえ。`templates/instruction-sheet/task-brief.md` を複製して埋めるだけ。

**Q3. 越側から質問が来たら？**
1. RFI フォーマットなら PM 回答欄に記入して返却
2. 規約の曖昧さが原因なら `standards/` を更新
3. 同じミスが2回以上なら `feedback-log/common-mistakes.md` に記録 → 該当 L1〜L4 項目を強化

**Q4. ディテールの再利用手順は？**
→ `detail-library/index.md` で検索 → 該当 `items/<ID>/` を案件にコピー → `reuse_count` を更新。

**Q5. AHA 特殊要素を含む案件の LOD は？**
→ 通常 LOD より **1段階上**。例：一般壁が 60% で LOD350 なら、3DP 壁は LOD400。

**Q6. 規約が現実と合わなくなったら？**
→ Slack で合意 → `standards/*.md` を更新（PR レビュー） → 関連チェックリストも同時更新 → 越側に通知。

**Q7. Claude Code で作業させるには？**
→ このディレクトリで Claude Code を起動。`CLAUDE.md` を自動で読むので、「新規案件 ABCD の雛形作って」「指示書のドラフト作って」等を自然言語で依頼可能。

---

## ファイル一覧（詳細）

### 📐 社内標準

| ファイル | 用途 | 準拠規格 |
|---|---|---|
| `standards/file-naming.md` | ファイル命名 | ISO 19650-2 |
| `standards/layer-naming.md` | レイヤ命名 | ISO 13567 |
| `standards/drawing-notation.md` | 線・文字・寸法・記号 | 社内 + JIS/ISO |
| `standards/revit-family-rules.md` | Revit ファミリ作成 | 社内標準 |

### ✅ チェックリスト

| ファイル | 用途 | 実施タイミング |
|---|---|---|
| `checklists/L1-basic-to-detail.md` | 基本→実施移行 | 実施着手時 1回 |
| `checklists/L2-milestone-30-60-90.md` | 中間ゲート | 30 / 60 / 90 % |
| `checklists/L3-pre-issue.md` | 出図前最終 | 出図 3日前 |
| `checklists/L4-aha-specific.md` | AHA特殊要素 | 該当時、常時 |

### 📋 テンプレート

| ファイル | 用途 |
|---|---|
| `templates/instruction-sheet/task-brief.md` | タスク指示書（1タスク1ブリーフ） |
| `templates/rfi/rfi-form.md` | 質問票 |
| `templates/drawing-list/drawing-list.md` | 図面リスト |
| `templates/lod-matrix/lod-matrix.md` | LOD 定義表 |

### 🗂️ ディテール・フィードバック

| ファイル | 用途 |
|---|---|
| `detail-library/index.md` | ディテール総目録 |
| `feedback-log/common-mistakes.md` | 越側頻出ミス類型集 |
| `feedback-log/monitoring-findings.md` | 現場・施工段階フィードバック |

### 🇻🇳 越側オンボーディング

| ファイル | 用途 |
|---|---|
| `onboarding-vn/README.md` | 入口 |
| `onboarding-vn/01-welcome-and-workflow.md` | AHA 紹介・役割・ツール |
| `onboarding-vn/02-standards-quick-reference.md` | 標準の英語要約 |
| `onboarding-vn/03-checklists-quick-reference.md` | チェックリストの英語要約 |
| `onboarding-vn/04-daily-cycle.md` | 日次サイクル詳細 |
| `onboarding-vn/05-glossary-jp-en-vi.md` | 日英越用語集 |

### 🏗️ 案件

| ファイル | 用途 |
|---|---|
| `projects/SAMPLE-001/` | サンプル案件（新規案件の雛形） |
| `projects/<CODE>/CLAUDE.md` | 案件別 Claude 文脈 |
| `projects/<CODE>/01_Drawing-List.md` | 案件の図面リスト |
| `projects/<CODE>/02_LOD-Matrix.md` | 案件の LOD 表 |
| `projects/<CODE>/03_Kickoff-Notes.md` | キックオフ議事録 |
| `projects/<CODE>/04_Instruction-Log.md` | 指示書履歴 |
| `projects/<CODE>/05_RFI-Log.md` | RFI 履歴 |

---

## 困ったら

| 症状 | どこを見る |
|---|---|
| 新規案件の始め方がわからない | この README「日本側PM」セクション |
| ファイル名がわからない | `standards/file-naming.md` |
| レイヤ名がわからない | `standards/layer-naming.md` |
| 線の太さがわからない | `standards/drawing-notation.md` |
| チェック漏れが不安 | `checklists/L3-pre-issue.md` |
| AHA特殊要素の対応 | `checklists/L4-aha-specific.md` |
| 過去ディテールを探したい | `detail-library/index.md` |
| 越側への英語説明 | `onboarding-vn/` 一式 |
| それでもわからない | Slack で PM にエスカレーション |

---

## 更新・貢献

- 規約変更：Slack で合意 → 該当 `standards/*.md` を修正 → 関連チェックリストも同時更新
- ミス記録：即日 `feedback-log/common-mistakes.md` に追記
- ディテール追加：案件終了後、PM が判定 → `detail-library/items/` に登録
- この README 自体の改善：気づいたら直ちに修正提案

---

最終更新：2025-04-14（v1 初版）
