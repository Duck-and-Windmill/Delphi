from pymongo import MongoClient
import rtree
from statistics import mode

class createMapCoords():
    @staticmethod
    def execute():
        client = MongoClient()
        repo = client.repo

        print("Loading Data...")

        finalData = repo['delphi.finalData'].find()
        capitals = repo['delphi.capitals'].find()
        print("Loaded Final Data")

        print("Building RTree...")
        participantsRTree = rtree.index.Index()
        totalCount = finalData.count()
        count = 0
        for i in range(totalCount):
            bounds = (float(finalData[i]['lng']), float(finalData[i]['lat']), float(finalData[i]['lng']), float(finalData[i]['lat']))
            participantsRTree.insert(i, bounds)
            count += 1
            print("Progress:", count/totalCount)

        print("Finding Nearest Participants to each Capital...")
        finalList = []
        count = 0
        totalCount = capitals.count()
        for capital in capitals:
            bounds = (float(capital['long']), float(capital['lat']), float(capital['long']), float(capital['lat']))
            nearestIndices = participantsRTree.nearest(bounds, 100)
            nearest = [finalData[i] for i in nearestIndices]
            activities = [t["activity_type"] for t in nearest]
            capital.pop("_id")
            capital["activity_type"] = {"Email": activities.count("Email")/len(activities), "Call": activities.count("Call")/len(activities), "Letter": activities.count("Letter")/len(activities)}
            finalList.append(capital)
            count += 1
            print("Progress:", count/totalCount)

        print("Saving Capitals with Activity Type...")
        repo.drop_collection("delphi.finalCapitals")
        repo.create_collection("delphi.finalCapitals")
        repo['delphi.finalCapitals'].insert_many(finalCapitals)

        print("Done")
        repo.logout()

createMapCoords.execute()