import urllib.request
import json
import datetime
import uuid
import requests
import dml

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

    def cleanData(t):
        # ID, Sex, Marital Status, Birth Date, (Lng, Lat)
        return (t["id"], t["sex"], t["marital_status"], t["birth_date"], (t["longitude"], t["latitude"]))

    @staticmethod
    def execute():
        client = dml.pymongo.MongoClient()
        repo = client.repo

        participants = repo['delphi.participants']
        policies = repo['delphi.policies']
        activities = repo['delphi.activities']

        repo.dropCollection("activities")
        repo.createCollection("activities")
        repo['delphi.activities'].insert_many(activities)
        repo['delphi.activities'].metadata({'complete':True})

        repo.dropCollection("activities")
        repo.createCollection("activities")
        repo['delphi.activities'].insert_many(activities)
        repo['delphi.activities'].metadata({'complete':True})

        repo.dropCollection("activities")
        repo.createCollection("activities")
        repo['delphi.activities'].insert_many(activities)
        repo['delphi.activities'].metadata({'complete':True})

        repo.logout()

transformData.execute()