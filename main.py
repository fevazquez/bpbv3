import asyncio
import discord
import os
import logging
import platform
from typing import Final 
from dotenv import load_dotenv
from discord.ext import commands
from discord import Intents, Message

# Load secrets
load_dotenv()
TOKEN: Final[str] = os.getenv('DISCORD_TOKEN')

# Setup logger
logger: logging.Logger = logging.getLogger()
logger.setLevel(logging.INFO)

file_handler: logging.FileHandler = logging.FileHandler(filename='bot.log', encoding='utf-8', mode='w')
file_handler_formatter: logging.Formatter = logging.Formatter(
  '[{asctime}] [{levelname:<8}] {name}: {message}', '%Y-%m-%d %H:%M:%S', style='{'
)
file_handler.setFormatter(file_handler_formatter)
logger.addHandler(file_handler)

# Bot Setup
intents: Intents = Intents.default()
intents.message_content = True
bot: commands.Bot = commands.Bot(command_prefix='>', case_insensitive=True, intents=intents)

async def load_extensions():
  for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
      cog = filename[:-3]

      try:
        # cut off the .py from the file name
        await bot.load_extension(f'cogs.{cog}')
        logger.info(f'Loaded extension "{cog}"')
      
      except Exception as e:
        cog = f'{type(e).__name__}: {e}'
        logger.error(f'Failed to load cog: #{cog}')

# Handle startup
@bot.event
async def on_ready() -> None:
  logger.info('------------------------------------------')
  logger.info(f'Logged in as {bot.user.name}')
  logger.info(f'discord.py API version: {discord.__version__}')
  logger.info(f'Python version: {platform.python_version()}')
  logger.info(
    f'Running on: {platform.system()} {platform.release()} ({os.name})'
  )
  logger.info('------------------------------------------')

  try:
    await load_extensions()

  except Exception as e:
    logger.error(f'Failed to load cogs: {e}')

  # Print to console to let the user know its alive.
  print(f'{bot.user} is now running!')
  

# Handling incoming messages
@bot.event
async def on_message(message: Message) -> None:

  username: str = str(message.author)
  user_message: str = str(message.content)

  # Prevent infinite bot loop where it responds to iteself 
  # and ignore all incoming messages that are not appropriately prefixed
  if username == bot.user or not user_message.startswith('>'):
    return

  # Log user request
  channel: str = str(message.channel)
  logger.info(f'[{channel}] {username}: "{user_message}"')

  await bot.process_commands(message)

# Entry point
def main() -> None:
  bot.run(token=TOKEN)

if __name__ == '__main__':
  main()