import asyncio
import discord
import os
import logging
import platform
from typing import Final 
from dotenv import load_dotenv
from discord.ext import commands
from discord.ext.commands import Context
from discord import Intents, Message

# Load secrets
load_dotenv()
TOKEN: Final[str] = os.getenv('DISCORD_TOKEN')
invite_link: Final[str] = os.getenv('INVITE_LINK')
prefix: Final[str] = '>' # to be moved to json file, apparently its the better approach

# Setup logger
logger: logging.Logger = logging.getLogger()
logger.setLevel(logging.INFO)

file_handler: logging.FileHandler = logging.FileHandler(filename='bot.log', encoding='utf-8', mode='w')
file_handler_formatter: logging.Formatter = logging.Formatter(
  '[{asctime}] [{levelname:<8}] {name}: {message}', '%Y-%m-%d %H:%M:%S', style='{'
)
file_handler.setFormatter(file_handler_formatter)
logger.addHandler(file_handler)

# Bot initializers
intents: Intents = Intents.default()
intents.message_content = True

class Bot(commands.Bot):
  def __init__(self) -> None:
    super().__init__(
      command_prefix=commands.when_mentioned_or(prefix),
      case_insensitive=True,
      intents=intents,
      help_command=None
    )
    self.logger = logger
    self.invite_link = invite_link

  # Loads all the cogs for all supported commands
  async def load_extensions(self) -> None:
    for filename in os.listdir('./cogs'):
      if filename.endswith('.py'):
        cog = filename[:-3]

        try:
          # cut off the .py from the file name
          await self.load_extension(f'cogs.{cog}')
          logger.info(f'Loaded extension "{cog}"')
        
        except Exception as e:
          cog = f'{type(e).__name__}: {e}'
          logger.error(f'Failed to load cog: #{cog}')

  async def setup_hook(self) -> None:
    """
    This function executes once at the start of the bot run. Creates the logs file, 
    and attempts to loads all the cogs.
    """
    self.logger.info('------------------------------------------')
    self.logger.info(f'Logged in as {self.user.name}')
    self.logger.info(f'discord.py API version: {discord.__version__}')
    self.logger.info(f'Python version: {platform.python_version()}')
    self.logger.info(
      f'Running on: {platform.system()} {platform.release()} ({os.name})'
    )
    self.logger.info('------------------------------------------')

    try:
      await self.load_extensions()

    except Exception as e:
      logger.error(f'Failed to load cogs: {e}')

    # Print to console to let the user know its alive.
    print(f'{self.user} is now running!')

  async def on_message(self, message: Message) -> None:
    """
    Handles all incoming messages on the feed. We ignore the messages that
    are sent by the bot and the ones where there is no prefix
    """
    username: str = str(message.author)
    user_message: str = str(message.content)

    # Prevent infinite bot loop where it responds to iteself 
    # and ignore all incoming messages that are not appropriately prefixed
    if username == self.user or not user_message.startswith('>'):
      return

    await self.process_commands(message)

  async def on_command_completion(self, ctx: Context) -> None:
    """
    Runs after every successful command. We log the request here tracking the 
    discord guild (server), guild id, channel, username and command 
    """
    username: str = str(ctx.author)
    command: str = str(ctx.command)
    channel: str = str(ctx.channel)

    if ctx.guild:
      guild: str = str(ctx.guild)
      guild_id: str = str(ctx.guild.id)
      self.logger.info(
        f'[ guild:{ctx.guild.name}, id:{ctx.guild.id}, channel:{channel} ] {username}: "{prefix}{command}"'
      )
    else:
      self.logger.info(f'[DM] {username}: "{prefix}{command}"')
      
  async def on_command_failed(self, ctx: Context, error) -> None:
    """
    Runs after a normal command catches an error. This will be used in the future when 
    we add privileged commands

    :param error: the error we ecountered
    """
    embed = discord.Embed(
      title="Error!",
      description=str(error),
      color=0xe6400e
    )

    if isinstance(error, commands.MissingRequiredArguments):
      await ctx.send(embed=embed)

# Entry point
def main() -> None:
  bot = Bot()
  bot.run(TOKEN)

if __name__ == '__main__':
  main()