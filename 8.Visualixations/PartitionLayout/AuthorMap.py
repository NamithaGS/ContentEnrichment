
import json

sweetJsonFile=open("/Users/charanshampur/Sites/MyHtml/circle.json","r")
jsonStr=sweetJsonFile.readline()
jsonLoad = json.loads(jsonStr)

authorJsonFile=open("author.json","w")

conceptGraph={}
for doc in jsonLoad:
    if "Publications" in doc and "Author" in doc:
            authorDic={}
            authorDic[doc["Author"]]=[doc["Publications"][x] for x in range(0,20) if x < len(doc["Publications"])]
            if "Geographic_NAME" in doc:
                if doc["Geographic_NAME"] not in conceptGraph:
                    conceptGraph[doc["Geographic_NAME"]]=authorDic
                else:
                    conceptGraph[doc["Geographic_NAME"]].update(authorDic)
            else:
                if "others" not in conceptGraph:
                    conceptGraph["others"]=authorDic
                else:
                    conceptGraph["others"].update(authorDic)

def formatRec(link,size):
    return {"name":link,"size":size}

conceptList=[]
for key,value in conceptGraph.items():
    conceptDetail={}
    conceptDetail["name"]=key
    itemList=[]
    for k,v in value.items():
        itemDetail={}
        itemDetail["name"]=k;
        itemDetail["children"]=[formatRec(x,len(v)) for x in v]
        itemList.append(itemDetail)
    conceptDetail["children"]=itemList
    conceptList.append(conceptDetail)

finalAuthorJson={"name":"Location/Author","children":conceptList}
json.dump(finalAuthorJson,authorJsonFile,indent=4)
print "success"