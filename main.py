import os
import asyncio
import logging
from dotenv import load_dotenv
import discord
from discord.ext import commands, tasks
from api_fetch import fetch_customer_ids
import json

load_dotenv()

TOKEN = os.getenv('TOKEN')

# load settings from app_settings.json
with open('app_settings.json', 'r') as f:
    data = json.load(f)
    boomfi_sub_link = data["payment_links"]["normal"]["subscription"]
    boomfi_lifetime_link = data["payment_links"]["normal"]["lifetime"]


# Bot setup
intents = discord.Intents.default()
intents.members = True  # Enable member intent to read the member list

bot = commands.Bot(command_prefix="!", intents=intents)

# Role name (or ID) to be assigned/removed
role_name = "Premium"

# Global variable for the customer list
customers_list = []

# Configure logging
logging.basicConfig(level=logging.INFO)

# Function to check for updates to the customer list and update the role
async def update_roles_based_on_customers():
    global customers_list

    # Fetch the latest customer list
    new_customers_list = await fetch_customer_ids()

    # Check if the customers have their roles updated
    await manage_roles()

    if new_customers_list != customers_list:
        logging.info("Customer list has changed!")
        customers_list = new_customers_list
    else:
        logging.info("No changes to the customer list.")

    # Wait for a specified period before checking again (e.g., 60 seconds)
    await asyncio.sleep(30)

async def manage_roles():
    for guild in bot.guilds:
        # Fetch the role by name
        role = discord.utils.get(guild.roles, name=role_name)

        if not role:
            logging.warning(f"Role '{role_name}' not found!")
            continue

        # Fetch all members with the role
        members_with_role = [member for member in guild.members if role in member.roles]

        # Remove the role from members who are not in the customer list
        for member in members_with_role:
            if str(member.id) not in customers_list:
                await member.remove_roles(role)
                logging.info(f"Removed role from {member.name} ({member.id})")

        # Add the role to members who are in the customer list, but don't have it
        for user_id in customers_list:
            member = guild.get_member(int(user_id))
            if member and role not in member.roles:
                await member.add_roles(role)
                logging.info(f"Assigned role to {member.name} ({member.id})")

@bot.event
async def on_ready():
    logging.info(f"Bot is logged in as {bot.user}")

    # Start the background task to check for updates every 60 seconds
    bot.loop.create_task(periodically_check_customer_list())

# Background task to periodically check for updates
async def periodically_check_customer_list():
    while True:
        await update_roles_based_on_customers()

@bot.slash_command(name="join", description="Get your custom link")
async def join(ctx: discord.ApplicationContext):
    # Generate a custom link using the user's Discord ID
    user_id = ctx.author.id
    custom_link = f"{boomfi_sub_link}?customer_ident={user_id}"
    custom_link_lifetime = f"{boomfi_lifetime_link}?customer_ident={user_id}"
    # Create a button with the custom link
    button = discord.ui.Button(label="Click Here -> Monthly subscription", url=custom_link)
    button_lifetime = discord.ui.Button(label="Click Here -> Lifetime payment", url=custom_link_lifetime)
    view = discord.ui.View()
    view.add_item(button)
    view.add_item(button_lifetime)
    # Respond with the button
    await ctx.respond(
        f"Here is your custom link:",
        view=view,
        ephemeral=True  # Makes the message visible only to the user
    )

# Run the bot with your token
bot.run(TOKEN)
