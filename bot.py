from discord.ext.commands import Bot, errors, Embed
from json import dumps
import json
import requests
from datetime import datetime
import time
from helper import JSONHandler, CheckSynonym

async def handle_help(ctx, params):
    help_string ="""This is a simple discord bot that can give you information about COVID-19.
Usage: `!pif2 <command> <params1> <params2> <etc>`

Command List:
1. `help`
    - Usage: `!pif2 help`
    - Function: Show the help dialog

2. `status <country name>`
	  - Usage: `!pif2 status <country name>`
    - Function: Show status from given country 		 

3. `graph <country name>`
    - Usage: `!pif2 graph <country name>`
    - Function: Show graph from given country

4. `info`
	- Usage: `!pif2 info`
  - Function: Show summary info about COVID-19
"""

    return await ctx.send(help_string)
		
async def handle_status(ctx, params):
    url = "https://covid19.mathdro.id/api/countries/"
    fullParam = " "
    fullParam = fullParam.join(params)
    checked = synonymCheck.check_synonyms(fullParam)
    if checked != None:
        url += checked
        response = requests.get(url)
        string = response.json()
        status = JSONHandler(string)
        text = "COVID-19 Status in " + fullParam.capitalize() + ":\n\n"
        text += "Infected: " + str(status.confirmed.value) + "\n"
        text += "Recovered: " + str(status.recovered.value) + "\n"
        text += "Dead: " + str(status.deaths.value) + "\n\n"	
        text += "Last Updated : " + convert_datetime(str(status.lastUpdate)) + "\n"
        text += "Data taken from JHE University"
    else:
	      text = "I'm sorry, looks like those country does not exist in our database"
  
    return await ctx.send(text)

async def handle_info(ctx, params):
    url = "https://en.wikipedia.org/api/rest_v1/page/summary/Coronavirus_disease_2019"
    response = requests.get(url)
    string = response.json()
    text = string['extract'] +'\n\n' + 'Information is taken from: Wikipedia'

    return await ctx.send(text)

def convert_datetime(strDate):
    datetimeObj = strDate
    datetimeObj = datetimeObj.replace('T',' ',1)
    datetimeObj = datetimeObj[0:19]
    datetimeObj = datetime.strptime(datetimeObj,"%Y-%m-%d %H:%M:%S")
    hari = datetimeObj.strftime("%A")
    tanggal = datetimeObj.strftime("%d")
    bulan = datetimeObj.strftime("%B")
    tahun = "20" + datetimeObj.strftime("%y")
    jam = datetimeObj.strftime("%H")
    menit = datetimeObj.strftime("%M")
    result = hari + ", " + tanggal + " " + bulan + " " + tahun + " " + jam + ":" + menit + " GMT+0"

    return result
    
async def handle_graph(ctx, params):
    tempImageURL = "https://covid19.mathdro.id/api/countries/"
    imageURL = " "
    imageURL = imageURL.join(params)
    checked = synonymCheck.check_synonyms(imageURL)
    if checked != None:
        tempImageURL += checked
        tempImageURL += "/og"
        embed = discord.Embed()
        embed.set_image(url=tempImageURL)
        return await ctx.send("", embed = embed)
    else:
        text = "I'm sorry, looks like those country does not exist in our database"
        return await ctx.send(text)
	 
handler_map = {}

handler_map['help'] = handle_help # tulis handler functionnya diatas
handler_map['status'] = handle_status
handler_map['graph'] = handle_graph
handler_map['info'] = handle_info
bot = Bot(command_prefix='!')

@bot.event
async def on_ready():
    """
        Jangan dihapus, bwt debug koneksi
    """
    global synonymCheck
    synonymCheck = CheckSynonym()
    # synonymCheck.check_synonyms(nama_negara) buat cek synonymnya kalau gak ketemu kembaliannya 'empty'
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
