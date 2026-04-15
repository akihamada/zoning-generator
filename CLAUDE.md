# zoning-generator — Claude Code プロジェクト文脈

このファイルは Claude Code がこのリポジトリで作業するときに最初に読む文脈ファイルです。
どの端末（MacBook / iPhone / Mac mini）から接続しても同じ前提で会話が続けられるよう、
最小限のプロジェクト情報と、リモート作業の標準フローをまとめています。

---

## プロジェクト概要

`zoning-generator` は 2 つのコンポーネントから成ります。

1. **フロントエンド（静的ビルド成果物）** — 日本の用途地域ビューア
   - `index.html` / `assets/` / `favicon.svg` / `icons.svg`
   - Vite でビルド済みの単一ページ。このリポジトリ内にはソースは含まれていない。
   - ホスティングパスは `/zoning-generator/` 配下（`index.html` 参照）。

2. **`jp_struct/`** — 日本建築基準法 許容応力度設計 構造検定モジュール（Python）
   - 令82条に基づくルート1〜2の許容応力度検定
   - Rhino8 / Grasshopper / Karamba3D と連携
   - 詳細は `jp_struct/README.md` を参照

## ディレクトリ構成

```
zoning-generator/
├── CLAUDE.md                 # ← このファイル
├── index.html                # フロントエンド（ビルド済み）
├── assets/                   # JS/CSS バンドル
├── favicon.svg / icons.svg
├── config/
│   └── mac-ssh/              # リモート作業環境のテンプレート
│       ├── README.md
│       ├── tailscale-acl.json
│       └── ssh-config.example
└── jp_struct/                # Python 構造検定モジュール
    ├── README.md             # 詳細ドキュメント
    ├── jp_struct/            # パッケージ本体
    ├── data/                 # JIS / BH / 鋼材 / ボルト DB (JSON)
    ├── hops/                 # ghhops-server ブリッジ
    ├── gh_examples/
    ├── scripts/
    ├── tests/
    └── requirements.txt
```

## 単位系（`jp_struct/` 内）

内部は SI 単位系で統一:
- 力: **N**
- 長さ: **mm**
- 応力: **N/mm² (= MPa)**
- モーメント: **N·mm**

kN / kN·m との変換は入出力の境界（Karamba3D ブリッジなど）で行う。

## テスト / 開発コマンド

```bash
# jp_struct のテスト
cd jp_struct
pip install -r requirements.txt
pytest tests/

# スモークテスト (21件) + XLSX 出力テスト (1件)
pytest tests/test_smoke.py tests/test_report.py -v
```

## リモート作業の標準フロー

このリポジトリは Mac mini 上に clone されており、外出先の MacBook / iPhone から
Tailscale SSH 経由で tmux セッションに入って作業する想定です。

```
iPhone / MacBook
    ↓ Tailscale (VPN)
    ↓ ssh mac-mini  ← Tailscale SSH (鍵管理は Tailscale に委譲)
Mac mini（常時起動）
    ↓ tmux attach -t claude
    └─ Claude Code（このリポジトリ内で起動）
```

### セッションを開始するとき

```bash
ssh mac-mini
cd ~/projects/zoning-generator   # パスは環境に合わせて
tmux new -s claude               # 初回のみ
claude                           # Claude Code 起動
```

### セッションを離れるとき

`Ctrl+B` → `D` で **detach**。SSH を切っても Claude Code は生き続けます。

### 別端末から復帰するとき

```bash
ssh mac-mini
tmux attach -t claude
```

### tmux 早見表

| やりたいこと | コマンド |
|---|---|
| 新規セッション | `tmux new -s <名前>` |
| detach（離脱） | `Ctrl+B` → `D` |
| セッション一覧 | `tmux ls` |
| 復帰 | `tmux attach -t <名前>` |
| 縦分割 | `Ctrl+B` → `"` |
| 横分割 | `Ctrl+B` → `%` |
| ペイン移動 | `Ctrl+B` → 矢印 |
| セッション削除 | `tmux kill-session -t <名前>` |

リモート環境のセットアップ詳細は [`config/mac-ssh/README.md`](config/mac-ssh/README.md) を参照。

## 作業のお作法

- `jp_struct/` 配下のコードを変更したら必ず `pytest tests/` を通す
- 単位の境界では必ず SI に変換してから内部処理に渡す
- `data/*.json` を手で編集しない。更新は `jp_struct/scripts/generate_data.py` で再生成する
- フロントエンド (`index.html`, `assets/`) はビルド成果物なので基本的に手で編集しない
