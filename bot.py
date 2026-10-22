
import discord
from discord import app_commands
from discord.ext import commands
import os

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

STAFF_ROLE_ID = 123456789012345678  # À remplacer par l'ID de ton rôle Staff


def is_staff(member):
    return (
        member.guild_permissions.administrator
        or any(role.id == STAFF_ROLE_ID for role in member.roles)
    )


@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"Bot connecté : {bot.user}")


@bot.tree.command(name="rank", description="Ajouter un rôle")
@app_commands.describe(membre="Le membre", role="Le rôle à ajouter")
async def rank(interaction: discord.Interaction, membre: discord.Member, role: discord.Role):
    if not is_staff(interaction.user):
        return await interaction.response.send_message("❌ Permission refusée.", ephemeral=True)
    if role.is_default() or role.managed or role >= interaction.guild.me.top_role:
        return await interaction.response.send_message("❌ Rôle non autorisé ou trop élevé.", ephemeral=True)
    await membre.add_roles(role, reason=f"Rank par {interaction.user}")
    await interaction.response.send_message(f"✅ Rôle {role.mention} ajouté à {membre.mention}.")


@bot.tree.command(name="unrank", description="Retirer un rôle")
@app_commands.describe(membre="Le membre", role="Le rôle à retirer")
async def unrank(interaction: discord.Interaction, membre: discord.Member, role: discord.Role):
    if not is_staff(interaction.user):
        return await interaction.response.send_message("❌ Permission refusée.", ephemeral=True)
    if role.is_default() or role.managed or role >= interaction.guild.me.top_role:
        return await interaction.response.send_message("❌ Rôle non autorisé ou trop élevé.", ephemeral=True)
    await membre.remove_roles(role, reason=f"Unrank par {interaction.user}")
    await interaction.response.send_message(f"✅ Rôle {role.mention} retiré à {membre.mention}.")


bot.run(os.environ["DISCORD_TOKEN"])
