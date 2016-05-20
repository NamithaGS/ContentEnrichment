
import rdflib
import glob
import json
path=glob.glob("/Users/charanshampur/sweet/2.3/*")
outputOntologyHierFile=open("OntologyHier.json","w")
outRegexFile=open("RegexSweet.txt","w")
g=rdflib.Graph()
OntologyGraph={}

for file in path:
    g.load(file)
    for s,p,o in g:
        sub = s.split("#")
        pred = p.split("#")
        obj = o.split("#")
        if(len(pred)>1):
            if(pred[1] in "subClassOf"):
                if(len(sub)>1 and len(obj)>1):
                    if(obj[1] not in OntologyGraph):
                        OntologyGraph[obj[1]]=[sub[1]]
                    else:
                        if(sub[1] not in OntologyGraph[obj[1]]):
                            OntologyGraph[obj[1]].append(sub[1])

json.dump(OntologyGraph,outputOntologyHierFile,indent=4)

for key,value in OntologyGraph.items():
    regex=""
    listNew=[]
    for val in value:
        newVal=""
        newVal=val[0]
        for i in range(1,len(val)):
            if(str(val[i]).isupper()):
                newVal+=' '+val[i]
            else:
                newVal+=val[i]
        listNew.append(newVal)
    regex+="SWEET_"+key+"=("+"|".join(listNew)+")"
    outRegexFile.write(regex+"\n")
