import discord
import platform
from discord import Embed
from discord.ext import commands
from discord.ext.commands import Context

class General(commands.Cog, name='general'):
  def __init__(self, bot) -> None:
    self.bot = bot

  @commands.command(
    name='ping',
    description='This is a command that checks if the bot is healthy',
  )
  async def ping(self, ctx: Context) -> None:
    """
    This is a testing command that pings the cog to check if we are able call all commands.

    :param context: The application command context.
    """
    embed = Embed(
      title='🏓 Pong!',
      description=f'I am alive and happy. The bot latency is about {round(self.bot.latency * 1000)}ms.',
      color=0x00FF00, # green hex
    )
    await ctx.send(embed=embed)

  @commands.command(
    name='botinfo',
    description='Get some arguably useful information about the bot',
    aliases=['binfo']
  )
  async def botinfo(self, ctx: Context) -> None:
    """
    This is a command that provides general bot information.

    :param context: The application command context.
    """
    embed = Embed(
      title="ehyeh asher ehyeh",
      color=0x00FF00, # green hex
    )

    embed.add_field(name='Owner:', value='itsfernanflow', inline=True)
    embed.add_field(
      name='Python Version:', value=f'{platform.python_version()}', inline=True
    )
    embed.add_field(name='Bot version:', value='0.0.1 - Alpha', inline=True)

    embed.add_field(
      name='Prefix:',
      value=f'"{self.bot.prefix}" for normal commands',
      inline=False,
    )

    embed.set_footer(text=f'Requested by {ctx.author}')
    await ctx.send(embed=embed)

  @commands.command(
    name='invite',
    description='Fetch the invite link to add the bot to a server.',
  )
  async def invite(self, ctx: Context) -> None:
    """
    Get the invite link for the bot to add it to any existing server.

    :params context: The application command context.
    """
    embed = Embed(
      description=f'Add me to any server by clicking [here]({self.bot.invite_link})',
      color=0x2a33bd
    )

    try:
      await ctx.author.send(embed=embed)
      await ctx.send('Check your dms 😉')

    except discord.Forbidden:
      await ctx.send(embed=embed)

  @commands.command(
    name='help',
    description='List all commands the bot has to offer.',
    aliases=['h']
  )
  async def help(self, ctx: Context) -> None:
    """
    General help command. Displays all the available commands from all the different cogs

    :param context: The application command context.
    """
    embed = Embed(
      title='ℹ️ Help me',
      description=f'Commands at your disposal:',
      color=0x00FF00, # green hex
    )

    for cog in self.bot.cogs:
      current_cog = self.bot.get_cog(cog.lower())
      commands = current_cog.get_commands()

      data = []
      for command in commands:
        description = command.description.partition('\n')[0]
        data.append(f'{command.name} - {description}')

      help_text = '\n'.join(data)
      embed.add_field(
        name=cog.capitalize(), value=f"```{help_text}```", inline=False
      )

    await ctx.send(embed=embed)

# Add the cog to the bot so that it can load, unload, reload and use it's content.
async def setup(bot) -> None:
  await bot.add_cog(General(bot))