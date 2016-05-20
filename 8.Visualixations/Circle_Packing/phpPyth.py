
import json
import re
import operator
inputJsonFile = open("/Users/charanshampur/Sites/MyHtml/circle.json","r")
#flareFile=open("/Users/charanshampur/solr/lucene_solr_4_10/solr/example/solr-webapp/webapp/MyHtml/flare.json","w")
circlePackJsonFile=open("flare.json","w")
jsonStr=inputJsonFile.readline()
gunCollec={}
jsonLoad = json.loads(jsonStr)
sweetConcepts=["NER_SWEET_MesoscaleWind","NER_SWEET_Landform","NER_SWEET_WaterSubstance","NER_SWEET_EcologicalDynamics","NER_SWEET_Phenomena","NER_SWEET_ElectromagneticProcess","NER_SWEET_Hydrosphere","NER_SWEET_Sediment","NER_SWEET_AstronomicalBody","NER_SWEET_ChemicalReaction","NER_SWEET_Glacier","NER_SWEET_Force","NER_SWEET_ChemicalProcess","NER_SWEET_Environment","NER_SWEET_PlanetaryScience","NER_SWEET_Animal","NER_SWEET_Ice","NER_SWEET_Geology","NER_SWEET_FossilFuel","NER_SWEET_WaterSubstance"]

conceptGraph={}
for doc in jsonLoad:
    for key,value in doc.items():
        if key in sweetConcepts:
            if key not in conceptGraph:
                conceptGraph[key]={}
                if(type(value) is list):
                    for v in value:
                        conceptGraph[key].update({v:[doc["id"]]})
                else:
                    conceptGraph[key].update({value:[doc["id"]]})
            else:
                if(type(value)is list):
                    for v in value:
                        if v in conceptGraph[key]:
                            conceptGraph[key][v].append(doc["id"])
                        else:
                            conceptGraph[key].update({v:[doc["id"]]})
                else:
                    if value in conceptGraph[key]:
                        conceptGraph[key][value].append(doc["id"])
                    else:
                        conceptGraph[key].update({value:[doc["id"]]})

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

finalFlareJson={"name":"flare","children":conceptList}

json.dump(finalFlareJson,circlePackJsonFile,indent=4)
print "success"