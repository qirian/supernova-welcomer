import os
import discord
from discord.ext import commands
from keep_alive import keep_alive

# ---- Intents ----
intents = discord.Intents.default()
intents.members = True  # required for join/leave and AutoRole

bot = commands.Bot(command_prefix="!", intents=intents)

# ---- IDs ----
GUILD_ID = 1401492898293481505
WELCOME_CHANNEL_ID = 1401715590259019816
AUTO_ROLE_ID = 140000000000000000  # <-- replace with your AutoRole ID

# ---- Image Links ----
IMG_THUMB = "https://cdn.discordapp.com/attachments/1401822345953546284/1418750912758943754/emvpuh1.gif"
IMG_AUTHOR = IMG_THUMB
IMG_FOOTER = IMG_THUMB
IMG_BANNER = "https://cdn.discordapp.com/banners/1402963593527431280/a_00aa2372c379edf2e6dbbccc1ad36c50.gif?size=1024&animated=true"

# ---- On Ready ----
@bot.event
async def on_ready():
    print(f"Bot logged in as {bot.user}")
    await bot.change_presence(activity=discord.Streaming(
        name="discord.gg/supernova",
        url="https://www.twitch.tv/qirixn"
    ))

# ---- Welcome ----
@bot.event
async def on_member_join(member):
    channel = bot.get_channel(WELCOME_CHANNEL_ID)
    if not channel:
        print("Welcome channel not found")
        return

    # AutoRole
    role = member.guild.get_role(AUTO_ROLE_ID)
    if role:
        await member.add_roles(role)
        print(f"AutoRole {role.name} assigned to {member}")

    # Welcome Embed
    embed = discord.Embed(
        title="Welcome to Supernova | Hosted by Levin",
        description=f"Welcome {member.mention} to the server",
        color=discord.Color.green()
    )
    embed.set_author(name=member.name, icon_url=IMG_AUTHOR)
    embed.set_thumbnail(url=IMG_THUMB)
    embed.set_image(url=IMG_BANNER)
    embed.set_footer(text="Supernova | Hosted by Levin", icon_url=IMG_FOOTER)
    await channel.send(embed=embed)
    print(f"Welcome embed sent for {member}")

# ---- Leave ----
@bot.event
async def on_member_remove(member):
    channel = bot.get_channel(WELCOME_CHANNEL_ID)
    if not channel:
        print("Leave channel not found")
        return

    embed = discord.Embed(
        title="Goodbye from Supernova | Hosted by Levin",
        description=f"{member.mention} has left the server",
        color=discord.Color.red()
    )
    embed.set_author(name=member.name, icon_url=IMG_AUTHOR)
    embed.set_thumbnail(url=IMG_THUMB)
    embed.set_image(url=IMG_BANNER)
    embed.set_footer(text="Supernova | Hosted by Levin", icon_url=IMG_FOOTER)
    await channel.send(embed=embed)
    print(f"Leave embed sent for {member}")

# ---- Keep Alive ----
keep_alive()  # keeps the bot online with Render + UptimeRobot

# ---- Start Bot ----
bot.run(os.getenv("DISCORD_TOKEN"))
