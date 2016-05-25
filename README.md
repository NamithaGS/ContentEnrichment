# ContentEnrichment

# Synopsis
Content Enrichment in the Text Retrieval Conference (TREC) Polar Dynamic Domain Dataset

## Motivation
Performing Content Extraction, Extracting Metadata, Information Clustering and Similarity, and Named Entity Recognition – to
scientifically enrich the Polar dataset and to contribute to http://polar.usc.edu , a new website being created to provide Polar Data Insights to the scientific community

## Tasks
1. Context Extraction Enrichment – Applying the Tag Ratios algorithm to
identify text, and you will construct a Tika parser to extract Measurement 
mentions from text automatically. </br>

2. Metadata Enrichment – Applying the GROBID journal parser with Tika, and
extract TEI metadata, and also scientific publication metadata using the Google
Scholar API to develop a network of related scientific publications to your Polar
dataset, and to map publications to the data. In addition, classifying the data
using a common Earth science domain model, ontology, called SWEET, for
Semantic Web for Earth and Environmental Terminology
(http://sweet.jpl.nasa.gov/). Also creating Digital Object Identifiers (DOIs)
for your data. </br>

3. Information Similarity and Clustering – Creating clusters of your Polar data
using the enriched measurements extracted, and using the enriched metadata, and
browse and expose your information using Data-Driven-Documents visualizations
after ingesting data into Apache Solr and/or ElasticSearch. </br>

4. Named Entity Recognition (NER) – Applying geospatial NER using the
GeoTopicParser in Apache Tika and using the MEMEX GeoParser tools

## Contributors
Charan Shampur </br>
Manisha Kampasi

## License
Apache Tika
https://tika.apache.org/license.html
