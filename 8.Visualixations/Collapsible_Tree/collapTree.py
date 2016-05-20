
import json

ctakesJsonFile=open("/Users/charanshampur/Sites/MyHtml/circle.json","r")
locOrgFile=open("output.json","w")
jsonStr=ctakesJsonFile.readline()
jsonLoad=json.loads(jsonStr)


locGraph={}
for doc in jsonLoad:
    if "Geographic_NAME" in doc and "NER_ORGANIZATION" in doc:
        if doc["Geographic_NAME"] not in locGraph:
            if type(doc["NER_ORGANIZATION"]) is list:
                locGraph[doc["Geographic_NAME"]]=[doc["NER_ORGANIZATION"][i] for i in range(0,5) if i < len(doc["NER_ORGANIZATION"])]
            else:
                locGraph[doc["Geographic_NAME"]]=[doc["NER_ORGANIZATION"]]
        else:
            if len(locGraph[doc["Geographic_NAME"]]) < 10:
                if type(doc["NER_ORGANIZATION"]) is list:
                    locGraph[doc["Geographic_NAME"]].extend([doc["NER_ORGANIZATION"][i] for i in range(0,5) if i < len(doc["NER_ORGANIZATION"])])
                else:
                    locGraph[doc["Geographic_NAME"]].extend([doc["NER_ORGANIZATION"]])



def formatRec(link,size):
    return {"name":link,"size":size}

itemList=[]
for k,v in locGraph.items():
    itemDetail={}
    itemDetail["name"]=k;
    itemDetail["children"]=[formatRec(x,5) for x in v]
    itemList.append(itemDetail)

finalLocOrgJson={"name":"Location/Organization","children":itemList}
json.dump(finalLocOrgJson,locOrgFile,indent=4)
print "success"