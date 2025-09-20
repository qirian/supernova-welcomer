import os
import discord
from discord.ext import commands, tasks
import asyncio
import logging
from datetime import datetime

# ---- Intents ----
intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# ---- IDs ----
GUILD_ID = 1401492898293481505
STATUS_CHANNEL_ID = 1401715590259019816
LOG_CHANNEL_ID = 1401822345953546284

# ---- Logging ----
logging.basicConfig(level=logging.INFO)

# ---- On Ready ----
@bot.event
async def on_ready():
    print(f"✅ Eingeloggt als {bot.user}")
    update_status_embed.start()
    heartbeat_embed.start()
    await set_streaming_presence()

# ---- Streaming Presence ----
async def set_streaming_presence():
    await bot.wait_until_ready()
    await bot.change_presence(activity=discord.Streaming(
        name="Hazmob FPS: Online Shooter",
        url="https://twitch.tv/discord"
    ))

# ---- Heartbeat Embed ----
@tasks.loop(minutes=1)
async def heartbeat_embed():
    channel = bot.get_channel(STATUS_CHANNEL_ID)
    if not channel:
        return

    guild = bot.get_guild(GUILD_ID)
    if not guild:
        return

    embed = discord.Embed(
        title="🔄 Heartbeat",
        description=f"Bot läuft stabil – {datetime.utcnow().strftime('%H:%M:%S UTC')}",
        color=discord.Color.green()
    )
    embed.add_field(name="👥 Mitglieder", value=str(guild.member_count))
    embed.set_footer(text=f"Supernova | Hosted by Levin", icon_url=bot.user.avatar.url if bot.user.avatar else None)

    await channel.send(embed=embed)

# ---- Persistent Status Embed ----
@tasks.loop(minutes=5)
async def update_status_embed():
    channel = bot.get_channel(STATUS_CHANNEL_ID)
    if not channel:
        return

    guild = bot.get_guild(GUILD_ID)
    if not guild:
        return

    embed = discord.Embed(
        title="📊 Supernova Dashboard",
        color=discord.Color.blue(),
        timestamp=datetime.utcnow()
    )
    embed.set_thumbnail(url=bot.user.avatar.url if bot.user.avatar else None)
    embed.add_field(name="🤖 Bot", value="✅ Online", inline=True)
    embed.add_field(name="👥 Mitglieder", value=str(guild.member_count), inline=True)
    embed.add_field(name="🟢 Status", value="Stabil", inline=True)
    embed.set_footer(text="Supernova | Hosted by Levin", icon_url=bot.user.avatar.url if bot.user.avatar else None)

    # Versuchen, die letzte Nachricht vom Bot zu finden und zu editieren
    async for msg in channel.history(limit=20):
        if msg.author == bot.user and msg.embeds:
            await msg.edit(embed=embed)
            break
    else:
        await channel.send(embed=embed)

# ---- Logging ----
@bot.event
async def on_message_delete(message):
    if message.guild is None:
        return
    channel = bot.get_channel(LOG_CHANNEL_ID)
    if not channel:
        return

    embed = discord.Embed(
        title="🗑️ Nachricht gelöscht",
        description=f"Von {message.author.mention} in {message.channel.mention}",
        color=discord.Color.red(),
        timestamp=datetime.utcnow()
    )
    embed.add_field(name="Inhalt", value=message.content or "*(leer)*")
    embed.set_footer(text="Supernova Logs", icon_url=bot.user.avatar.url if bot.user.avatar else None)
    await channel.send(embed=embed)

# ---- Commands ----
@bot.command()
async def ping(ctx):
    await ctx.send("🏓 Pong!")

@bot.command()
async def clear(ctx, amount: int):
    await ctx.channel.purge(limit=amount + 1)
    await ctx.send(f"✅ {amount} Nachrichten gelöscht.", delete_after=5)

# ---- Welcome & Leave ----
@bot.event
async def on_member_join(member):
    channel = bot.get_channel(STATUS_CHANNEL_ID)
    if not channel:
        return

    embed = discord.Embed(
        title="**Welcome to Supernova | Hosted by Levin**",
        description=f"Hey {member.mention}, willkommen auf **{member.guild.name}**! 🎉",
        color=discord.Color.green()
    )
    embed.set_author(
        name=member.name,
        icon_url="https://cdn.discordapp.com/attachments/1401822345953546284/1418750912758943754/emvpuh1.gif"
    )
    embed.set_thumbnail(
        url="https://cdn.discordapp.com/attachments/1401822345953546284/1418750912758943754/emvpuh1.gif"
    )
    embed.set_image(
        url="https://cdn.discordapp.com/banners/1402963593527431280/a_00aa2372c379edf2e6dbbccc1ad36c50.gif?size=1024&animated=true"
    )
    embed.set_footer(
        text=f"{member.guild.name}",
        icon_url="https://cdn.discordapp.com/attachments/1401822345953546284/1418750912758943754/emvpuh1.gif"
    )

    await channel.send(embed=embed)

@bot.event
async def on_member_remove(member):
    channel = bot.get_channel(STATUS_CHANNEL_ID)
    if not channel:
        return

    embed = discord.Embed(
        title="**Goodbye from Supernova | Hosted by Levin**",
        description=f"{member.mention} hat **{member.guild.name}** verlassen. 👋",
        color=discord.Color.red()
    )
    embed.set_author(
        name=member.name,
        icon_url="https://cdn.discordapp.com/attachments/1401822345953546284/1418750912758943754/emvpuh1.gif"
    )
    embed.set_thumbnail(
        url="https://cdn.discordapp.com/attachments/1401822345953546284/1418750912758943754/emvpuh1.gif"
    )
    embed.set_image(
        url="https://cdn.discordapp.com/banners/1402963593527431280/a_00aa2372c379edf2e6dbbccc1ad36c50.gif?size=1024&animated=true"
    )
    embed.set_footer(
        text=f"{member.guild.name}",
        icon_url="https://cdn.discordapp.com/attachments/1401822345953546284/1418750912758943754/emvpuh1.gif"
    )

    await channel.send(embed=embed)

# ---- Keep Alive (falls Render/Replit braucht) ----
from keep_alive import keep_alive
keep_alive()

# ---- Start ----
bot.run(os.getenv("DISCORD_TOKEN"))
