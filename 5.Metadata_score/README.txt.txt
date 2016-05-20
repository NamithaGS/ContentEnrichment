Program Name: processMetadata.py

This program merges the metadata JSON files from Task 3,5,6 and 7. It then calculates the metadata score as follows:

a)	From the complete list of metadata fields, we shortlist a list of fields which we plan to use for our data analysis. We did this by excluding fields which we think will not be useful in our analysis. For example the “Optional_” fields from the GeoTopic Parser, "content", "Content-Type" fields, etc.
b)	For each document, increment the score by 1 every time a field from this list is encountered.


Instructions to run the program:

1. Place the JSON files which contain the extracted metadata from previous steps in the same folder where the program is placed (Measurement.json, Publication.json and Sweet.json)
2. Run the program. It ouputs a JSON file which is merged with all the metadata fields, along with an additional field - "MetaScore"