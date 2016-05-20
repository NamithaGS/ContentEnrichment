
import json
import tika
import re
from tika import parser
mergeJsonFile=open("/Users/charanshampur/PycharmProjects/assign2/Merged.json","r")
sweetJsonFile=open("Sweet.json","w")
jsonLoad=json.load(mergeJsonFile)

def getSweetNer(metaData):
    metaDataFormatted={}
    for key,value in metaData.items():
        if(re.match("NER",key)):
            metaDataFormatted[key]=value
    return metaDataFormatted

sweetJson=[]
for doc in jsonLoad:
    print doc["id"]
    sweetDict={}
    sweetDict.update(doc)
    if "content" in doc:
        parsedData=parser.from_buffer(doc["content"])
        if "metadata" in parsedData:
            meta=getSweetNer(parsedData["metadata"])
            if(len(meta)>0):
                sweetDict.update(meta)
    sweetJson.append(sweetDict)

json.dump(sweetJson,sweetJsonFile,indent=4)





