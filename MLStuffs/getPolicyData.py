import urllib.request
import json
import datetime
import uuid
import requests
from pymongo import MongoClient

class getPolicyData():
    @staticmethod
    def execute():
        client = MongoClient()
        repo = client.repo

        print("Fetching Policies Data...")
        #https://v3v10.vitechinc.com/solr/policy_info/select?indent=on&q=promo_codes:[*%20TO%20*]&wt=json&rows=43234
        policiesURL = 'https://v3v10.vitechinc.com/solr/policy_info/select?indent=on&q=*:*&wt=json&rows=1532000'
        policies = requests.get(policiesURL).json()["response"]["docs"]
        print("Saving Policies Data...")        
        repo.drop_collection("delphi.policies")
        repo.create_collection("delphi.policies")
        repo['delphi.policies'].insert_many(policies)
        print("Done")
        repo.logout()

getPolicyData.execute()