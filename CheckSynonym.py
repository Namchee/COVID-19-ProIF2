import json
import requests
from os import environ
from dotenv import load_dotenv, find_dotenv


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
                if(result != 'empty'):
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
