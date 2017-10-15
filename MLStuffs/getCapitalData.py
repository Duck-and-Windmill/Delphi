import json
import requests
from pymongo import MongoClient

class getCapitalData():
    @staticmethod
    def execute():
        client = MongoClient()
        repo = client.repo

        print("Fetching Capitals Data...")
        capitalsURL = 'https://gist.githubusercontent.com/ROODAY/aa139c803c6b142fabc5e30a3e210a18/raw/362836851ca6db7ba36ba95a1e88e5e841d97b8d/CapitalCoords.json'
        capitals = requests.get(capitalsURL).json()
        final = []
        for capital in capitals:
          final.append(capitals[capital])

        print("Saving Capitals Data...")        
        repo.drop_collection("delphi.capitals")
        repo.create_collection("delphi.capitals")
        repo['delphi.capitals'].insert_many(final)
        print("Done")
        repo.logout()

getCapitalData.execute()