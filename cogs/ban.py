import datetime
from discord import Embed
from discord.ext import commands
from discord.ext.commands import Context
from pytz import timezone

class Ban(commands.Cog, name='ban'):
  def __init__(self, bot) -> None:
    self.bot = bot

  @commands.command(
    name='ban',
    description='bans a person named Paul',
  )
  async def ban(self, ctx: Context, *args) -> None:
    """
    Main bot functionality.

    :param context: The application command context.
    :args: command arguments
    """
    name = args[0]
    embed = Embed(
      title='Bring down the ban hammer! 🔨',
      color=0x00FF00, # green hex
    )

    ban_count = 1
    if name == "paul":
      embed.add_field(
        name='',
        value=f'{name} has been banned. He has been banned {ban_count} times! my prefix is {}',
        inline=False,
      )

    else:
      embed.add_field(
        name='',
        value=f'{name} can\'t be banned. Only paul is allowed to be banned!',
        inline=False,
      )

    await ctx.send(embed=embed)
 
# Add the cog to the bot so that it can load, unload, reload and use it's content.
async def setup(bot) -> None:
  await bot.add_cog(Ban(bot))