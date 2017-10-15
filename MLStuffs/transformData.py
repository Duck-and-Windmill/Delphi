import urllib.request
import json
import datetime
import uuid
import requests
from pymongo import MongoClient
from dateutil.relativedelta import relativedelta

class transformData():
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

    def cleanParticipants(t):
        sex = 1 if (t["sex"] == "M") else 0
        married = 1 if (t["marital_status"] == "M") else 0
        birth = datetime.datetime.strptime(t["birth_date"].split("T")[0], "%Y-%m-%d")
        age = relativedelta(datetime.datetime.now(), birth).years
        return {"id": t["id"], "sex": sex, "married": married, "age": age, "coords": (t["longitude"], t["latitude"])}

    @staticmethod
    def execute():
        client = MongoClient()
        repo = client.repo

        print("Loading Data...")

        participants = repo['delphi.participants']
        print("Loaded Participants")
        policies = repo['delphi.policies']
        print("Loaded Policies")
        activities = repo['delphi.activities']
        print("Loaded Activities")

        print("Transforming Participants...")
        cleanedParticipants = transformData.project(participants.find(), transformData.cleanParticipants)

        print("Saving Cleaned Participants...")
        repo.drop_collection("delphi.cleanedParticipants")
        repo.create_collection("delphi.cleanedParticipants")
        repo['delphi.cleanedParticipants'].insert_many(cleanedParticipants)

        print("Done")
        repo.logout()

transformData.execute()