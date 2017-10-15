from pymongo import MongoClient

class finalTransform():
    @staticmethod
    def execute():
        client = MongoClient()
        repo = client.repo

        print("Loading Data...")
        cleanedParticipants = repo['delphi.cleanedParticipants']
        print("Loaded Participants")
        policies = repo['delphi.policies'].find()
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

        finalSet = []
        print("Generating Product of PP and Activities...")
        count = 0
        for person in projectedParticipantsAndPolicies:
            activity = activities.find_one({"promocodes": person["promo_codes"]})
            if activity:
                count += 1
                print("Progress:", count/len(projectedParticipantsAndPolicies))
                person["activity_type"] = activity["activity_type"]              
                person["lng"] = float(person["lng"])
                person["lat"] = float(person["lat"])
                person.pop("_id", None)
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

try:
    finalTransform.execute()
except BulkWriteError as bwe:
    print(bwe.details)
    print(bwe.details['writeErrors'])
    raise