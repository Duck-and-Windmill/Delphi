import urllib.request
import json
import datetime
import uuid
import requests
from pymongo import MongoClient
from dateutil.relativedelta import relativedelta

class coordsToFloats():
    def project(R, p):
        return [p(t) for t in R]
    def convertCoords(t):
        t["lng"] = float(t["lng"])
        t["lat"] = float(t["lat"])
        return t

    @staticmethod
    def execute():
        client = MongoClient()
        repo = client.repo

        print("Loading Data...")

        finalData = repo['delphi.finalData']
        print("Loaded Final Data")

        print("Transforming Final Data...")
        coordsAsFloats = coordsToFloats.project(finalData.find(), coordsToFloats.convertCoords)

        print("Saving Cleaned Participants...")
        repo.drop_collection("delphi.finalData2")
        repo.create_collection("delphi.finalData2")
        repo['delphi.finalData2'].insert_many(coordsAsFloats)

        print("Done")
        repo.logout()

coordsToFloats.execute()