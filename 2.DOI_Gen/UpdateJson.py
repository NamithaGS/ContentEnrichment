__author__ = 'namitha'
import json
import yaml
import sys


# File with the Filename vs DOI
fpDOI = open("DOI_url.json","r")
json_object_DOI = json.loads(fpDOI.read())
# Location of the file to be converted
aa = sys.argv[1]
fpMeasurement = open(aa,"r")
json_objec_Measurement = json.loads((fpMeasurement.read()))
# Measuement file with DOIs instead of filepath
DOInewfile = open(aa.split(".")[0]+"new.json","w")


#Get url and short url in 2 dict
bb = json_object_DOI.get('DOI',{})
urldict = [bb[i]['url'] for i in range(0,len(bb))]
shorturldict = [bb[i]['shorturl'] for i in range(0,len(bb))]

urldict = [str(x) for x in urldict]
shorturldict = [str(x) for x in shorturldict]

json_objec_Measurementnew ={}
##json_objec_Measurement = unicode(json_objec_Measurement,"utf-8")
for key, value in list(json_objec_Measurement.items()):
    idname = ("http://"+(str(key).split("/")[-1])).lower()
    print idname
    index1 = urldict.index(idname)
    print index1
    shorturl = shorturldict[index1]
    print shorturl
    cc = unicode.decode(key,'utf-8')
    json_objec_Measurementnew[shorturl]= value
json.dump(json_objec_Measurementnew,DOInewfile,indent=4)
DOInewfile.close()

