# Word Counter

Discord サーバー内の特定ワードを含むメッセージや、指定ロールを持つユーザーの全発言をカウントする Discord Bot です。

## 機能

- **特定ワード検出** — 設定したキーワードを含むメッセージに自動でリアクションを付与し、カウントを記録
- **ロール別カウント** — 指定ロールを持つユーザーの全メッセージをカウント対象に
- **カウント確認** — `/count` コマンドで自分のカウント数を確認
- **ランキング表示** — `/ranking` コマンドでTOP10ランキングを表示

## セットアップ

### 1. リポジトリをクローン

```bash
git clone https://github.com/Ramune-07/Word-Counter.git
cd WordCounter
```

### 2. 依存パッケージをインストール

```bash
pip install -r requirements.txt
```

### 3. 環境変数を設定

`sample.env` をコピーして `.env` を作成し、各項目を設定してください。

```bash
cp sample.env .env
```

| 変数名 | 説明 |
|---|---|
| `DISCORD_TOKEN` | Discord Bot のトークン |
| `TARGET_WORDS` | 反応させたいワード（カンマ区切りで複数指定可） |
| `REACTION_EMOJI` | リアクションに使用する絵文字 |
| `EXEMPT_ROLE_ID` | 全発言をカウント対象にするロールの ID |

### 4. Bot を起動

```bash
python main.py
```

## コマンド

| コマンド | 説明 |
|---|---|
| `/count` | 自分の合計カウントを表示 |
| `/ranking` | カウントランキング TOP10 を表示 |

## 使用技術

- [discord.py](https://discordpy.readthedocs.io/)
- [python-dotenv](https://pypi.org/project/python-dotenv/)
- SQLite3（Python 標準ライブラリ）
