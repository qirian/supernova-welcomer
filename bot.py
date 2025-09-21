import discord
from discord.ext import commands
import os
from keep_alive import keep_alive

intents = discord.Intents.default()
intents.members = True  # wichtig für join/leave events
bot = commands.Bot(command_prefix="!", intents=intents)

# IDs
WELCOME_CHANNEL_ID = 1418440616131428482
LEAVE_CHANNEL_ID = 1418441039701610516
AUTOROLE_ID = 1401752418093498429
AUTOROLE_USER_ID = 1401763417357815848
AUTOROLE_BOT_ID = 1410848890638434355

# Cache für letzte Nachrichten
last_messages = {}

# --- Funktion um doppelte Embeds zu verhindern ---
async def send_unique_embed(channel, embed, kind):
    """Send embed and auto-delete old duplicates, keeping the newest one"""
    # Wenn es schon eine alte Nachricht gibt -> löschen
    if kind in last_messages:
        try:
            old_msg = await channel.fetch_message(last_messages[kind])
            if old_msg:
                await old_msg.delete()
        except discord.NotFound:
            pass

    # Neue Nachricht senden und speichern
    msg = await channel.send(embed=embed)
    last_messages[kind] = msg.id
    return msg

# --- Events ---
@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Streaming(
        name="discord.gg/supernova",
        url="https://www.twitch.tv/qirixn"
    ))
    print(f"Bot {bot.user} is ready.")

@bot.event
async def on_member_join(member):
    # Channel abrufen
    channel = bot.get_channel(WELCOME_CHANNEL_ID)
    if not channel:
        return

    # Member zählen
    total_members = len([m for m in member.guild.members if not m.bot])
    total_bots = len([m for m in member.guild.members if m.bot])

    # Embed erstellen
    embed = discord.Embed(
        title="Supernova x Welcomer",
        description=f"Welcome {member.mention} to **Supernova | Hosted by Levin**\n\n"
                    f"We're now with you {total_members} Members and {total_bots} Bots.",
        color=0x7b28a1
    )
    embed.set_author(name="Supernova x Welcomer")
    embed.set_thumbnail(url=member.display_avatar.url)
    embed.set_footer(text="© 2022–2024 Supernova | Hosted by Levin. All Rights Reserved.")

    await send_unique_embed(channel, embed, kind=f"welcome_{member.id}")

    # Rollen vergeben
    role_everyone = member.guild.get_role(AUTOROLE_ID)
    role_user = member.guild.get_role(AUTOROLE_USER_ID)
    role_bot = member.guild.get_role(AUTOROLE_BOT_ID)

    if role_everyone:
        await member.add_roles(role_everyone)
    if member.bot and role_bot:
        await member.add_roles(role_bot)
    elif not member.bot and role_user:
        await member.add_roles(role_user)

@bot.event
async def on_member_remove(member):
    # Channel abrufen
    channel = bot.get_channel(LEAVE_CHANNEL_ID)
    if not channel:
        return

    # Member zählen
    total_members = len([m for m in member.guild.members if not m.bot])
    total_bots = len([m for m in member.guild.members if m.bot])

    # Embed erstellen
    embed = discord.Embed(
        title="Supernova x Welcomer",
        description=f"Have a good day {member.mention} from **Supernova | Hosted by Levin**\n\n"
                    f"Without you we're {total_members} Members and {total_bots} Bots.",
        color=0x7b28a1
    )
    embed.set_author(name="Supernova x Welcomer")
    embed.set_thumbnail(url=member.display_avatar.url)
    embed.set_footer(text="© 2022–2024 Supernova | Hosted by Levin. All Rights Reserved.")

    await send_unique_embed(channel, embed, kind=f"leave_{member.id}")

# --- Keep Alive ---
keep_alive()
bot.run(os.getenv("DISCORD_TOKEN"))
