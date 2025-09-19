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
intents.guilds = True

bot = commands.Bot(command_prefix="!", intents=intents)

# ------------------------
# Channels
# ------------------------
WELCOME_CHANNEL_ID = 1418440616131428482
GOODBYE_CHANNEL_ID = 1418441039701610516
GUILD_ID = 1401492898293481505  # Server-ID
AUTHOR_ICON = "https://images-ext-1.discordapp.net/external/ORAM7L-2USvIhk9TKRteJkF9JyLXFa0RNBvrfual4E0/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/1401488134457524244/067dd861b8a4de1438d12c7bc283d935.webp?width=848&height=848"

TOTAL_USER_VOICE_NAME = "TotalUserCount"
BOTS_VOICE_NAME = "Bots Online"

# ------------------------
# Utility Function
# ------------------------
def create_embed(title, description_lines, image_url, thumbnail_url, footer_text, footer_icon, author_icon):
    description = '\n'.join(description_lines)
    embed = discord.Embed(
        title=title,
        description=description,
        color=0x8f1eae
    )
    embed.set_author(name="Supernova x Welcomer", icon_url=author_icon)
    embed.set_image(url=image_url)
    embed.set_thumbnail(url=thumbnail_url)
    embed.set_footer(text=footer_text, icon_url=footer_icon)
    return embed

# ------------------------
# Voice Channel Update
# ------------------------
async def update_voice_channels(guild):
    # TotalUserCount
    total_users = guild.member_count
    total_channel = discord.utils.get(guild.voice_channels, name=lambda n: TOTAL_USER_VOICE_NAME in n)
    if not total_channel:
        # Channel erstellen, falls nicht vorhanden
        total_channel = await guild.create_voice_channel(f"{TOTAL_USER_VOICE_NAME}: {total_users}")
    else:
        await total_channel.edit(name=f"{TOTAL_USER_VOICE_NAME}: {total_users}")

    # Bots Count
    bot_count = sum(1 for member in guild.members if member.bot)
    bots_channel = discord.utils.get(guild.voice_channels, name=lambda n: BOTS_VOICE_NAME in n)
    if not bots_channel:
        bots_channel = await guild.create_voice_channel(f"{BOTS_VOICE_NAME}: {bot_count}")
    else:
        await bots_channel.edit(name=f"{BOTS_VOICE_NAME}: {bot_count}")

# ------------------------
# Events
# ------------------------
@bot.event
async def on_ready():
    print(f"✅ Eingeloggt als {bot.user}")
    # Streaming Status
    activity = discord.Streaming(name="discord.gg/supernova", url="https://www.twitch.tv/qirixn")
    await bot.change_presence(status=discord.Status.online, activity=activity)
    print("🎬 Streaming Status gesetzt!")

    guild = bot.get_guild(GUILD_ID)
    if guild:
        await update_voice_channels(guild)

@bot.event
async def on_member_join(member):
    # Welcome Embed
    channel = bot.get_channel(WELCOME_CHANNEL_ID)
    if channel:
        description_lines = [f"Hey {member.mention} welcome to **discord.gg/supernova**."]
        embed = create_embed(
            title="**Welcome to discord.gg/supernova**",
            description_lines=description_lines,
            image_url="https://media.discordapp.net/attachments/1401822345953546284/1418437611193765888/Welcome.png?ex=68ce1e77&is=68ccccf7&hm=ea11922ec548a7438ce45a26eb96988ce281f7e9b57ebd240ffea5d3778f452e&=",
            thumbnail_url="https://cdn.discordapp.com/avatars/1401488134457524244/067dd861b8a4de1438d12c7bc283d935.webp?size=1024",
            footer_text="© 2022–2024 Superbova. All Rights Reserved.",
            footer_icon=AUTHOR_ICON,
            author_icon=AUTHOR_ICON
        )
        await channel.send(embed=embed, allowed_mentions=discord.AllowedMentions(users=True))

    # Voice Channels updaten
    await update_voice_channels(member.guild)

@bot.event
async def on_member_remove(member):
    # Leave Embed
    channel = bot.get_channel(GOODBYE_CHANNEL_ID)
    if channel:
        description_lines = ["Have a good Day from **discord.gg/supernova**."]
        embed = create_embed(
            title="**Goodbye from discord.gg/supernova**",
            description_lines=description_lines,
            image_url="https://media.discordapp.net/attachments/1401822345953546284/1418437610828988546/Good-Bye.png?ex=68ce1e77&is=68ccccf7&hm=bcf1f0ebb001ceeb793c4ed9b7022973d6d057b6ba34fcd171f3ca587b122499&=",
            thumbnail_url="https://cdn.discordapp.com/avatars/1401488134457524244/067dd861b8a4de1438d12c7bc283d935.webp?size=1024",
            footer_text="© 2022–2024 Superbova. All Rights Reserved.",
            footer_icon=AUTHOR_ICON,
            author_icon=AUTHOR_ICON
        )
        await channel.send(embed=embed)

    # Voice Channels updaten
    await update_voice_channels(member.guild)

# ------------------------
# Run Bot
# ------------------------
bot.run(os.getenv("DISCORD_TOKEN"))
