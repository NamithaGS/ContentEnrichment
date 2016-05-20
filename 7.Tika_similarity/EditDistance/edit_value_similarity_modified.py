#!/usr/bin/env python2.7
#
# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#

from tika import parser
import urllib2
import os, editdistance, itertools, argparse, csv
from requests import ConnectionError
from time import sleep
import json


def stringify(attribute_value):
    try:
        if isinstance(attribute_value, list):
            return str((", ".join(str(attribute_value))).encode('utf-8').strip())
        else:
            return str(str(attribute_value).encode('utf-8').strip())
    except:
        print("Debug")

def computeScores(inputDir, outCSV, acceptTypes, allKeys):
    na_metadata = ["resourceName"]
    with open(outCSV, "wb") as outF:
        a = csv.writer(outF, delimiter=',')
        a.writerow(["x-coordinate","y-coordinate","Similarity_score"])

        filename_list = []

        for root, dirnames, files in os.walk(inputDir):
            dirnames[:] = [d for d in dirnames if not d.startswith('.')]
            for filename in files:
                if not filename.startswith('.'):
                    filename_list.append(os.path.join(root, filename))
        try:
            filename_list = [filename for filename in filename_list if "metadata" in parser.from_file(filename)]
        except ConnectionError:
            sleep(1)

        

        if acceptTypes:
            filename_list = [filename for filename in filename_list if str(parser.from_file(filename)['metadata']['Content-Type'].encode('utf-8')).split('/')[-1] in acceptTypes]
        else:
            print "Accepting all MIME Types....."

        files_tuple = itertools.combinations(filename_list, 2)
        for file1, file2 in files_tuple:
            try:           
                row_edit_distance = [file1, file2]            

                file1_parsedData = parser.from_file(file1)
                file2_parsedData = parser.from_file(file2)
                
                intersect_features = set(file1_parsedData["metadata"].keys()) & set(file2_parsedData["metadata"].keys()) 
                            
                intersect_features = [feature for feature in intersect_features if feature not in na_metadata ]

                file_edit_distance = 0.0
                for feature in intersect_features:

                    file1_feature_value = stringify(file1_parsedData["metadata"][feature])
                    file2_feature_value = stringify(file2_parsedData["metadata"][feature])

                    if len(file1_feature_value) == 0 and len(file2_feature_value) == 0:
                        feature_distance = 0.0
                    else:
                        feature_distance = float(editdistance.eval(file1_feature_value, file2_feature_value))/(len(file1_feature_value) if len(file1_feature_value) > len(file2_feature_value) else len(file2_feature_value))
                    
                    file_edit_distance += feature_distance

            
                if allKeys:
                    file1_only_features = set(file1_parsedData["metadata"].keys()) - set(intersect_features)
                    file1_only_features = [feature for feature in file1_only_features if feature not in na_metadata]

                    file2_only_features = set(file2_parsedData["metadata"].keys()) - set(intersect_features)
                    file2_only_features = [feature for feature in file2_only_features if feature not in na_metadata]

                    file_edit_distance += len(file1_only_features) + len(file2_only_features)       # increment by 1 for each disjunct feature in (A-B) & (B-A), file1_disjunct_feature_value/file1_disjunct_feature_value = 1
                    file_edit_distance /= float(len(intersect_features) + len(file1_only_features) + len(file2_only_features))

                else:
                    file_edit_distance /= float(len(intersect_features))    #average edit distance

                row_edit_distance.append(1-file_edit_distance)
                a.writerow(row_edit_distance)

            except ConnectionError:
                sleep(1)
            except KeyError:
                continue


def compute_score_withjson(json_input_file, outCSV, acceptTypes, allKeys):
    f = open(os.getcwd()+"\\test.json","w")
    na_metadata = ["resourceName"]
    with open(outCSV, "wb") as outF:
        a = csv.writer(outF, delimiter=',')
        a.writerow(["x-coordinate","y-coordinate","Similarity_score"])
        metadata_dict={}
        with open(json_input_file) as inputfile:
            parsedData = json.load(inputfile)
            parsedData = parsedData.get("response").get("docs")
        f.write(str(parsedData))
        for doc in parsedData:
            metadata_dict[doc["id"]]=doc
        files_tuple = itertools.combinations(metadata_dict.keys(), 2)
        for file1, file2 in files_tuple:
            try:
                row_edit_distance = [file1, file2]

                file1_metadata = metadata_dict[file1]
                file2_metadata = metadata_dict[file2]

                intersect_features = set(file1_metadata.keys()) & set(file2_metadata.keys())

                intersect_features = [feature for feature in intersect_features if feature not in na_metadata ]

                file_edit_distance = 0.0
                for feature in intersect_features:

                    file1_feature_value = stringify(file1_metadata[feature])
                    file2_feature_value = stringify(file2_metadata[feature])

                    if len(file1_feature_value) == 0 and len(file2_feature_value) == 0:
                        feature_distance = 0.0
                    else:
                        feature_distance = float(editdistance.eval(file1_feature_value, file2_feature_value))/(len(file1_feature_value) if len(file1_feature_value) > len(file2_feature_value) else len(file2_feature_value))

                    file_edit_distance += feature_distance

                if allKeys:
                    file1_only_features = set(file1_metadata.keys()) - set(intersect_features)
                    file1_only_features = [feature for feature in file1_only_features if feature not in na_metadata]

                    file2_only_features = set(file2_metadata.keys()) - set(intersect_features)
                    file2_only_features = [feature for feature in file2_only_features if feature not in na_metadata]

                    file_edit_distance += len(file1_only_features) + len(file2_only_features)       # increment by 1 for each disjunct feature in (A-B) & (B-A), file1_disjunct_feature_value/file1_disjunct_feature_value = 1
                    file_edit_distance /= float(len(intersect_features) + len(file1_only_features) + len(file2_only_features))

                else:
                    file_edit_distance /= float(len(intersect_features))    #average edit distance

                row_edit_distance.append(1-file_edit_distance)
                a.writerow(row_edit_distance)

            except ConnectionError:
                sleep(1)
            except KeyError:
                continue
    return

if __name__ == "__main__":
    solr_connection = sys.argv[1]
    metadata_type = sys.argv[2]
    #solr_connection="http://localhost:8984/solr/polardata_1"
    #metadata_type="Measurement"
    #List of fields to fetch from Solr. 
    MeasurementFields = "id,Measurements"
    PublicationFields = "id,title,Author,Publications,grobid*"
    LocationFields = "id,Geographic*"
    SweetFields = "id,NER_SWEET*"
    
    fieldStr=""
    if (metadata_type=="Sweet"):
        fieldStr=SweetFields
    elif (metadata_type=="Measurement"):
        fieldStr=MeasurementFields
    elif (metadata_type=="Publication"):
        fieldStr=PublicationFields
    elif (metadata_type=="Location"):
        fieldStr=LocationFields    
    
    # Create query string to pass to Solr
    #queryString = solr_connection+"/select?q=*%3A*&fl=" + fieldStr + "&wt=json&indent=true&rows=100000"
    queryString = solr_connection+"/select?q=Measurements:*&fl=" + fieldStr + "&wt=json&indent=true&rows=10000"
    #Read query result response from Solr
    response = urllib2.urlopen(queryString).read()
    json_input_file = os.getcwd()+ "/Temp.json"
    
    with open(json_input_file,"w") as f:
        f.write(response)
    compute_score_withjson(json_input_file,os.getcwd()+"\\output.csv","false","true")













