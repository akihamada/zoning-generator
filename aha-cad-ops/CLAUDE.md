# CLAUDE.md — AHA CAD Operations

> **👤 人間の方へ** — 運用の始め方・使い方は **[`README.md`](./README.md)** を参照。役割別のクイックスタートがあります。
> **🤖 Claude Code（AI）** — 本ファイルはセッション開始時に自動で読み込まれる文脈です。

Aki Hamada Architects（AHA）のベトナムCADオペレーター外注運用を支える管理システム。Claude Code はこのファイルをセッション開始時に読み、以下の文脈で作業する。

## 目的

1. 越側CADオペへの指示精度を仕組みで担保
2. 若手スタッフの実施図スキル底上げ（暗黙知の形式知化）
3. 案件横断で再利用可能なディテール・チェックリストDB構築

## ディレクトリ構成

```
aha-cad-ops/
├── CLAUDE.md                    # このファイル
├── templates/                   # テンプレート集
│   ├── instruction-sheet/       # 指示書
│   ├── rfi/                     # 質問票
│   ├── drawing-list/            # 図面リスト
│   └── lod-matrix/              # LOD定義表
├── checklists/                  # 品質チェックリスト
│   ├── L1-basic-to-detail.md    # 基本→実施移行時
│   ├── L2-milestone-30-60-90.md # 中間チェック（30/60/90%）
│   ├── L3-pre-issue.md          # 出図前最終
│   └── L4-aha-specific.md       # AHA特有要素
├── standards/                   # 社内標準
│   ├── drawing-notation.md      # 表記マニュアル
│   ├── layer-naming.md          # レイヤ命名（ISO 13567ベース）
│   ├── file-naming.md           # ファイル命名（ISO 19650ベース）
│   └── revit-family-rules.md    # ファミリ作成ルール
├── detail-library/              # 再利用ディテールDB
│   └── index.md
├── projects/                    # 案件別ワークスペース
│   └── SAMPLE-001/              # サンプル案件構成（テンプレ兼参照）
├── feedback-log/                # 運用フィードバック
│   ├── common-mistakes.md       # 越側頻出ミス
│   └── monitoring-findings.md   # 現場フィードバック
├── onboarding-vn/               # 越側オンボーディング資料（英語）
│   ├── README.md
│   ├── 01-welcome-and-workflow.md
│   ├── 02-standards-quick-reference.md
│   ├── 03-checklists-quick-reference.md
│   ├── 04-daily-cycle.md
│   └── 05-glossary-jp-en-vi.md
└── scripts/                     # Dynamo/GH自動化
```

## 体制前提

| 項目 | 内容 |
|---|---|
| 日本側窓口PM | 1名固定 |
| 越側CADオペ | 初期1〜2名（エージェント経由） |
| 時差 | 日本 -2h（夕方指示→翌朝レビュー） |
| コミュニケーション | Slack + Notion + Google Drive |
| 言語 | 指示書・チェックリストは日英併記 |

## AHAの設計特性（全作業で必ず考慮）

- **コア概念**：Hyper Naturalism / Computing Wildness
- **特殊技術要素**：
  - 土系3Dプリント（繊維補強＋酸化Mg系）
  - 異形形態（Rhino ↔ Revit 往復ワークフロー）
  - キネティック／センサー／デジタルアート統合
- **主要案件タイプ**：パビリオン／歴史建築リノベ（旧高岡共立銀行等）／リゾートヴィラ／ミュージアム
- **図面特性**：一品生産ディテール比率が高い → LOD管理と指示粒度は通常事務所より高く設定

## 作業依頼の型（Claude への指示はこのどれかに該当）

### A. テンプレート作成・改訂
- 既存類似テンプレを `templates/` 配下で先に確認
- 日本語＋英語併記（越側が英語運用の場合）
- Markdown形式、PDF化想定のレイアウト

### B. チェックリスト作成・更新
- 階層（L1〜L4）を明示
- 各項目は「誰が／いつ／何を確認」の3要素
- チェック欄（`- [ ]`）付き

### C. 案件別セットアップ
- `projects/[案件コード]/` 新規作成
- 指示書・図面リスト・LOD表・スケジュール初期セット生成
- 案件特性（用途・規模・特殊要素）をヒアリングしてカスタマイズ

### D. フィードバック蓄積
- `feedback-log/common-mistakes.md` に類型化して追記
- 再発防止のチェックリスト項目に反映（どのL何番に追加したか明記）

### E. スクリプト開発
- Revit Dynamo / Rhino Grasshopper Python
- 対象：建具表・仕上表・面積表・整合チェック自動化
- 既存スクリプト流用可否を先に確認

## 出力スタイル

- 冗長な前置き・挨拶は不要、本題から
- 曖昧な形容詞・無根拠な数字は避ける
- 不明点は推測せず確認質問を返す
- 長文は階層的に構造化（見出し・表・箇条書き）
- 日本語ベース、図面用語・システム用語は英語併記可

## NG

- 既存ファイルの無断上書き（必ず差分提示→承認後反映）
- テンプレの一般論化（AHA案件特性を必ず織り込む）
- 法規・構造・設備の断定的判断（該当専門家確認を促す）

## 参照規格

| 対象 | 参照規格 | 参照ファイル |
|---|---|---|
| ファイル命名 | ISO 19650-2 | `standards/file-naming.md` |
| レイヤ命名 | ISO 13567 | `standards/layer-naming.md` |
| 図面表記 | 社内標準＋JIS/ISO | `standards/drawing-notation.md` |
| Revitファミリ | AHA 社内標準 | `standards/revit-family-rules.md` |

## 開始時アクション（Claude 向け）

新規セッションで依頼を受けたら：

1. 現在のディレクトリ状態を確認（`ls -la`）
2. 未整備項目を下記「現在のフェーズ」に照らして報告
3. 次の着手候補を3つ優先度付きで提案
4. ユーザの判断を待って作業開始

## 現在のフェーズ

初期構築期。進行順：

1. ✅ 運用設計の合意
2. ✅ ディレクトリ構成の初期化
3. ✅ チェックリストL1〜L4の初版
4. ✅ 表記マニュアル・命名規則の策定
5. ✅ 指示書テンプレv1作成（task-brief / rfi-form / drawing-list / lod-matrix）
6. 🟡 パイロット案件試験運用（SAMPLE-001 構成完成、実案件適用待ち）
7. ⬜ ディテールDB初期構築（目標100点）
8. ✅ 越側オンボーディング資料v1（`onboarding-vn/` 01〜05）
