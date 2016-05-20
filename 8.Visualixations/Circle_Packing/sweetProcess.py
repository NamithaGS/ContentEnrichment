
import json
import re
import operator
sweetJsonFile=open("/Users/charanshampur/PycharmProjects/CSCI599/Sweet.json","r")
jsonLoad=json.load(sweetJsonFile)

sweetConcepts={}
sweetConceptsList={}
for doc in jsonLoad:
    for key,value in doc.items():
        if(re.match("NER_SWEET",key)):
            if key not in sweetConcepts:
                sweetConcepts[key]=1
                if type(value) is list:
                    sweetConceptsList[key]=[x for x in value]
                else:
                    sweetConceptsList[key]=[value]
            else:
                sweetConcepts[key]+=1
                if type(value) is list:
                    for v in value:
                        if v not in sweetConceptsList[key]:
                            sweetConceptsList[key].append(v)
                else:
                    if value not in sweetConceptsList[key]:
                        sweetConceptsList[key].append(value)

sorted_x = sorted(sweetConcepts.items(), key=operator.itemgetter(1))
print sorted_x
print sweetConceptsList