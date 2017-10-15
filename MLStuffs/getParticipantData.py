import json
import requests
from pymongo import MongoClient

class getParticipantData():
    @staticmethod
    def execute():
        client = MongoClient()
        repo = client.repo

        print("Fetching Participant Data...")
        participantsURL = 'https://v3v10.vitechinc.com/solr/participant/select?indent=on&q={!join%20from=participant_id%20to=id%20fromIndex=policy_info}promo_codes:[*%20TO%20*]&wt=json&rows=39306'
        participants = requests.get(participantsURL).json()["response"]["docs"]
        print("Saving Participant Data...")        
        repo.drop_collection("delphi.participants")
        repo.create_collection("delphi.participants")
        repo['delphi.participants'].insert_many(participants)
        print("Done")
        repo.logout()

getParticipantData.execute()