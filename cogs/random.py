import datetime
import time
from discord import Embed
from discord.ext import commands
from discord.ext.commands import Context
from pytz import timezone

class Random(commands.Cog, name='random'):
  def __init__(self, bot) -> None:
    self.bot = bot

  @commands.command(
    name='wednesday',
    description='This is a command that checks if the bot is healthy',
    aliases=['wed']
  )
  async def wednesday(self, ctx: Context) -> None:
    """
    Tells us if its wednesday, my dudes.

    :param context: The application command context.
    """
    embed = Embed(
      title='What day is it?',
      color=0x00FF00, # green hex
    )
    date: datetime.datetime = datetime.datetime.now() 
    date: date.astimezone = date.astimezone(timezone('US/Pacific'))
    
    is_wed: bool = False
    # It is wednesday
    if date.isoweekday() == 3:
      embed.add_field(
        name='It IS Wednesday my doods.',
        value='aaaaaaaahhhhhhhhhhhhhhhhhh',
        inline=False,
      )
      is_wed = True

    # Every other day
    else:
      embed.add_field(
        name='It is NOT Wednesday my doods.',
        value='sadge.',
        inline=False,
      )

    await ctx.send(embed=embed)
    # Unfortunatly, the discord API does not currently support 
    # embedding youtube videos on an Embed object. A workaround 
    # is to send the link, and discord auto-makes and embed video
    if is_wed:
      await ctx.send('https://www.youtube.com/watch?v=du-TY1GUFGk')

 
# Add the cog to the bot so that it can load, unload, reload and use it's content.
async def setup(bot) -> None:
  await bot.add_cog(Random(bot))