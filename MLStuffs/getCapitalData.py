import json
import requests
from pymongo import MongoClient

class getCapitalData():
    @staticmethod
    def execute():
        client = MongoClient()
        repo = client.repo

        print("Fetching Capitals Data...")
        capitalsURL = 'https://gist.githubusercontent.com/ROODAY/76b5ead0afd607e599fa72a9a4dfc930/raw/cca0b16a11a90b93c4f2a72bd7d8ad9ea3a4813d/Canadia.json'
        capitals = requests.get(capitalsURL).json()

        print("Saving Capitals Data...")        
        repo.drop_collection("delphi.capitals")
        repo.create_collection("delphi.capitals")
        repo['delphi.capitals'].insert_many(capitals)
        print("Done")
        repo.logout()

getCapitalData.execute()