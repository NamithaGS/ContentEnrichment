similarity_modified.py

This program is based on the similarity.py program to calculate Jaccard distance based on Keys (golden feature set)

We made the following changes to this program:
a)	Updated the program to use the metadata extracted from our Solr index (in JSON format)
b)	Instead of extracting the basic metadata from TIKA python, our program uses the metadata we extracted from steps 3, 5, 6 and 7.
c)	The rest of the logic to calculate the Jaccard distance is the same as before.
 
Instructions to run the program:
Run the following command:  similarity_modified.py "<URL where Solr is hosted><core name>" <metadata type>

The meta data type can be one of the following - Measurement, Publication, Location, Sweet or All 

Example: similarity_modified.py "http://localhost:8983/solr/polardata" "Sweet"

This program outputs the similarity-scores.txt file which will then be run against the following programs from TIKA Similarity library:

1.cluster-scores.py
2.circle-packing.py
3.generateLevelCluster.py
 
The visualizations generated for each of the metadata types have been stored in the corresponding folders.