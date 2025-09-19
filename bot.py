import os
import discord
from discord.ext import commands
from flask import Flask
from threading import Thread

# ------------------------
# Keep-Alive Setup
# ------------------------
app = Flask('')

@app.route('/')
def home():
    return "Bot läuft!", 200

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    Thread(target=run).start()

keep_alive()

# ------------------------
# Discord Bot Setup
# ------------------------
intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

# ------------------------
# Channels
# ------------------------
WELCOME_CHANNEL_ID = 1418440616131428482
GOODBYE_CHANNEL_ID = 1418441039701610516

# ------------------------
# Utility Function
# ------------------------
def create_embed(title, description_lines, image_url, thumbnail_url, footer_text, footer_icon):
    description = '\n'.join([f"> {line}" for line in description_lines])
    embed = discord.Embed(
        title=title,  # Title exakt übernommen
        description=description,
        color=0x8f1eae
    )
    embed.set_author(name="Supernova x Welcomer")
    embed.set_image(url=image_url)
    embed.set_thumbnail(url=thumbnail_url)
    embed.set_footer(text=footer_text, icon_url=footer_icon)
    return embed

# ------------------------
# Events
# ------------------------
@bot.event
async def on_ready():
    print(f"✅ Eingeloggt als {bot.user}")
    # Streaming Status setzen
    activity = discord.Streaming(
        name="discord.gg/supernova",
        url="https://www.twitch.tv/qirixn"
    )
    await bot.change_presence(status=discord.Status.online, activity=activity)
    print("🎬 Streaming Status gesetzt!")

@bot.event
async def on_member_join(member):
    channel = bot.get_channel(WELCOME_CHANNEL_ID)
    if channel:
        description_lines = [
            "🛬 First how was your flight?",
            "🔎 Here you find your ⁠test",
            "🥇 At least but not last our ⁠test2",
            "",
            f"👤User: {member.mention}",
            f"⌛ TotalUserCount: {member.guild.member_count}",
            "🔗 InviteLink: [Supernova Invite Link](https://discord.gg/3mRkJ6UYwx)"
        ]
        embed = create_embed(
            title="👋 Welcome to Supernova | Hosted by Levin Yilmaz",
            description_lines=description_lines,
            image_url="https://media.discordapp.net/attachments/1401822345953546284/1418437611193765888/Welcome.png?ex=68ce1e77&is=68ccccf7&hm=ea11922ec548a7438ce45a26eb96988ce281f7e9b57ebd240ffea5d3778f452e&=",
            thumbnail_url="https://cdn.discordapp.com/avatars/1401488134457524244/067dd861b8a4de1438d12c7bc283d935.webp?size=1024",
            footer_text="© 2022–2024 Superbova. All Rights Reserved.",
            footer_icon="https://images-ext-1.discordapp.net/external/ORAM7L-2USvIhk9TKRteJkF9JyLXFa0RNBvrfual4E0/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/1401488134457524244/067dd861b8a4de1438d12c7bc283d935.webp?width=848&height=848"
        )
        await channel.send(embed=embed, allowed_mentions=discord.AllowedMentions(users=True))

@bot.event
async def on_member_remove(member):
    channel = bot.get_channel(GOODBYE_CHANNEL_ID)
    if channel:
        description_lines = [
            "",
            "🍀 We wish you a good Travel.",
            "🔎 And we hope you find what you searching for.",
            "🥇 It was a honour for us to had you on our Server!",
            "",
            f"👤User: {member.name}",  # Ping beim Leave technisch nicht möglich
            f"⌛ TotalUserCount: {member.guild.member_count}",
            "🔗 InviteLink: [Supernova Invite Link](https://discord.gg/3mRkJ6UYwx)"
        ]
        embed = create_embed(
            title="👋 Thanks for your Visit | Hosted by Levin Yilmaz",
            description_lines=description_lines,
            image_url="https://media.discordapp.net/attachments/1401822345953546284/1418437610828988546/Good-Bye.png?ex=68ce1e77&is=68ccccf7&hm=bcf1f0ebb001ceeb793c4ed9b7022973d6d057b6ba34fcd171f3ca587b122499&=",
            thumbnail_url="https://cdn.discordapp.com/avatars/1401488134457524244/067dd861b8a4de1438d12c7bc283d935.webp?size=1024",
            footer_text="© 2022–2024 Superbova. All Rights Reserved.",
            footer_icon="https://images-ext-1.discordapp.net/external/ORAM7L-2USvIhk9TKRteJkF9JyLXFa0RNBvrfual4E0/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/1401488134457524244/067dd861b8a4de1438d12c7bc283d935.webp?width=848&height=848"
        )
        await channel.send(embed=embed)

# ------------------------
# Run Bot
# ------------------------
bot.run(os.getenv("DISCORD_TOKEN"))
