from discord.ext.commands import Bot, errors
from json import dumps
import json
import requests
from datetime import datetime
import time

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
"""

    return await ctx.send(help_string)
class Status(object):
    def __init__(self, data):
        if type(data) is str:
            data = jsson.loads(data)
        self.convert_json(data)

    def convert_json(self, data):
        self.__dict__ = {}
        for key, value in data.items():
            if type(value) is dict:
                value = Status(value)
            self.__dict__[key] = value

    def __setitem__(self, key, value):
        self.__dict__[key] = value

    def __getitem__(self, key):
        return self.__dict__[key]
		
async def handle_status(ctx, params):
    url = "https://covid19.mathdro.id/api/countries/"
    url += params[0]
    response = requests.get(url)
    string = response.json()
    status = Status(string)
    text = "Perkembangan COVID-19 di " + params[0].capitalize() + ":\n\n"
    text += "Jumlah Kasus Positif: " + str(status.confirmed.value) + "\n"
    text += "Jumlah Pasien Sembuh: " + str(status.recovered.value) + "\n"
    text += "Jumlah Pasien Meninggal: " + str(status.deaths.value) + "\n\n"	
    text += "Terakhir Diperbarui : " + convert_datetime(str(status.lastUpdate)) + "\n"
    text += "Data diambil dari JHE University"
    return await ctx.send(text)

def convert_datetime(strDate):
     hari = ["Minggu", "Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu"]
     bulan = ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus", "September", "Oktober", "November", "Desember"]
     datetimeObj = strDate
     datetimeObj = datetimeObj.replace('T',' ',1)
     datetimeObj = datetimeObj[0:19]
     datetimeObj = datetime.strptime(datetimeObj,"%Y-%m-%d %H:%M:%S")
     nohari = int(datetimeObj.strftime("%w"))
     tanggal = datetimeObj.strftime("%d")
     nobulan = int(datetimeObj.strftime("%m"))-1
     tahun = "20" + datetimeObj.strftime("%y")
     jam = datetimeObj.strftime("%H")
     menit = datetimeObj.strftime("%M")
     result = hari[nohari] + ", " + tanggal + " " +bulan[nobulan] + " " + tahun + " pukul " + jam + ":" + menit + " GMT+0"
     return result
	 
handler_map = {}

handler_map['help'] = handle_help # tulis handler functionnya diatas
handler_map['status'] = handle_status
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
    """
        Jangan diubah-ubah :)
    """
    if handler_map.get(params[0]) is None:
        error_string = """I'm sorry, but I don't understand that 😔
You can type `!pif2 help` to get information about how to use this bot"""

        return await ctx.send(error_string)
    else:
        return await handler_map[params[0]](ctx, params[1:])
