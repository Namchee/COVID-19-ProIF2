from discord.ext.commands import Bot, errors
from json import dumps

bot = Bot(command_prefix='!')

@bot.event
async def on_ready():
    print('Bot is connected to these servers:')

    for guild in bot.guilds:
        print('{} ({})'.format(guild.name, guild.id))

@bot.command(name='pif2')
async def say(ctx, param1):
    try:
        await ctx.send(param1.lower())
    except errors.MissingRequiredArgument:
        return