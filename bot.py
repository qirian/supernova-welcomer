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
intents.members = True  # für Join/Leave Events

bot = commands.Bot(command_prefix="!", intents=intents)

# Feste Channel IDs
WELCOME_CHANNEL_ID = 1418440616131428482
GOODBYE_CHANNEL_ID = 1418441039701610516

# ------------------------
# Utility Function für Embeds
# ------------------------
def create_embed(title, description, image_url, thumbnail_url, author_name, author_icon, footer_text):
    description = '\n'.join([f"> {line}" for line in description.split('\n')])
    embed = discord.Embed(
        title=f"# {title}",
        description=description,
        color=0x8f1eae
    )
    embed.set_image(url=image_url)
    embed.set_thumbnail(url=thumbnail_url)
    embed.set_author(name=author_name, icon_url=author_icon)
    embed.set_footer(text=footer_text)
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
        embed = create_embed(
            title="Welcome to Supernova | Hosted by Levin Yilmaz",
            description=(
                "We wish you a good Travel.\n"
                "And we hope you find what you searching for.\n\n"
                "It was a honour for us to had you on our Server!"
            ),
            image_url="https://media.discordapp.net/attachments/1401822345953546284/1418437610828988546/Good-Bye.png?ex=68ce1e77&is=68ccccf7&hm=bcf1f0ebb001ceeb793c4ed9b7022973d6d057b6ba34fcd171f3ca587b122499&=",
            thumbnail_url="https://cdn.discordapp.com/avatars/1401488134457524244/067dd861b8a4de1438d12c7bc283d935.webp?size=1024",
            author_name=member.name,
            author_icon="https://cdn.discordapp.com/avatars/1401488134457524244/067dd861b8a4de1438d12c7bc283d935.webp?size=1024",
            footer_text="© 2022–2024 Superbova. All Rights Reserved."
        )
        await channel.send(embed=embed)

@bot.event
async def on_member_remove(member):
    channel = bot.get_channel(GOODBYE_CHANNEL_ID)
    if channel:
        embed = create_embed(
            title="Thanks for your Visit | Hosted by Levin Yilmaz",
            description=(
                "We wish you a good Travel.\n"
                "And we hope you find what you searching for.\n\n"
                "It was a honour for us to had you on our Server!"
            ),
            image_url="https://media.discordapp.net/attachments/1401822345953546284/1418437610828988546/Good-Bye.png?ex=68ce1e77&is=68ccccf7&hm=bcf1f0ebb001ceeb793c4ed9b7022973d6d057b6ba34fcd171f3ca587b122499&=",
            thumbnail_url="https://cdn.discordapp.com/avatars/1401488134457524244/067dd861b8a4de1438d12c7bc283d935.webp?size=1024",
            author_name=member.name,
            author_icon="https://cdn.discordapp.com/avatars/1401488134457524244/067dd861b8a4de1438d12c7bc283d935.webp?size=1024",
            footer_text="© 2022–2024 Superbova. All Rights Reserved."
        )
        await channel.send(embed=embed)

# ------------------------
# Run Bot
# ------------------------
bot.run(os.getenv("DISCORD_TOKEN"))
