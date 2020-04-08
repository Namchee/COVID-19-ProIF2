from discord.ext.commands import Bot, errors
from json import dumps
from CheckSynonym import CheckSynonym

async def handle_help(ctx, params):
    help_string ="""This is a simple discord bot that can give you information about COVID-19.
Usage: `!pif2 <command> <params1> <params2> <etc>`

Command List:
1. `help`
    - Usage: `!pif2 help`
    - Function: Show the help dialog
"""

    return await ctx.send(help_string)

handler_map = {}

handler_map['help'] = handle_help # tulis handler functionnya diatas

bot = Bot(command_prefix='!')

@bot.event
async def on_ready():
    """
        Jangan dihapus, bwt debug koneksi
    """
    synonymCheck = CheckSynonym()
    # synonymCheck.check_synonyms(textparam) buat cek synonymnya kalau gak ketemu kembaliannya 'empty'
    print('Bot is connected to these servers:')

    for guild in bot.guilds:
        print('{} ({})'.format(guild.name, guild.id))

@bot.command(name='pif2')
async def command_hub(ctx, *params):
    """
        Jangan diubah-ubah :)
    """
    if handler_map.get(params[0]) is None:
        error_string = """I'm sorry, but I don't understand that 😔
You can type `!pif2 help` to get information about how to use this bot"""

        return await ctx.send(error_string)
    else:
        return await handler_map[params[0]](ctx, params[1:])
