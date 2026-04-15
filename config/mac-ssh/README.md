# Mac mini リモートアクセス環境

外出先の MacBook / iPhone から自宅の Mac mini に Tailscale SSH で接続し、
tmux で永続化された Claude Code セッションに入るための設定テンプレートです。

## ファイル一覧

| ファイル | 用途 |
|---|---|
| `tailscale-acl.json` | Tailscale Admin Console に貼り付ける ACL テンプレート |
| `ssh-config.example` | クライアント (MacBook) の `~/.ssh/config` に追記するエントリ |
| `README.md` | このファイル。Mac mini 側の手順と運用メモ |

## 構成図

```
iPhone (Termius) / MacBook
        │
        │ Tailscale (VPN, NAT 越え不要)
        │
        ▼
Mac mini (常時起動, Tailscale SSH)
        │
        ▼
tmux session "claude"
        │
        ▼
Claude Code (~/projects/zoning-generator で起動)
```

## 前提条件 (インストール済み)

- [x] Mac mini に Tailscale インストール済み
- [x] Mac mini に `tmux` インストール済み (`brew install tmux`)
- [x] MacBook に Tailscale インストール・ログイン済み
- [x] iPhone に Tailscale + Termius (or Blink Shell) インストール・ログイン済み

## Mac mini 側のセットアップ

### 1. システム設定

- **システム設定 → 一般 → 共有 → リモートログイン: OFF**
  Tailscale SSH を使うので、macOS 標準の sshd は不要です。公開面を減らすために OFF を推奨します。
- **システム設定 → 一般 → ソフトウェアアップデート → 自動インストール: OFF**
  夜中の再起動で tmux セッションが飛ぶのを防ぐため。

### 2. スリープ無効化

```bash
sudo pmset -a sleep 0 displaysleep 0
```

または GUI で: **システム設定 → ディスプレイ → 詳細設定 → ディスプレイがオフのときもスリープさせない**

### 3. Tailscale SSH を有効化

```bash
sudo tailscale up --ssh --advertise-tags=tag:mac-mini
```

これで Mac mini は `tag:mac-mini` タグ付きで tailnet に参加し、Tailscale 経由の SSH を受け付けます。

### 4. ACL を反映

`tailscale-acl.json` の中身を開き、以下のプレースホルダーを置換:

- `<YOUR_EMAIL>` → あなたの Tailscale ログインメール
- `<MAC_USER>` → Mac mini の macOS ユーザー名

置換後、[Tailscale Admin Console の ACL エディタ](https://login.tailscale.com/admin/acls/file) に貼り付けて保存。タグ承認を求められたら承認します。

### 5. tmux セッションを起動

```bash
cd ~/projects/zoning-generator
tmux new -s claude
claude
```

起動後、`Ctrl+B` → `D` で detach しておけば以降クライアントから `tmux attach -t claude` で復帰できます。

## クライアント (MacBook) 側のセットアップ

`ssh-config.example` の中身を `~/.ssh/config` に追記し、`<MAC_USER>` を置換してください。

```bash
cat config/mac-ssh/ssh-config.example >> ~/.ssh/config
# ~/.ssh/config を開いて <MAC_USER> を置換
```

これで `ssh mac-mini` だけで Mac mini に入れます。

## クライアント (iPhone / Termius) 側のセットアップ

1. Termius を開き **Hosts → New Host**
2. **Alias**: `mac-mini`
3. **Hostname**: `mac-mini` (Tailscale MagicDNS が有効なら短縮名で OK)
4. **Username**: `<MAC_USER>` で置換したユーザー名
5. **Port**: `22`
6. 鍵認証は不要 (Tailscale SSH が処理)

オプション: Termius の **Snippets** 機能に `tmux attach -t claude || tmux new -s claude` を登録しておくと、ログイン後ワンタップでセッションに入れます。

## 日常の使い方

### 作業開始

```bash
# どの端末からでも同じ
ssh mac-mini
tmux attach -t claude   # セッションが無ければ tmux new -s claude
```

### 作業中断

`Ctrl+B` → `D` で detach。SSH を切ってもセッションは残ります。

### 端末を切り替える

MacBook → iPhone や iPhone → MacBook も同じ手順。`tmux attach -t claude` で全く同じ画面の続きから作業できます。

### 複数プロジェクトを並行

```bash
tmux new -s zoning      # zoning-generator 用
tmux new -s jp-struct   # jp_struct 用
tmux ls                 # 一覧
tmux attach -t zoning   # 切替
```

## tmux 早見表

| 操作 | コマンド |
|---|---|
| 新規セッション | `tmux new -s <名前>` |
| detach (離脱) | `Ctrl+B` → `D` |
| セッション一覧 | `tmux ls` |
| 復帰 | `tmux attach -t <名前>` |
| 縦分割 | `Ctrl+B` → `"` |
| 横分割 | `Ctrl+B` → `%` |
| ペイン移動 | `Ctrl+B` → 矢印 |
| セッション削除 | `tmux kill-session -t <名前>` |

## トラブルシュート

### Mac mini に繋がらない

```bash
tailscale status   # どの端末からでも OK
```

- Mac mini が online でない場合 → Mac mini のコンソールで `sudo tailscale up --ssh --advertise-tags=tag:mac-mini` を再実行
- `ssh: Could not resolve hostname mac-mini` → MagicDNS が無効の可能性。Admin Console の DNS 設定で MagicDNS を ON にする、または `ssh <MAC_USER>@<Tailscale IP>` で直接繋ぐ

### `check` モードで再認証がうるさい

iPhone からブラウザが開けない、頻繁に認証を求められて不便、などの場合は `tailscale-acl.json` の `ssh` ブロックで `"action": "check"` を `"action": "accept"` に変更し、ACL を再保存してください。セキュリティと利便性のトレードオフです。

### tmux セッションが消えた

Mac mini が再起動するとセッションは消えます。再起動後に:

```bash
ssh mac-mini
cd ~/projects/zoning-generator
tmux new -s claude
claude
```

で作り直してください。

### Claude Code が反応しない / セッションが固まった

```bash
tmux kill-session -t claude
tmux new -s claude
claude
```

で作り直すのが最速です。

## セキュリティメモ

- Tailscale SSH は鍵管理を Tailscale に委ねるので、漏れた `id_rsa` でアクセスされる心配はありません
- `action: "check"` によりセッション開始時の再認証が必須 (デフォルト 12h)
- `tag:mac-mini` によりアクセス先が明示的に限定されます
- macOS の「リモートログイン」を OFF にしておくことで、標準 sshd の公開面をなくせます
