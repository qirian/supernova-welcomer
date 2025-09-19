import os
import discord
from discord.ext import commands
from flask import Flask
from threading import Thread
import json

# ------------------------
# Keep-Alive Setup
# ------------------------
app = Flask('')

@app.route('/')
def home():
    return "Welcomer Bot läuft!", 200

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
# Config
# ------------------------
WELCOME_CHANNEL_ID = 1418440616131428482
LEAVE_CHANNEL_ID = 1418441039701610516
AUTOROLE_ID = 1401763417357815848

AUTHOR_ICON = "https://cdn.discordapp.com/avatars/1401488134457524244/067dd861b8a4de1438d12c7bc283d935.webp?size=1024"
THUMBNAIL = AUTHOR_ICON
WELCOME_IMAGE = "https://media.discordapp.net/attachments/1401822345953546284/1418437611193765888/Welcome.png?ex=68ce1e77&is=68ccccf7&hm=ea11922ec548a7438ce45a26eb96988ce281f7e9b57ebd240ffea5d3778f452e&="
LEAVE_IMAGE = "https://media.discordapp.net/attachments/1401822345953546284/1418437610828988546/Good-Bye.png?ex=68ce1e77&is=68ccccf7&hm=bcf1f0ebb001ceeb793c4ed9b7022973d6d057b6ba34fcd171f3ca587b122499&="

# Datei zum Speichern der User, die bereits Embeds bekommen haben
DATA_FILE = "welcomer_data.json"
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w") as f:
        json.dump({"welcomed": [], "left": []}, f)

def load_data():
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

# ------------------------
# Events
# ------------------------
@bot.event
async def on_ready():
    print(f"✅ Welcomer Bot eingeloggt als {bot.user}")

    # Streaming Status
    activity = discord.Streaming(
        name="discord.gg/supernova",
        url="https://www.twitch.tv/qirixn"
    )
    await bot.change_presence(status=discord.Status.online, activity=activity)
    print("Streaming Status gesetzt!")

@bot.event
async def on_member_join(member):
    data = load_data()
    if member.id in data["welcomed"]:
        return  # schon begrüßt, nichts tun

    # AutoRole vergeben
    role = member.guild.get_role(AUTOROLE_ID)
    if role:
        await member.add_roles(role)

    # Welcome Embed senden
    channel = bot.get_channel(WELCOME_CHANNEL_ID)
    if channel:
        embed = discord.Embed(
            title="Welcome to discord.gg/supernova",
            description=f"Hey {member.mention} welcome to **discord.gg/supernova**",
            color=0x8f1eae
        )
        embed.set_author(name="Supernova x Welcomer", icon_url=AUTHOR_ICON)
        embed.set_thumbnail(url=THUMBNAIL)
        embed.set_image(url=WELCOME_IMAGE)
        embed.set_footer(text="© 2022–2024 Superbova. All Rights Reserved.", icon_url=AUTHOR_ICON)
        await channel.send(embed=embed)

    data["welcomed"].append(member.id)
    save_data(data)

@bot.event
async def on_member_remove(member):
    data = load_data()
    if member.id in data["left"]:
        return  # schon verabschiedet, nichts tun

    # Leave Embed senden
    channel = bot.get_channel(LEAVE_CHANNEL_ID)
    if channel:
        embed = discord.Embed(
            title="Goodbye from discord.gg/supernova",
            description=f"Have a good Day from **discord.gg/supernova**",
            color=0x8f1eae
        )
        embed.set_author(name="Supernova x Welcomer", icon_url=AUTHOR_ICON)
        embed.set_thumbnail(url=THUMBNAIL)
        embed.set_image(url=LEAVE_IMAGE)
        embed.set_footer(text="© 2022–2024 Superbova. All Rights Reserved.", icon_url=AUTHOR_ICON)
        await channel.send(embed=embed)

    data["left"].append(member.id)
    save_data(data)

# ------------------------
# Run Bot
# ------------------------
bot.run(os.getenv("DISCORD_TOKEN"))
