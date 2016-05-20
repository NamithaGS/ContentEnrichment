
Instructions for running different parsers and for setting up website integrated with SOLR.


Note -
exported Variables :
NER_RES = /Users/username/Apache-tika/nerModels
Tika_Server = /Users/username/Apache-tika/tika-1.12/tika-server/target/tika-server-1.12.jar


Task 3 Program : TagRatioParser.py (Tag Ratio and NER using Open NLP) 
---------------------------------------------------------------------
program requirement - Start the OpenNLP server on port 9998, Install BeautifulSoup and bs4
Edit the location of the directory where the common crawl data is present in the program TagRatioParser.py

OpenNLP:
Command for starting Tika Server integrated with open NLP -
java -classpath $NER_RES:$Tika_Server org.apache.tika.server.TikaServerCli --config=Apache-tika/nerModels/tika-config.xml 
This starts the Tika Server on port 9998

Task 4 Program : URLshortening.php ( DOI Generation)
----------------------------------------------------
program requirement - As mentioned in http://yourls.org/#Install , PHP version 5.2 or greater, MySQL version 5.0 or greater, Apache with mod_rewrite enabled, PHP Curl extension installed. SQL data base must be created and 
URLShortening.php , run it on the server enabled with PHP, SQL ( as mentioned in Yourls)
Input : Measurements.json 
Output : DOI_url.json file 

UpdateJson.py <inputfile.txt>
Inout : Measurements.json 
Output : Measurementsnew.json 
(Contains the updated file with filenames replaced with DOIs)

Task 5 and 6 Program : grobidGeotopicParser.py (grobit journal parser and geo topic parser)
-------------------------------------------------------------------------------------------
program requirement - Grobid Service on port 8080, tika-grobid parser on port 9998, tika-geoTopic parser on port 9090, tika-server(defaukt tika) on port 9091
Edit the location of the directory where the common crawl data is present in the program grobidGeotopicParser.py
Have the scholar.py program in the same directory as the above program.
The program also takes as input the output json file generated from previous step.

Due to frequent calls to google scholar api, your system might get blocked from using it. 
WorkAround : open browser visit google scholar enter the captcha, clear the google scholar cookie and export the cookies into a text file and add it in scholar.py program (COOKIE_JAR_FILE). Or you can also create a vpn and then use it https://www.privatetunnel.com/home/

Grobid  :
Command For Starting the grobid service -
cd $HOME/gorbid/grobid/grobid-service
mvn -Dmaven.test.skip=true jetty:run-war
This starts the Grobid Service on port 8080

Command for starting Tika Server integrated with grobid service -
java -classpath $HOME/gorbid/grobidparser-resources/:$Tika_Server org.apache.tika.server.TikaServerCli --config=$HOME/gorbid/grobidparser-resources/tika-config.xml
This starts the Tika Server on port 9998

GeoTopicParser :
I am using the 1.11 snapshot for this, as I am facing some issue with tika-1.12.jar for geo-topic parsing. for remaining all other parsers 1.12 is used
java -classpath /Users/username/nutch/tika/tika/tika-server/target/tika-server-1.11-SNAPSHOT.jar:$HOME/geo-topic/location-ner-model:$HOME/geo-topic/geotopic-mime org.apache.tika.server.TikaServerCli --port=9090

Default_Tika server :
java -jar $Tika_Server --port=9091


Task_7 Program Sweet parser(Sweet Concept extraction and Tika Regex Ner)
------------------------------------------------------------------------
Run the program sweet3.py to extract all the concepts from owl files.

Program Tika_Sweet_Parser.py -
Run the Tika Regex Ner parser with sweet enabled

Tika Sweet Seerver on port 9998
java -Dner.impl.class=org.apache.tika.parser.ner.regex.RegexNERecogniser -classpath $NER_REGEX:$Tika_Server org.apache.tika.server.TikaServerCli --config=/Users/username/Tika_Regex_Ner/tika-config.xml

Run the program Tika_Sweet_Parser.py 
Input : Merged.json file generated from previous steps
output : final Output file to be indexed into SOLR

Standalone sweet extractor-
java -Dner.impl.class=org.apache.tika.parser.ner.regex.RegexNERecogniser -classpath $NER_REGEX:$TIKA_APP org.apache.tika.cli.TikaCLI --config=/Users/username/Tika_Regex_Ner/tika-config.xml -m http://www.cs.usc.edu/faculty_staff/faculty



Tas4 9 and 12 Setting up Solr and the website
---------------------------------------------

The website is constructed using Twitter Bootstrap, and Jquery.

Ingest the data into SOLR using the following command use the schema.xml present with the submission:
curl 'http://localhost:8983/solr/update?commit=true' --data-binary @MetaScoreNew.json -H 'Content-type:application/json'

Copy all the files present inside each of the folders under task_12 into your Server Container (Httpd Server with php support)  

Place the following files in the server root :

[d3.html,process.php,maps.html,world-110m2.json,phpPyth.py,circlePacking.html,getCounts.py,lineGraph.html,wordCloud.py,wordCloud.html,AuthorMap.py,partition.html,d3.js,d3.layout.js,style.css,collapTree.py,collapsibleTree.html]

Edit the process.php file to point to the correct python interpreter and the path to python programs placed on the server root directory.
eg : passthru('/Library/Frameworks/Python.framework/Versions/2.7/bin/python2.7 /Users/username/Sites/MyHtml/phpPyth.py');
change it to the appropriate python Interpreter location in all places in the program.

d3.html is the application entry point.

Task10 : MemexGeoParser
------------------------
Start solr server on 8984 :
solr start -p 8984

Start the geoparser solr server at port port 8983, Inside \GeoParser-master\geoparser_app : 
solr start -p 8983

Start lucene server:
java -cp %HOMELUC%\target\lucene-geo-gazetteer-0.3-SNAPSHOT-jar-with-dependencies.jar edu.usc.ir.geo.gazetteer.GeoNameResolver -i path\to\geoIndex -server

Start Tika_Server  on 8001:
java -cp path\to\location-ner-model;path\to\geotopic-mime;path\to\tika-server-1.12.jar org.apache.tika.server.TikaServerCli --port=8001

Quick check:
curl -T polar.geot -H "Content-Disposition: attachment; filename=polar.geot" http://localhost:8001/rmeta

Run DJANGO:
python manage.py runserver
http://localhost:8000/

Task 14 Ctakes parser(NER using Ctakes)
---------------------------------------

Command for running tika server with ctakes parser :
java -classpath $HOME/ctakes/ctakes-config:/Users/username/nutch/tika/tika/tika-server/target/tika-server-1.11-SNAPSHOT.jar:${CTAKES_HOME}/desc:${CTAKES_HOME}/resources:`./gen-server-classpath.sh` org.apache.tika.server.TikaServerCli --config=$HOME/ctakes/ctakes-config/tika-config.xml

Execute the program ctakesParser.py 
Input file : Json file generated from Task 7