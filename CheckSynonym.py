import json
import requests


class CheckSynonym:
    def __init__(self):
        self.URL = "https://words.bighugelabs.com/api/2/"
        self.API_KEY = 'b21ab0483ed4e31ed5c41cd8f5aac2d7/'
        self.allCountries = self.fetch_all_countries()
        self.type = '/json'

    def check_synonyms(self,textParam):
        completeURL = self.URL+self.API_KEY+textParam+self.type
        sendRequest = requests.get(url = completeURL)
        data = sendRequest.json()
        synonymList = data["noun"]["syn"]
        result = "not found"
        for countries in synonymList:
            result = self.binary_search(0, len(self.allCountries)-1, countries)
            if(result != 'empty'):
                break
        return result

    def __binary_search(self, left, right, searchedText):
        if right >= left:
            mid = left+int((right-left)/2)
            if self.allCountries[mid]["name"].casefold() == searchedText.casefold():
                return self.allCountries[mid]["name"]
            elif self.allCountries[mid]["name"] > searchedText:
                return self.binary_search(left, mid-1, searchedText)
            else:
                return self.binary_search(mid+1, right, searchedText)
        else:
            return "empty"

    @staticmethod
    def __fetch_all_countries():
        file = open("countries.txt", "r")
        content = file.read()
        jsonContent = json.loads(content)
        allCountries = jsonContent["countries"]
        return allCountries

