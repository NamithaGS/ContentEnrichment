
import json
import tika
import re
from tika import parser
sweetJsonFile=open("/Users/charanshampur/PycharmProjects/CSCI599/SweetLatest.json","r")
ctakesJsonFile=open("Ctakes.json","w")
jsonLoad=json.load(sweetJsonFile)


def getCtakesData(metadata):
    metaDataFormatted={}
    for key,value in metadata.items():
        if "ctakes:DateAnnotation" in key or "ctakes:AnatomicalSiteMention" in key or "ctakes:MeasurementAnnotation" in key or "ctakes:FractionAnnotation" in key:
            metaDataFormatted[key]=value
    return metaDataFormatted

ctakesJson=[]
for doc in jsonLoad:
    print doc["id"]
    ctakesDict={}
    ctakesDict.update(doc)
    if "content" in doc:
        parsedData=parser.from_buffer(doc["content"])
        if "metadata" in parsedData:
            meta=getCtakesData(parsedData["metadata"])
            if(len(meta)>0):
                ctakesDict.update(meta)
    ctakesJson.append(ctakesDict)


json.dump(ctakesJson,ctakesJsonFile,indent=4)
