import json
import requests
from os import environ
from dotenv import load_dotenv, find_dotenv
from datetime import datetime
import urllib.parse

class CheckSynonym:
    def __init__(self):
        load_dotenv(find_dotenv())
        self.URL = "https://words.bighugelabs.com/api/2/"
        self.API_KEY = environ.get("BIG_HUGE_THESAURUS_KEY")+"/"
        self.allCountries = self.__fetch_all_countries()
        self.type = '/json'

    def check_synonyms(self, textParam):
        result = ""
        textParam = textParam.capitalize()
        if textParam.casefold() == "South Korea".casefold():
            textParam = "Korea, South"
        result = self.__binary_search(0, len(self.allCountries)-1, textParam)
        if result == None:
            completeURL = self.URL+self.API_KEY+textParam+self.type
            sendRequest = requests.get(url = completeURL)
            try:
                data = sendRequest.json()
                synonymList = data["noun"]["syn"]
            except json.JSONDecodeError:
                synonymList ="empty"

            for countries in synonymList:
                result = self.__binary_search(0, len(self.allCountries)-1, countries)
                if(result != None):
                    break

        return result

    def __binary_search(self, left, right, searchedText):
        if right >= left:
            mid = left+(right-left) //2
            if self.allCountries[mid]["name"].casefold() == searchedText.casefold():
                return self.allCountries[mid]["name"]
            elif self.allCountries[mid]["name"] > searchedText:
                return self.__binary_search(left, mid-1, searchedText)
            else:
                return self.__binary_search(mid+1, right, searchedText)
        else:
            return None

    def __fetch_all_countries(self):
        file = open("countries.txt", "r")
        content = file.read()
        jsonContent = json.loads(content)
        allCountries = jsonContent["countries"]

        return allCountries

class JSONHandler(object):
    def __init__(self, data):
        if type(data) is str:
            data = json.loads(data)
        
        self.convert_json(data)

    def convert_json(self, data):
        self.__dict__ = {}
        for key, value in data.items():
            if type(value) is dict:
                value = JSONHandler(value)
            
            self.__dict__[key] = value

    def __setitem__(self, key, value):
        self.__dict__[key] = value

    def __getitem__(self, key):
        return self.__dict__[key]

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
