from discord.ext.commands import Bot, errors
from json import dumps

bot = Bot(command_prefix='!')

@bot.event
async def on_ready():
    """
        Jangan dihapus, bwt debug koneksi
    """

    print('Bot is connected to these servers:')

    for guild in bot.guilds:
        print('{} ({})'.format(guild.name, guild.id))

@bot.command(name='pif2')
async def command_hub(ctx, *params):
    await ctx.send('Steren Ganteng Sekali (SGS)') # placeholder