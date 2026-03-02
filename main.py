import discord
import os
import sqlite3
from discord.ext import commands
from dotenv import load_dotenv

# .envファイルの読み込み
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
# カンマ区切りの文字列をリストに変換して空白を除去
TARGET_WORDS = [word.strip() for word in os.getenv('TARGET_WORDS').split(',')]
REACTION_EMOJI = os.getenv('REACTION_EMOJI')
EXEMPT_ROLE_ID = int(os.getenv('EXEMPT_ROLE_ID'))

# データベースの初期設定
db_path = 'word_counter.db'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS counts (
        user_id INTEGER PRIMARY KEY,
        count INTEGER DEFAULT 0
    )
''')
conn.commit()

# Botの権限設定
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    # スラッシュコマンドを同期
    await bot.tree.sync()
    print(f'Logged in as {bot.user.name} (ID: {bot.user.id})')
    print(f'Target words: {TARGET_WORDS}')

@bot.event
async def on_message(message):
    # Bot自身の発言は無視
    if message.author.bot:
        return

    # ロール判定
    has_role = any(role.id == EXEMPT_ROLE_ID for role in message.author.roles)
    
    # メッセージ内にTARGET_WORDSのいずれかが含まれているか判定
    has_target_word = any(word in message.content for word in TARGET_WORDS)
    
    # 特定ワードが含まれているか、または特定のロールを持っている場合
    if has_target_word or has_role:
        # リアクションを付与
        try:
            await message.add_reaction(REACTION_EMOJI)
        except Exception as e:
            print(f"Reaction error: {e}")

        # データベースを更新
        user_id = message.author.id
        cursor.execute('''
            INSERT INTO counts (user_id, count) 
            VALUES (?, 1) 
            ON CONFLICT(user_id) DO UPDATE SET count = count + 1
        ''', (user_id,))
        conn.commit()

    # 他のコマンドを処理できるようにする
    await bot.process_commands(message)

# カウント確認用スラッシュコマンド
@bot.tree.command(name='count', description='自分の合計カウントを表示')
async def count(interaction: discord.Interaction):
    cursor.execute('SELECT count FROM counts WHERE user_id = ?', (interaction.user.id,))
    row = cursor.fetchone()
    count = row[0] if row else 0
    await interaction.response.send_message(f'{interaction.user.display_name}さんの合計カウント: {count}')

# ランキング表示用スラッシュコマンド
@bot.tree.command(name='ranking', description='カウントランキングを表示')
async def ranking(interaction: discord.Interaction):
    cursor.execute('SELECT user_id, count FROM counts ORDER BY count DESC LIMIT 10')
    rows = cursor.fetchall()

    if not rows:
        await interaction.response.send_message('まだカウントデータがありません。')
        return

    ranking_lines = []
    for i, (user_id, cnt) in enumerate(rows, start=1):
        member = interaction.guild.get_member(user_id)
        name = member.display_name if member else f'不明なユーザー({user_id})'
        ranking_lines.append(f'**{i}位** {name} — {cnt}回')

    embed = discord.Embed(
        title='📊 カウントランキング TOP10',
        description='\n'.join(ranking_lines),
        color=discord.Color.gold()
    )
    await interaction.response.send_message(embed=embed)

bot.run(TOKEN)