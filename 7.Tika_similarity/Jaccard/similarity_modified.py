
import os
import json
import operator
import urllib2
import sys
def convertUnicode( fileDict ) :
	fileUTFDict = {}
	for key in fileDict:
		if isinstance(key, unicode) :
			key = key.encode('utf-8').strip()
		value = fileDict.get(key)
		if isinstance(value, unicode) :
			value = value.encode('utf-8').strip()
		fileUTFDict[key] = value

	return str(fileUTFDict)

#Modified function to calculate similarity based on the JSON output produced by Solr
def calculate_similarity(json_input_file,metadata_type):
	dirFile = ""
	filenames = []
	filename_list = []
	allowed_mime_types = []
	directory_flag = 0
	union_feature_names = set()
	resemblance_scores = {}
	file_parsed_data ={}

	with open(json_input_file) as inputfile:
		parsedData = json.load(inputfile)
		parsedData = parsedData.get("response").get("docs")
		count=0
		for doc in parsedData:
			count=count+1
			file_parsed_data[doc["id"]] = doc
			union_feature_names = union_feature_names | set(doc.keys())
		total_num_features = len(union_feature_names)
	print union_feature_names
# now compute the specific resemblance and containment scores
	for filename in file_parsed_data:
		overlap = {}
		overlap = set(file_parsed_data[filename].keys()) & set(union_feature_names)
		resemblance_scores[filename] = float(len(overlap))/total_num_features
		
	sorted_resemblance_scores = sorted(resemblance_scores.items(), key=operator.itemgetter(1), reverse=True)
	
	f = open("similarity-scores.txt", "w")
	f.write("Resemblance : \n")
	for tuple in sorted_resemblance_scores:
		f.write(os.path.basename(tuple[0].rstrip(os.sep)) + ","+str(tuple[1]) + "," + tuple[0] + "," + convertUnicode(file_parsed_data[tuple[0]]) + '\n')
		
if __name__ == "__main__":
	solr_connection = sys.argv[1]
	metadata_type = sys.argv[2]
	#solr_connection="http://localhost:8983/solr/polardata"
	#metadata_type="Measurement"
	#List of fields to fetch from Solr. 
	MeasurementFields = "NER_PERSON,NER_MONEY,NER_PERCENT,NER_TIME,NER_LOCATION,NER_ORGANIZATION,NER_DATE,Measurements"
	PublicationFields = "title,Author,Publications,grobid*"
	LocationFields = "Geographic*"
	SweetFields = "NER_SWEET*"
	Allfields ="id" + "," + MeasurementFields + "," + PublicationFields + "," + LocationFields + "," + SweetFields
	fieldStr=""
	if (metadata_type=="Sweet"):
		fieldStr="id" + SweetFields
	elif (metadata_type=="Measurement"):
		fieldStr="id" + MeasurementFields
	elif (metadata_type=="Publication"):
		fieldStr="id"  + PublicationFields
	elif (metadata_type=="Location"):
		fieldStr="id" + LocationFields	
	elif (metadata_type=="All"):
		fieldStr="id" + Allfields	
	
	# Create query string to pass to Solr
	queryString = solr_connection+"/select?q=*%3A*&fl=" + fieldStr + "&wt=json&indent=true&rows=100000"
	#Read query result response from Solr
	response = urllib2.urlopen(queryString).read()
	json_input_file = os.getcwd()+ "/Temp.json"
	
	with open(json_input_file,"w") as f:
		f.write(response)
	calculate_similarity(json_input_file,metadata_type)




