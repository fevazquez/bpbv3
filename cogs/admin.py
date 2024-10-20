import discord
import platform
from discord import Embed
from discord.ext import commands
from discord.ext.commands import Context

class Admin(commands.Cog, name='admin'):
  def __init__(self, bot) -> None:
    self.bot = bot

  @commands.guild_only()
  @commands.has_permissions(administrator=True)
  @commands.command(
    name='reload',
    description='Reload a specific cog in order to get updated commands',
    aliases=['r']
  )
  async def reload_extensions(self, ctx: Context, cog_name: str) -> None:
    """
    Reloads the passed in cog. This is useful when we want to add new commands 
    but dont want to restart the bot to update the cog with the command. i.e. 100% uptime!

    :param cog_name: the name of the cog we want to reload
    """
    try:
      await self.bot.reload_extension(f'cogs.{cog_name}')

      embed = Embed(
        title='🔄 Reloaded!',
        description=f'Successfully reloaded {cog_name}! Use the ** `{self.bot.prefix}help` **to see the updates!**',
        color=0x00FF00, # green hex
      )
      self.bot.logger.info(f'Successfully reloaded cog {cog_name}')

    except Exception as e:
      embed = Embed(
        title='🚨 Reload Error! 🚨',
        description=f'Could not reload {cog_name}! Check in with your local bot master.',
        color=0xe6400e, # red hex
      )
      self.bot.logger.error(f'Failed to reload cog {cog_name}: {e}')
    
    finally:
      await ctx.send(embed=embed)

  @commands.guild_only()
  @commands.has_permissions(administrator=True)
  @commands.command(
    name='admin_help',
    description='List all available admin commands',
    aliases=['ah']
  )
  async def admin_help(self, ctx: Context) -> None:
    """
    Displays all the available commands this admin cog

    :param context: The application command context.
    """
    embed = Embed(
      title='ℹ️ Admin help',
      description=f'Commands at your disposal:',
      color=0x00FF00, # green hex
    )

    admin_cog = self.bot.get_cog('admin')
    commands = admin_cog.get_commands()

    data = []
    for command in commands:
      description = command.description.partition('\n')[0]
      data.append(f'{command.name} - {description}')

    help_text = '\n'.join(data)
    embed.add_field(
      name='Admin', value=f"```{help_text}```", inline=False
    )

    await ctx.send(embed=embed)

  @commands.guild_only()
  @commands.has_permissions(administrator=True)
  @commands.command(
    name='set_prefix',
    description='Change the bot command prefix',
    aliases=['cp']
  )
  async def change_prefix(self, ctx: Context, new_prefix: str) -> None:
    """
    Change the command prefix of the bot

    :param context: The application command context.
    """
    if new_prefix == self.bot.prefix:
      embed = Embed(
        title='No change needed',
        description=f'Command prefix **is already `{new_prefix}`!** No changes needed.',
        color=0x00FF00, # green hex
      )
    else:
      self.bot.prefix = new_prefix

      embed = Embed(
        title='Success!',
        description=f'Command prefix is now {self.bot.prefix}',
        color=0x00FF00, # green hex
      )

    await ctx.send(embed=embed)


# Add the cog to the bot so that it can load, unload, reload and use it's content.
async def setup(bot) -> None:
  await bot.add_cog(Admin(bot))