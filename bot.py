import os
import discord
from discord.ext import commands
from keep_alive import keep_alive

# ---- Intents ----
intents = discord.Intents.default()
intents.members = True  # required for join/leave and AutoRole

bot = commands.Bot(command_prefix="!", intents=intents)

# ---- IDs ----
WELCOME_CHANNEL_ID = 1418440616131428482  # Welcome Channel
LEAVE_CHANNEL_ID = 1418441039701610516   # Leave Channel
AUTO_ROLE_ID = 140000000000000000        # <-- replace with your AutoRole ID

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

    # AutoRole (für alle Mitglieder, auch Bots)
    role = member.guild.get_role(AUTO_ROLE_ID)
    if role:
        try:
            await member.add_roles(role)
            print(f"AutoRole {role.name} assigned to {member}")
        except Exception as e:
            print(f"Could not assign role to {member}: {e}")

    # Mitglied-Typ Kennzeichnung
    member_type = "(Bot)" if member.bot else ""

    # Gesamtzahl Mitglieder & Bots
    total_members = sum(1 for m in member.guild.members if not m.bot)
    total_bots = sum(1 for m in member.guild.members if m.bot)

    # Welcome Embed
    embed = discord.Embed(
        title="Welcome to Supernova | Hosted by Levin",
        description=f"Welcome {member.mention} {member_type} to the server, we're now with you **{total_members} Members** and **{total_bots} Bots**.",
        color=discord.Color(int("7b28a1", 16))  # Embed color
    )
    embed.set_author(name="Supernova x Welcomer", icon_url=IMG_AUTHOR)
    embed.set_thumbnail(url=IMG_THUMB)
    embed.set_image(url=IMG_BANNER)
    embed.set_footer(
        text="© 2022–2024 Supernova | Hosted by Levin. All Rights Reserved.",
        icon_url=IMG_FOOTER
    )

    try:
        await channel.send(embed=embed)
        print(f"Welcome embed sent for {member}")
    except Exception as e:
        print(f"Could not send welcome embed for {member}: {e}")

# ---- Leave ----
@bot.event
async def on_member_remove(member):
    channel = bot.get_channel(LEAVE_CHANNEL_ID)
    if not channel:
        print("Leave channel not found")
        return

    member_type = "(Bot)" if member.bot else ""
    total_members = sum(1 for m in member.guild.members if not m.bot)
    total_bots = sum(1 for m in member.guild.members if m.bot)

    embed = discord.Embed(
        title="Goodbye from Supernova | Hosted by Levin",
        description=f"{member.mention} {member_type} has left the server, without you we're **{total_members} Members** and **{total_bots} Bots**.",
        color=discord.Color(int("7b28a1", 16))  # Embed color
    )
    embed.set_author(name="Supernova x Welcomer", icon_url=IMG_AUTHOR)
    embed.set_thumbnail(url=IMG_THUMB)
    embed.set_image(url=IMG_BANNER)
    embed.set_footer(
        text="© 2022–2024 Supernova | Hosted by Levin. All Rights Reserved.",
        icon_url=IMG_FOOTER
    )

    try:
        await channel.send(embed=embed)
        print(f"Leave embed sent for {member}")
    except Exception as e:
        print(f"Could not send leave embed for {member}: {e}")

# ---- Keep Alive ----
keep_alive()  # keeps the bot online with Render + UptimeRobot

# ---- Start Bot ----
bot.run(os.getenv("DISCORD_TOKEN"))
