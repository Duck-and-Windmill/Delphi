import datetime
from pymongo import MongoClient
from dateutil.relativedelta import relativedelta

class cleanParticipantData():
    def project(R, p):
        return [p(t) for t in R]
    def cleanParticipants(t):
        sex = 1 if (t["sex"] == "M") else 0
        married = 1 if (t["marital_status"] == "M") else 0
        birth = datetime.datetime.strptime(t["birth_date"].split("T")[0], "%Y-%m-%d")
        age = relativedelta(datetime.datetime.now(), birth).years
        return {"id": t["id"], "sex": sex, "married": married, "age": age, "lng": t["longitude"], "lat": t["latitude"]}

    @staticmethod
    def execute():
        client = MongoClient()
        repo = client.repo

        print("Loading Data...")

        participants = repo['delphi.participants']
        print("Loaded Participants")

        print("Transforming Participants...")
        cleanedParticipants = cleanParticipantData.project(participants.find(), cleanParticipantData.cleanParticipants)

        print("Saving Cleaned Participants...")
        repo.drop_collection("delphi.cleanedParticipants")
        repo.create_collection("delphi.cleanedParticipants")
        repo['delphi.cleanedParticipants'].insert_many(cleanedParticipants)

        print("Done")
        repo.logout()

cleanParticipantData.execute()