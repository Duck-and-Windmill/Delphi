import urllib.request
import json
import datetime
import uuid
import requests
from pymongo import MongoClient
from dateutil.relativedelta import relativedelta
import itertools

class finalTransform():
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

    def equalParticipantsAndPolicies(t):
        return t[0]['id'] == t[1]['participant_id']

    def cleanParticipantsAndPolicies(t):
        finalObj = t[0]
        finalObj['promo_codes'] = t[1]['promo_codes']
        return finalObj

    def equalPPAndActivities(t):
        return t[0]['promo_codes'] == t[1]['promocodes']

    def cleanPPAndActivities(t):
        finalObj = t[0]
        finalObj['activity_type'] = t[1]['activity_type']
        return finalObj

    @staticmethod
    def execute():
        client = MongoClient()
        repo = client.repo

        print("Loading Data...")
        cleanedParticipants = repo['delphi.cleanedParticipants']
        print("Loaded Participants")
        policies = repo['delphi.policies'].find({"promo_codes": {"$exists": True}})
        print("Loaded Policies")
        activities = repo['delphi.activities']
        print("Loaded Activities")

        policyCount = policies.count()
        projectedParticipantsAndPolicies = []
        print("Generating Product of Participants and Policies...")
        count = 0
        for policy in policies:
            participant = cleanedParticipants.find_one({"id": policy["participant_id"]})
            if (participant):
                count += 1
                print("Progress:", count/policyCount)
                participant["promo_codes"] = policy["promo_codes"]
                participant["policy_id"] = policy["id"]
                projectedParticipantsAndPolicies.append(participant)
        print("Product Generated")
        print(len(projectedParticipantsAndPolicies))

        """projectedParticipantsAndPolicies = []
        print("Generating Product of Participants and Policies...")
        count = 0
        for person in cleanedParticipants:
            policy = policies.find_one({"participant_id": person["id"], "promo_codes": {"$exists": True}})
            if policy:
                count += 1
                print("Progress:", count/cleanedParticipants.count())
                person["promo_codes"] = policy["promo_codes"]
                projectedParticipantsAndPolicies.append(person)
        print("Product Generated")
        print(len(projectedParticipantsAndPolicies))"""

        finalSet = []
        print("Generating Product of PP and Activities...")
        count = 0
        for person in projectedParticipantsAndPolicies:
            activity = activities.find_one({"promocodes": person["promo_codes"]})
            if activity:
                count += 1
                print("Progress:", count/len(projectedParticipantsAndPolicies))
                person["activity_type"] = activity["activity_type"]
                finalSet.append(person)
        print("Product Generated")
        print(len(finalSet))
        print(finalSet[0])

        print("Saving Data...")
        repo.drop_collection("delphi.finalData")
        repo.create_collection("delphi.finalData")
        repo['delphi.finalData'].insert_many(finalSet)

        print("Done")
        repo.logout()

finalTransform.execute()