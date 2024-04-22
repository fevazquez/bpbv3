from discord.ext import commands
from discord.ext.commands import Context

class Ping(commands.Cog, name='greetings'):
  def __init__(self, bot) -> None:
    self.bot = bot

  @commands.command(
    name='ping',
    description='This is a command that checks if the cogs were properly loaded.',
  )
  async def ping(self, ctx: Context) -> None:
    """
    This is a testing command that pings the cog to check if we are able call commands defined here.

    :param context: The application command context.
    """
    await ctx.send('I am alive!')

# Add the cog to the bot so that it can load, unload, reload and use it's content.
async def setup(bot) -> None:
  await bot.add_cog(Ping(bot))