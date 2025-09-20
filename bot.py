import os
import discord
from discord.ext import commands, tasks
from datetime import datetime
from keep_alive import keep_alive

# ---- Intents ----
intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# ---- IDs ----
GUILD_ID = 1401492898293481505
STATUS_CHANNEL_ID = 1401715590259019816
LOG_CHANNEL_ID = 1401822345953546284

# ---- Image Links ----
IMG_THUMB = "https://cdn.discordapp.com/attachments/1401822345953546284/1418750912758943754/emvpuh1.gif"
IMG_AUTHOR = IMG_THUMB
IMG_FOOTER = IMG_THUMB
IMG_BANNER = "https://cdn.discordapp.com/banners/1402963593527431280/a_00aa2372c379edf2e6dbbccc1ad36c50.gif?size=1024&animated=true"

# ---- On Ready ----
@bot.event
async def on_ready():
    print(f"✅ Eingeloggt als {bot.user}")
    update_status_embed.start()
    heartbeat_embed.start()
    await bot.change_presence(activity=discord.Streaming(
        name="Hazmob FPS: Online Shooter",
        url="https://twitch.tv/discord"
    ))

# ---- Heartbeat Embed ----
@tasks.loop(minutes=1)
async def heartbeat_embed():
    channel = bot.get_channel(STATUS_CHANNEL_ID)
    guild = bot.get_guild(GUILD_ID)
    if not channel or not guild:
        return

    embed = discord.Embed(
        title="🔄 Heartbeat",
        description=f"Bot läuft stabil – {datetime.utcnow().strftime('%H:%M:%S UTC')}",
        color=discord.Color.green()
    )
    embed.set_thumbnail(url=IMG_THUMB)
    embed.set_footer(text="Supernova | Hosted by Levin", icon_url=IMG_FOOTER)

    await channel.send(embed=embed)

# ---- Persistent Status Embed ----
@tasks.loop(minutes=5)
async def update_status_embed():
    channel = bot.get_channel(STATUS_CHANNEL_ID)
    guild = bot.get_guild(GUILD_ID)
    if not channel or not guild:
        return

    embed = discord.Embed(
        title="📊 Supernova Dashboard",
        color=discord.Color.blue(),
        timestamp=datetime.utcnow()
    )
    embed.set_thumbnail(url=IMG_THUMB)
    embed.set_image(url=IMG_BANNER)
    embed.add_field(name="🤖 Bot", value="✅ Online", inline=True)
    embed.add_field(name="👥 Mitglieder", value=str(guild.member_count), inline=True)
    embed.add_field(name="🟢 Status", value="Stabil", inline=True)
    embed.set_footer(text="Supernova | Hosted by Levin", icon_url=IMG_FOOTER)

    # Editieren statt spammen
    async for msg in channel.history(limit=20):
        if msg.author == bot.user and msg.embeds:
            await msg.edit(embed=embed)
            break
    else:
        await channel.send(embed=embed)

# ---- Logging ----
async def send_log(title, description, color=discord.Color.orange()):
    channel = bot.get_channel(LOG_CHANNEL_ID)
    if not channel:
        return
    embed = discord.Embed(
        title=title,
        description=description,
        color=color,
        timestamp=datetime.utcnow()
    )
    embed.set_thumbnail(url=IMG_THUMB)
    embed.set_footer(text="Supernova Logs", icon_url=IMG_FOOTER)
    await channel.send(embed=embed)

@bot.event
async def on_message_delete(message):
    if message.guild and not message.author.bot:
        await send_log(
            "🗑️ Nachricht gelöscht",
            f"Von {message.author.mention} in {message.channel.mention}\n**Inhalt:** {message.content or '*(leer)*'}",
            discord.Color.red()
        )

# ---- Commands ----
@bot.command()
async def ping(ctx):
    embed = discord.Embed(
        title="🏓 Pong!",
        description=f"Antwortzeit: {round(bot.latency * 1000)}ms",
        color=discord.Color.blurple()
    )
    embed.set_thumbnail(url=IMG_THUMB)
    await ctx.send(embed=embed)

@bot.command()
async def clear(ctx, amount: int):
    await ctx.channel.purge(limit=amount + 1)
    embed = discord.Embed(
        title="🧹 Chat gesäubert",
        description=f"{amount} Nachrichten gelöscht.",
        color=discord.Color.orange()
    )
    embed.set_thumbnail(url=IMG_THUMB)
    await ctx.send(embed=embed, delete_after=5)

# ---- Welcome & Leave ----
@bot.event
async def on_member_join(member):
    channel = bot.get_channel(STATUS_CHANNEL_ID)
    if not channel:
        return

    embed = discord.Embed(
        title="**Welcome to Supernova | Hosted by Levin**",
        description=f"Willkommen {member.mention}! 🎉",
        color=discord.Color.green()
    )
    embed.set_author(name=member.name, icon_url=IMG_AUTHOR)
    embed.set_thumbnail(url=IMG_THUMB)
    embed.set_image(url=IMG_BANNER)
    embed.set_footer(text=f"{member.guild.name}", icon_url=IMG_FOOTER)

    await channel.send(embed=embed)
    await send_log("👋 Neuer User", f"{member.mention} ist beigetreten.", discord.Color.green())

@bot.event
async def on_member_remove(member):
    channel = bot.get_channel(STATUS_CHANNEL_ID)
    if not channel:
        return

    embed = discord.Embed(
        title="**Goodbye from Supernova | Hosted by Levin**",
        description=f"{member.mention} hat den Server verlassen. 👋",
        color=discord.Color.red()
    )
    embed.set_author(name=member.name, icon_url=IMG_AUTHOR)
    embed.set_thumbnail(url=IMG_THUMB)
    embed.set_image(url=IMG_BANNER)
    embed.set_footer(text=f"{member.guild.name}", icon_url=IMG_FOOTER)

    await channel.send(embed=embed)
    await send_log("❌ User gegangen", f"{member.mention} hat den Server verlassen.", discord.Color.red())

# ---- Keep Alive ----
keep_alive()

# ---- Start ----
bot.run(os.getenv("DISCORD_TOKEN"))
