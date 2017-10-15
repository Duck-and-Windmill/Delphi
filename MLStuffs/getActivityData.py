import urllib.request
import json
import datetime
import uuid
import requests
from pymongo import MongoClient

class getActivityData():
    @staticmethod
    def execute():
        client = MongoClient()
        repo = client.repo

        print("Fetching Activities Data...")
        activitiesURL = 'https://v3v10.vitechinc.com/solr/activities/select?indent=on&q=*:*&wt=json&rows=10'
        activities = requests.get(activitiesURL).json()["response"]["docs"]
        print("Saving Activities Data...")        
        repo.drop_collection("delphi.activities")
        repo.create_collection("delphi.activities")
        repo['delphi.activities'].insert_many(activities)
        print("Done")
        repo.logout()

getActivityData.execute()