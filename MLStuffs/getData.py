import urllib.request
import json
import datetime
import uuid
import requests
from pymongo import MongoClient

class getData():
    def union(R, S):
        return R + S
    def intersect(R, S):
        return [t for t in R if t in S]
    def product(R, S):
        return [(t,u) for t in R for u in S]
    def select(R, s):
        return [t for t in R if s(t)]
    def aggregate(R,f):
        keys = {r[0] for r in R}
        return [(key, f([v for (k,v) in R if k == key])) for key in keys]
    def project(R, p):
        return [p(t) for t in R]
    def removeDuplicates(seq):
        seen = set()
        seen_add = seen.add
        return [x for x in seq if not (x in seen or seen_add(x)) and x != " "]

    def cleanData(t):
        # ID, Sex, Marital Status, Birth Date, Lng, Lat
        return (t["id"], t["sex"], t["married"], t["age"], t["lng"], t["lat"], t['promo_codes'], t['policy_id'], t['activity_type'])

    @staticmethod
    def execute():

        print("Fetching Data...")
        #url = 'https://v3v10.vitechinc.com/solr/participant/select?indent=on&q=marital_status:S&wt=json&rows=10000'
        #participants = requests.get(url).json()["response"]["docs"]
        client = MongoClient()
        db = client.repo
        collection = db.delphi.finalData2
        participants = collection.find()
        print("Participant count", participants.count())
        #print("Pariticpants: ", participants)

        print("Data Fetched")
        print("Transforming Data...")

        cleanedParticipants = getData.project(participants, getData.cleanData)
        print("Cleaned participants count: ", len(cleanedParticipants))
        print("CLeaned participants: ", cleanedParticipants)
        print("Example Data Entry:")
        print(cleanedParticipants[0])

getData.execute()