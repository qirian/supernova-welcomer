import discord
from discord.ext import commands
import os
from keep_alive import keep_alive

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Channel IDs
WELCOME_CHANNEL_ID = 1418440616131428482
LEAVE_CHANNEL_ID   = 1418441039701610516
BOOST_CHANNEL_ID   = 1418440616131428482  # Kannst du ändern

# Embed Style
EMBED_COLOR = 0x7b28a1
THUMBNAIL_URL = "https://cdn.discordapp.com/attachments/1401822345953546284/1418750912758943754/emvpuh1.gif"
IMAGE_URL     = "https://cdn.discordapp.com/banners/1402963593527431280/a_00aa2372c379edf2e6dbbccc1ad36c50.gif?size=1024&animated=true"
AUTHOR_ICON   = THUMBNAIL_URL
FOOTER_TEXT   = "© 2022–2024 Supernova | Hosted by Levin. All Rights Reserved."
FOOTER_ICON   = THUMBNAIL_URL

# Rollen
ROLE_USER_ID = 1401763417357815848
ROLE_BOT_ID  = 1410848890638434355
ROLE_ALL_ID  = 1401752418093498429

# Cache: {guild_id: {user_id: {"welcome": True, "leave": True, "boost": True}}}
embed_cache = {}
# Letzte Nachricht gespeichert: {"welcome": msg_id, "leave": msg_id, "boost": msg_id}
last_messages = {}

def already_sent(guild_id, user_id, kind):
    """Check if embed already sent for this user and event type"""
    guild_cache = embed_cache.setdefault(guild_id, {})
    user_cache = guild_cache.setdefault(user_id, {"welcome": False, "leave": False, "boost": False})
    if user_cache[kind]:
        return True
    user_cache[kind] = True
    return False

async def send_unique_embed(channel, embed, kind):
    """Send embed and auto-delete duplicates"""
    msg = await channel.send(embed=embed)
    # Check duplicate
    if kind in last_messages:
        try:
            old_msg = await channel.fetch_message(last_messages[kind])
            if old_msg and old_msg.embeds and old_msg.embeds[0].description == embed.description:
                # delete duplicate
                await msg.delete()
                return old_msg
        except discord.NotFound:
            pass
    last_messages[kind] = msg.id
    return msg

# -------------------------
# Member Join
# -------------------------
@bot.event
async def on_member_join(member):
    # AutoRole für alle
    role_all = member.guild.get_role(ROLE_ALL_ID)
    if role_all:
        await member.add_roles(role_all)

    # Jeder kriegt User-Rolle (Bots werden wie User behandelt)
    role_user = member.guild.get_role(ROLE_USER_ID)
    if role_user:
        await member.add_roles(role_user)

    # Welcome nur einmal
    if already_sent(member.guild.id, member.id, "welcome"):
        return

    channel = member.guild.get_channel(WELCOME_CHANNEL_ID)
    if channel:
        total_members = len(member.guild.members)

        embed = discord.Embed(
            title="Welcome to Supernova | Hosted by Levin",
            description=f"Welcome {member.mention} to the server, we're now {total_members} Members.",
            color=EMBED_COLOR
        )
        embed.set_thumbnail(url=THUMBNAIL_URL)
        embed.set_image(url=IMAGE_URL)
        embed.set_author(name="Supernova x Welcomer", icon_url=AUTHOR_ICON)
        embed.set_footer(text=FOOTER_TEXT, icon_url=FOOTER_ICON)
        await send_unique_embed(channel, embed, "welcome")

# -------------------------
# Member Leave
# -------------------------
@bot.event
async def on_member_remove(member):
    if already_sent(member.guild.id, member.id, "leave"):
        return

    channel = member.guild.get_channel(LEAVE_CHANNEL_ID)
    if channel:
        total_members = len(member.guild.members)

        embed = discord.Embed(
            title="Goodbye from Supernova | Hosted by Levin",
            description=f"{member.mention} has left the server, without you we're {total_members} Members.",
            color=EMBED_COLOR
        )
        embed.set_thumbnail(url=THUMBNAIL_URL)
        embed.set_image(url=IMAGE_URL)
        embed.set_author(name="Supernova x Welcomer", icon_url=AUTHOR_ICON)
        embed.set_footer(text=FOOTER_TEXT, icon_url=FOOTER_ICON)
        await send_unique_embed(channel, embed, "leave")

# -------------------------
# Boost
# -------------------------
@bot.event
async def on_member_update(before, after):
    if before.premium_since != after.premium_since and after.premium_since is not None:
        if already_sent(after.guild.id, after.id, "boost"):
            return

        channel = after.guild.get_channel(BOOST_CHANNEL_ID)
        if channel:
            booster_count = sum(1 for m in after.guild.members if m.premium_since)

            embed = discord.Embed(
                title="A new Boost has appeared.",
                description=f"Thank you {after.mention} for your Boost! We have thanks to you {booster_count} Boosts.",
                color=EMBED_COLOR
            )
            embed.set_thumbnail(url=THUMBNAIL_URL)
            embed.set_image(url=IMAGE_URL)
            embed.set_author(name="Supernova x Welcomer", icon_url=AUTHOR_ICON)
            embed.set_footer(text=FOOTER_TEXT, icon_url=FOOTER_ICON)
            await send_unique_embed(channel, embed, "boost")

# -------------------------
# Ready
# -------------------------
@bot.event
async def on_ready():
    print(f"Welcomer Bot logged in as {bot.user}")
    await bot.change_presence(activity=discord.Streaming(
        name="dicsord.gg/supernova",
        url="https://www.twitch.tv/qirixn"
    ))

# -------------------------
# Keep Alive + Run
# -------------------------
keep_alive()
bot.run(os.getenv("DISCORD_TOKEN"))
