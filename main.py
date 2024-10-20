import discord
import os
import logging
import platform
import random
from typing import Final 
from dotenv import load_dotenv
from discord import CustomActivity, Embed
from discord.ext import commands, tasks
from discord.ext.commands import Context
from discord import Intents, Message
from PIL import Image
from io import BytesIO

# Load secrets
load_dotenv()
TOKEN: Final[str] = os.getenv('DISCORD_TOKEN')
invite_link: Final[str] = os.getenv('INVITE_LINK')
prefix: Final[str] = os.getenv('DEFAULT_PREFIX') 

# Setup logger
logger: logging.Logger = logging.getLogger()
logger.setLevel(logging.INFO)

file_handler: logging.FileHandler = logging.FileHandler(filename='logs/bot.log', encoding='utf-8', mode='w')
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
    self.prefix = prefix

  async def load_extensions(self) -> None:
    """
    Loads all the cogs for all supported commands
    """
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

  @tasks.loop(minutes=1.0)
  async def status_task(self) -> None:
    """
    Setup the game status task of the bot

    Discord does not support emojis in a bot's custom status. This is not a limitation of the API but of Discord itself. Work around is include the emoji in the status message.
    """
    statuses = ['🍌 Domo Arigato Your Girls A Thot Though', '💎 yo soy holder']
    await self.change_presence(activity=CustomActivity(name=random.choice(statuses)))


  @tasks.loop(minutes=1.0)
  async def avatar_task(self) -> None:
    """
    Setup the avatar the bot
    """

    image = Image.open('img/avatar.png')
    new_icon_bytes = BytesIO()
    image.save(new_icon_bytes, format='PNG')

    # Edit the bot's avatar using the bytes-like object
    await self.user.edit(avatar=bytes(new_icon_bytes.getvalue()))

  @avatar_task.before_loop
  async def before_status_task(self) -> None:
    """
    Before starting the status changing task, we make sure the bot is ready
    """
    await self.wait_until_ready()


  @status_task.before_loop
  async def before_status_task(self) -> None:
    """
    Before starting the status changing task, we make sure the bot is ready
    """
    await self.wait_until_ready()

  async def setup_hook(self) -> None:
    """
    This function executes once at the start of the bot run. Creates the logs file, 
    and attempts to load all the cogs.
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

    self.status_task.start()

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
    if username == self.user or not user_message.startswith(self.prefix):
      return

    await self.process_commands(message)

  async def on_command_completion(self, ctx: Context) -> None:
    """
    Runs after every successful command. We log the request here tracking the 
    discord guild (server), guild id, channel, username and command with any parameters
    """
    username: str = str(ctx.author)
    command: str = str(ctx.command)
    channel: str = str(ctx.channel)
    arguments: str = str(" ".join(str(arg) for arg in ctx.args[2:]))

    if ctx.guild:
      self.logger.info(
        f'[ guild:{ctx.guild.name}, id:{ctx.guild.id}, channel:{channel} ] {username}: "{self.prefix}{command} {arguments}"'
      )
    else:
      self.logger.info(f'[DM] {username}: "{self.prefix}{command}"')
      
  async def on_command_error(self, ctx: Context, error, *args) -> None:
    """
    Runs after a normal command catches an error. This will be used in the future when 
    we add privileged commands.

    :param error: the error we ecountered
    """
    username: str = str(ctx.author)
    command: str = str(ctx.command)
    channel: str = str(ctx.channel)
    arguments: str = str(" ".join(str(arg) for arg in ctx.args[2:]))

    embed = Embed(
      title='🚨 Error! 🚨',
      color=0xe6400e
    )

    if isinstance(error, commands.MissingRequiredArgument):
      embed.add_field(
        name='I need more information bro!',
        value=f'**Please pass all required arguments!**',
        inline=False,
      )

    elif isinstance(error, commands.CommandNotFound):
      embed.add_field(
        name='What did you call me?',
        value=f'**Invalid command. Try using** `{self.prefix}help` **to figure out commands!**',
        inline=False,
      )

    elif isinstance(error, commands.CheckFailure):
      embed.add_field(
        name='Who told you I can do that?',
        value=f'**Nothing to see here comrade.**',
        inline=False,
      )

    elif isinstance(error, commands.BadArgument):
      embed.add_field(
        name='I am confuzled',
        value=f'**I dont understand what you gave me. Please refer to `{self.prefix}help` menu.**',
        inline=False,
      )

    elif isinstance( error, commands.TooManyArguments):
       embed.add_field(
        name='Uhhhh I dont need that many arguments',
        value=f'**Please refer to the command help message for more info.**',
        inline=False,
      )

    else:
      embed.add_field(
        name='I am confuzled.',
        value=f'💩 Check in with your local bot master. I just had a brain fart. 💩',
        inline=False,
      )
    
    await ctx.send(embed=embed)

    if ctx.guild:
      self.logger.error(
        f'[ guild:{ctx.guild.name}, id:{ctx.guild.id}, channel:{channel} ] {username}: "{self.prefix}{command} {arguments}" ERROR: {error}'
      )
    else:
      self.logger.error(
        f'[DM] {username}: "{self.prefix}{command} {arguments}" [ERROR]: {error}'
      )

# Entry point
def main() -> None:
  bot = Bot()
  bot.run(TOKEN)

if __name__ == '__main__':
  main()