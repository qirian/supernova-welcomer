import discord
from discord.ext import commands
import os
from keep_alive import keep_alive

intents = discord.Intents.default()
intents.members = True
intents.guilds = True
bot = commands.Bot(command_prefix="!", intents=intents)

# IDs
WELCOME_CHANNEL_ID = 1418440616131428482
LEAVE_CHANNEL_ID = 1418441039701610516
BOOST_CHANNEL_ID = 1418440857891377192
AUTOROLE_ID = 1401752418093498429
AUTOROLE_USER_ID = 1401763417357815848
AUTOROLE_BOT_ID = 1410848890638434355

# Bilder für Embeds
THUMBNAIL_URL = "https://cdn.discordapp.com/attachments/1401822345953546284/1418750912758943754/emvpuh1.gif"
IMAGE_URL = "https://cdn.discordapp.com/banners/1402963593527431280/a_00aa2372c379edf2e6dbbccc1ad36c50.gif?size=1024&animated=true"
AUTHOR_ICON = "https://cdn.discordapp.com/attachments/1401822345953546284/1418750912758943754/emvpuh1.gif"
FOOTER_ICON = "https://cdn.discordapp.com/attachments/1401822345953546284/1418750912758943754/emvpuh1.gif"

# Cache für letzte Nachrichten
last_messages = {}

# --- Funktion um doppelte Embeds zu verhindern ---
async def send_unique_embed(channel, embed, kind):
    """Send embed only if no existing duplicate in channel"""
    # Prüfe, ob eine Nachricht mit derselben kind-ID schon existiert
    if kind in last_messages:
        try:
            old_msg = await channel.fetch_message(last_messages[kind])
            if old_msg and old_msg.embeds:
                # Bereits vorhanden -> nichts senden
                return old_msg
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
    channel = bot.get_channel(WELCOME_CHANNEL_ID)
    if not channel:
        return

    total_members = len([m for m in member.guild.members if not m.bot])
    total_bots = len([m for m in member.guild.members if m.bot])

    embed = discord.Embed(
        title="Supernova x Welcomer",
        description=f"Welcome {member.mention} to **Supernova | Hosted by Levin**\n\n"
                    f"We're now with you {total_members} Members and {total_bots} Bots.",
        color=0x7b28a1
    )
    embed.set_author(name="Supernova x Welcomer", icon_url=AUTHOR_ICON)
    embed.set_thumbnail(url=THUMBNAIL_URL)
    embed.set_image(url=IMAGE_URL)
    embed.set_footer(
        text="© 2022–2024 Supernova | Hosted by Levin. All Rights Reserved.",
        icon_url=FOOTER_ICON
    )

    await send_unique_embed(channel, embed, kind=f"welcome_{member.id}")

    # Rollen
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
    channel = bot.get_channel(LEAVE_CHANNEL_ID)
    if not channel:
        return

    total_members = len([m for m in member.guild.members if not m.bot])
    total_bots = len([m for m in member.guild.members if m.bot])

    embed = discord.Embed(
        title="Supernova x Welcomer",
        description=f"Have a good day {member.mention} from **Supernova | Hosted by Levin**\n\n"
                    f"Without you we're {total_members} Members and {total_bots} Bots.",
        color=0x7b28a1
    )
    embed.set_author(name="Supernova x Welcomer", icon_url=AUTHOR_ICON)
    embed.set_thumbnail(url=THUMBNAIL_URL)
    embed.set_image(url=IMAGE_URL)
    embed.set_footer(
        text="© 2022–2024 Supernova | Hosted by Levin. All Rights Reserved.",
        icon_url=FOOTER_ICON
    )

    await send_unique_embed(channel, embed, kind=f"leave_{member.id}")

@bot.event
async def on_guild_update(before, after):
    if before.premium_subscription_count != after.premium_subscription_count:
        channel = bot.get_channel(BOOST_CHANNEL_ID)
        if not channel:
            return

        booster_count = after.premium_subscription_count

        embed = discord.Embed(
            title="A new Boost has appeared.",
            description=f"Thank you for your Boost! We now have {booster_count} Boosts thanks to you.",
            color=0x7b28a1
        )
        embed.set_author(name="Supernova x Welcomer", icon_url=AUTHOR_ICON)
        embed.set_thumbnail(url=THUMBNAIL_URL)
        embed.set_image(url=IMAGE_URL)
        embed.set_footer(
            text="© 2022–2024 Supernova | Hosted by Levin. All Rights Reserved.",
            icon_url=FOOTER_ICON
        )

        await send_unique_embed(channel, embed, kind="boost")

# --- Keep Alive ---
keep_alive()
bot.run(os.getenv("DISCORD_TOKEN"))
