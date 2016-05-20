import json
import re

#Merge the data extracted from steps 3,4, 5 and 6 into a single JSON file which will be loaded into Solr
file_path1 = "Measurement.json"
file_path2 = "Publication.json"
file_path3 = "Sweet.json"
merged_file_path = "Merged.json"

writejsonToFile = open(merged_file_path,"w")
jsonData = {}
json_data=open(file_path1).read()
data_measurements = json.loads(json_data)
json_data=open(file_path2).read()
data_publications = json.loads(json_data)
json_data=open(file_path3).read()
data_sweet = json.loads(json_data)


#Merge data from all three files based on the "id" field, which is nothing but the unique file name
#Generate a metadata score for each file, based on certain attributes which are important for our schema/visualizations
for key, value in data_measurements.iteritems():
   modified_id = "http://polar.usc.edu/" + key.replace('/Users/charanshampur/newAwsDump/testFiles2/','')
   jsonData["id"] = modified_id
   jsonData.update(value)
   score=0;
   if "NER_DATE" in jsonData:
    score = score + 1
   if "NER_LOCATION" in jsonData:
    score = score + 1
   if "Measurements" in jsonData:
    score = score + 1
   
   try:
       publicationData = data_publications.get(key)
       if "Geographic_Latitude" in publicationData:
           score = score + 1
       if "Geographic_LONGITUDE" in publicationData:
           score = score + 1
       if "Geographic_NAME" in publicationData:
           score = score + 1
       if "Publications" in publicationData:
           score = score + 1
       if ("Author" in publicationData) |   ("grobid:header_Author" in publicationData):
           score = score + 1
       if ("title" in publicationData) |   ("grobid:header_Title" in publicationData):
           score = score + 1
           
       jsonData.update(publicationData)
   except TypeError:
       #Do nothing
       jsonData=jsonData
   
   try:
       sweetData = data_sweet.get(modified_id)
       jsonData.update(sweetData)
       if (re.match("NER_SWEET",sweetData)):
           score = score + 1
   except:
       print(modified_id) 
   jsonData["Meta_Score"] = score;
   json.dump(jsonData,writejsonToFile)
