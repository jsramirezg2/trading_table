import os
import time
import asyncio
from dotenv import load_dotenv
import discord
from discord.ext import commands, tasks
from api_fetch import fetch_customer_ids  # Import the function from fetch_api.py

load_dotenv()

TOKEN = os.getenv('TOKEN')

# Bot setup
intents = discord.Intents.default()
intents.members = True  # Enable member intent to read the member list

bot = commands.Bot(command_prefix="!", intents=intents)

# Role name (or ID) to be assigned/removed
role_name = "VIP member"

# Global variable for the customer list
customers_list = []

# Function to check for updates to the customer list and update the role
async def update_roles_based_on_customers():
    global customers_list

    # Fetch the latest customer list
    new_customers_list = fetch_customer_ids()

    if new_customers_list != customers_list:
        print("Customer list has changed!")
        customers_list = new_customers_list
        await manage_roles()  # Manage roles based on the updated list
    else:
        print("No changes to the customer list.")

    # Wait for a specified period before checking again (e.g., 60 seconds)
    await asyncio.sleep(60)

async def manage_roles():
    for guild in bot.guilds:
        # Fetch the role by name
        role = discord.utils.get(guild.roles, name=role_name)

        if not role:
            print(f"Role '{role_name}' not found!")
            continue

        # Fetch all members with the role
        members_with_role = [member for member in guild.members if role in member.roles]

        # Remove the role from members who are not in the customer list
        for member in members_with_role:
            if str(member.id) not in customers_list:
                await member.remove_roles(role)
                print(f"Removed role from {member.name} ({member.id})")

        # Add the role to members who are in the customer list, but don't have it
        for user_id in customers_list:
            member = guild.get_member(int(user_id))
            if member and role not in member.roles:
                await member.add_roles(role)
                print(f"Assigned role to {member.name} ({member.id})")

@bot.event
async def on_ready():
    print(f"Bot is logged in as {bot.user}")

    # Start the background task to check for updates every 60 seconds
    bot.loop.create_task(periodically_check_customer_list())

# Background task to periodically check for updates
async def periodically_check_customer_list():
    while True:
        await update_roles_based_on_customers()

# Run the bot with your token
bot.run(TOKEN)
