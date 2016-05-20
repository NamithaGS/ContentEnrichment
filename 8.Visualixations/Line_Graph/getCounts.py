import json, sys
import pprint
import re
from random import randint
timeFile=open("data.tsv","w")
with open('/Users/charanshampur/Sites/MyHtml/circle.json') as jsonFile:
    jsonLoad = json.load(jsonFile)

#rawJSON = rawJSON['response']['docs']

conceptGraph={}
for doc in jsonLoad:
    if "NER_DATE" in doc:
        values = doc["NER_DATE"]
        for v in values:
            match=re.search(r'20[0-1][0-9]',v)
            if(match!=None):
                year = match.group(0)
                if(int(year)>2000 and int(year) < 2017):
                    if year not in conceptGraph:
                        conceptGraph[year]=[1,0,0,0]
                    else:
                        conceptGraph[year][randint(0,3)]+=1
                    break

timeFile.write("date\tclose\n")
for key,value in conceptGraph.items():
    timeFile.write("1-Jan-"+key[2:4]+"\t"+str(value[0])+"\n")
    timeFile.write("1-Apr-"+key[2:4]+"\t"+str(value[1])+"\n")
    timeFile.write("1-Jul-"+key[2:4]+"\t"+str(value[2])+"\n")
    timeFile.write("1-Oct-"+key[2:4]+"\t"+str(value[3])+"\n")
    
timeFile.close()
print "success"