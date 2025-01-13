import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import api_fetch

load_dotenv()

TOKEN = os.getenv("TOKEN")

print(TOKEN)


if __name__ == '__main__':
    bot = commands.Bot(command_prefix='!')
    bot.run(TOKEN)