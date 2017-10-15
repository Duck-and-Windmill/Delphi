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

        print("Generating Product of Participants and Policies...")
        participantsAndPolicies = list(itertools.product(cleanedParticipants, policies))
        print("Product Generated")
        print(len(participantsAndPolicies))

        print("Selecting for matching Participants and Policies...")
        selectedParticipantsAndPolicies = finalTransform.select(participantsAndPolicies, finalTransform.equalParticipantsAndPolicies)
        print("Selection Complete")
        print(len(selectedParticipantsAndPolicies))

        selectedParticipantsAndPolicies = []
        for policy in policies:
            participant = cleanedParticipants.find({"id": policy["participant_id"]})
            participant["promo_codes"] = policy["promo_codes"]

        print("Projecting Participants with Policy Promo Code...")
        projectedParticipantsAndPolicies = finalTransform.project(selectedParticipantsAndPolicies, finalTransform.cleanParticipantsAndPolicies)
        print("Projection Complete")
        print(len(projectedParticipantsAndPolicies))



        print("Generating Product of PP and Activities...")
        ppAndActivities = list(itertools.product(projectedParticipantsAndPolicies, activities.find({"promocodes": {"$ne": "NA"}})))
        print("Product Generated")
        print(len(ppAndActivities))

        print("Selecting for matching Promo Codes...")
        selectedPPAndActivities = finalTransform.select(ppAndActivities, finalTransform.equalPPAndActivities)
        print("Selection Complete")
        print(len(selectedPPAndActivities))

        print("Projecting PP with Activity Type...")
        projectedPPAndActivities = finalTransform.project(selectedPPAndActivities, finalTransform.cleanPPAndActivities)
        print("Projection Complete")
        print(len(projectedPPAndActivities))

        print("Saving Data...")
        repo.drop_collection("delphi.finalData")
        repo.create_collection("delphi.finalData")
        repo['delphi.finalData'].insert_many(projectedPPAndActivities)

        print("Done")
        repo.logout()

finalTransform.execute()