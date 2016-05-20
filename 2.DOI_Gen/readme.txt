Create a DOI generation ContentHandler or Parser in Tika:
---------------------------------------------------------

URL Shortner YOURLS( run Your Own URL Shortener) is used for DOI generation: 
To install and run this URL shortner , a new database needs to be set up, along with changing the configuration and hosting the entire codebase 
in a server running PHP, SQL etc . Output formats can be JSON, XML, or simple raw text. 
API usage:
http://localhost/YOURLS-master/yourls-api.php?title=titleoftheURL&signature=ae6a332cc0&action=shorturl&format=json&url=url
Short URL is created which is unique for every file .  (define( 'YOURLS_UNIQUE_URLS', true ); in config.php)
URL shortner like this works better than writing a new content handler in Tika, as we also get  usage statistics like top clicked links, least clicked links, newest links, etc.

Steps to run the program : URLShortening.php , run it on the server enabled with PHP, SQL ( as mentioned in Yourls)
---------------------------------------------------------------------------------------------------------------------
Input : Measurements.json 
Output : DOI_url.json file 


Steps to run the program : UpdateJson.py <inputfile.txt>
------------------------------------------------------
Inout : Measurements.json 
Output : Measurementsnew.json 
(Contains the updated file with filenames replaced with DOIs)