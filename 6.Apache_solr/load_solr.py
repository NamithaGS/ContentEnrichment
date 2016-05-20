import sys
import os

def load_solr(solr_directory,file_path):
    #Load the merged data into Solr   
    solrjar = solr_directory + '\dist\solr-core-5.5.0.jar"'
    command = "java -classpath " + solrjar + " -Dauto=yes -Dc=polardata -Ddata=files org.apache.solr.util.SimplePostTool " + file_path
    os.system(command)

if __name__ == "__main__":
    solr_directory = sys.argv[1]
    file_path = sys.argv[2]
    #solr_directory = '"C:\\Users\\Manisha Kampasi\\Downloads\\solr-5.5.0\\solr-5.5.0\\'
    load_solr(solr_directory,file_path)
    
    