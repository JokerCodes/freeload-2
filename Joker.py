import discord
from discord.ext import commands
from discord import app_commands

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

freeload_mode = False

@bot.event
async def on_ready():
    try:
        # Global Sync (uncomment this for global syncing)
        # await bot.tree.sync()
        
        # Guild-Specific Sync (uncomment this for guild-specific syncing)
        # guild = discord.Object(id=YOUR_GUILD_ID)  # Replace with your Guild ID
        # await bot.tree.sync(guild=guild)
        
        print(f'Logged in as {bot.user}')
    except Exception as e:
        print(f'Failed to sync commands: {e}')

@bot.tree.command(name="freeload", description="Toggle freeload mode on or off.")
@app_commands.checks.has_permissions(administrator=True)
async def freeload(interaction: discord.Interaction, option: str):
    global freeload_mode
    if option.lower() == "on":
        freeload_mode = True
        await interaction.response.send_message("Freeload mode is now ON. Users leaving the server will be banned for 1 week.")
    elif option.lower() == "off":
        freeload_mode = False
        await interaction.response.send_message("Freeload mode is now OFF. Users leaving the server will not be banned.")
    else:
        await interaction.response.send_message("Invalid option. Use /freeload on or /freeload off.")

@bot.tree.command(name="ban", description="Ban a user from the server.")
@app_commands.checks.has_permissions(ban_members=True)
async def ban(interaction: discord.Interaction, user: discord.Member, reason: str = "No reason provided"):
    try:
        await user.ban(reason=reason)
        await interaction.response.send_message(f"{user.mention} has been banned for: {reason}")
    except Exception as e:
        await interaction.response.send_message(f"Failed to ban {user.mention}: {e}")

@bot.tree.command(name="unban", description="Unban a user from the server.")
@app_commands.checks.has_permissions(ban_members=True)
async def unban(interaction: discord.Interaction, user_id: str):
    try:
        user = await bot.fetch_user(user_id)
        await interaction.guild.unban(user)
        await interaction.response.send_message(f"{user.mention} has been unbanned.")
    except Exception as e:
        await interaction.response.send_message(f"Failed to unban user: {e}")

@bot.tree.command(name="warn", description="Warn a user.")
@app_commands.checks.has_permissions(manage_messages=True)
async def warn(interaction: discord.Interaction, user: discord.Member, reason: str = "No reason provided"):
    try:
        await user.send(f"You have been warned in {interaction.guild.name} for: {reason}")
        await interaction.response.send_message(f"{user.mention} has been warned for: {reason}")
    except Exception as e:
        await interaction.response.send_message(f"Failed to warn {user.mention}: {e}")

@bot.event
async def on_member_remove(member):
    if freeload_mode:
        try:
            await member.ban(reason="freeload", delete_message_days=0)
            print(f"Banned {member} for leaving the server during freeload mode.")
        except Exception as e:
            print(f"Failed to ban {member}: {e}")

bot.run('your bot token')
