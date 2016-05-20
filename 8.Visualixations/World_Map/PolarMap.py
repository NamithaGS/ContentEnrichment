
import json
import re
import operator
sweetJsonFile=open("/Users/charanshampur/PycharmProjects/CSCI599/Sweet.json","r")
citiesFile=open("cities2.csv","w")
jsonLoad=json.load(sweetJsonFile)

cities=[]
citiesFile.write("code,city,country,lat,lon"+"\n")
for doc in jsonLoad:
    if "Geographic_NAME" in doc:
        if doc["Geographic_NAME"] not in cities:
            cities.append(doc["Geographic_NAME"])
            locLine="xxx,"+doc["Geographic_NAME"]+",UnitedStates,"+doc["Geographic_LATITUDE"]+","+doc["Geographic_LONGITUDE"]+"\n"
            locLine=locLine.encode("ascii",errors="ignore")
            citiesFile.write(locLine)

citiesFile.close()
sweetJsonFile.close()




