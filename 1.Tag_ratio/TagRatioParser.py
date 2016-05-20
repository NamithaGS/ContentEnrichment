
from tika import detector
from tika import parser
from HTMLParser import HTMLParser
import os
from bs4 import BeautifulSoup
import math
import re
import json
import subprocess

# List of files for which tag ratio parsing has to be called.
tagRatioFileTypes=["text/html","application/rss+xml","application/xhtml+xml", "application/atom+xml", "application/rdf+xml", "application/xml"]

# List of files having html tags.
htmlFileTypes=["text/html","application/xhtml+xml"]

# Location of directory from which files have to be parsed.
path = "/Users/charanshampur/newAwsDump/testFiles2"

# Json file contains the NER metadata and Measurements identified from each file.
measurementFile = open("Measurement.json","w")

# error file contains location of file for which tika failed parsing.
errorFile = open("Tika_Parse_Error_File","w")

# Location of tika snapshot file.
tikaSnapshotPath = "/Users/charanshampur/Apache-tika/tika-1.12/tika-app/target/tika-app-1.12.jar"

#This class inherits the HTMLParser class and overrides its methods for counting the tag non tag characters.
class MyHTMLParser(HTMLParser):
    def setVariables(self):
        self.tagCharCount=0
        self.textCharCount=0
    def handle_starttag(self, tag, attrs):
        self.tagCharCount+=len(tag)
        try:
            self.tagCharCount+=sum([len(attr[0])+len(attr[1]) for attr in attrs])
        except:
            self.tagCharCount=0
            pass
    def handle_endtag(self, tag):
        self.tagCharCount+=len(tag)
    def handle_data(self, data):
        self.textCharCount+=len(data)
    def getTagCount(self):
        return self.tagCharCount
    def getTextCount(self):
        return self.textCharCount

# This function performs smoothing of the tag ratios calculated for each line of the file.
def performSmoothing(tagRatiosOfDoc):
    radius=2
    tagRatioSmooth={}
    n=tagRatiosOfDoc.__len__()-1
    if(n<3):
        return tagRatiosOfDoc
    for key,value in tagRatiosOfDoc.items():
        if key<2:
            i=0
            j=key+radius
        elif key>n-2:
            i=key-radius
            j=n
        else :
            i=key-radius
            j=key+radius
        sumOfSmooth=sum([tagRatiosOfDoc[k] for k in range(i,j+1)] )
        tagRatioSmooth[key]=sumOfSmooth/((2 * radius) + 1)
    return tagRatioSmooth

# This function calculates Standard Deviation which is used as a threshold for clustering Text Content
# present in the file.
def calculateSD(tagRatiosOfDoc):
    mean=sum([value for value in tagRatiosOfDoc.values()])/len(tagRatiosOfDoc)
    sqrdMean=sum([math.pow(abs(tagRatiosOfDoc[key]-mean),2) for key in tagRatiosOfDoc.keys()])/len(tagRatiosOfDoc)
    sd=math.sqrt(sqrdMean)
    return (float(sd)/2)

# This Function is used to parse the html file for identifying contents from it.
def handleHtml(path_to_file,docType):
    htmlFile = open(path_to_file,"r")
    soup = BeautifulSoup(htmlFile,"html.parser")
    [s.extract() for s in soup('script')]
    [s.extract() for s in soup('style')]
    [s.extract() for s in soup('img')]
    pageTitle = ""
    textPresent=""
    htmlString =""
    try:
        if docType in htmlFileTypes:
            for body in soup.find_all('body'):
                textPresent+= body.getText()
                htmlString+= body.prettify()
            pageTitle = soup.title.string
        else:
            htmlString = soup.prettify()
    except:
        pass
    if(len(htmlString)==0):
        return ""
    tagLines = htmlString.split("\n")
    tagRatiosOfDoc={}
    i=0
    textData=[]
    for line in tagLines:
        parser = MyHTMLParser()
        parser.setVariables()
        parser.feed(line.strip())
        noOfTagChar=parser.getTagCount()
        noOfTextChar=parser.getTextCount()
        if(noOfTagChar==0):
            tagRatio=noOfTextChar
        else:
            tagRatio=(float(noOfTextChar)/float(noOfTagChar))
        tagRatiosOfDoc[i]=tagRatio
        if noOfTextChar > 0:
            textToAppend=BeautifulSoup(line,"html.parser").get_text().strip()
            textData.append(textToAppend)
        else:
            textData.append("");
        i+=1
    tagRatioSmooth = performSmoothing(tagRatiosOfDoc)
    threshold = calculateSD(tagRatioSmooth)
    outputNerBuffer=pageTitle
    for key,value in tagRatioSmooth.items():
        if value > threshold:
            outputNerBuffer+=" "+textData[key]
    return outputNerBuffer

# This function fetches all the NER Metadata associated with the text.
def formatMeta(parsedData,contentType,buffer):
    measure=[]
    metaDataFormatted={}
    metaDataFormatted["content"]=buffer
    measure=re.findall(r'\d+\.\d+[a-zA-Z]+|\d+\.\d+ [a-zA-Z]+',buffer)
    if(len(measure)>0):
        metaDataFormatted["Measurements"]=measure
    if "metadata" not in parsedData:
        return metaDataFormatted
    metaData=parsedData["metadata"]
    for key,value in metaData.items():
        if(re.match("NER",key)):
            metaDataFormatted[key]=value
        if "title"==key:
            metaDataFormatted[key]=value
    metaDataFormatted["Content-Type"]=contentType
    return metaDataFormatted

# Function uses regular expression for identifying measurement present in text.
"""
def getMeasure(buffer):
    measurements=re.findall(r'\d+[a-zA-Z]+|\d+\s{1,3}[a-zA-Z]+|\d+\.\d+[a-zA-Z]+|\d+\.\d+\s[a-zA-Z]+',buffer)
    return measurements
"""

# Main Processing.
measurementJson={}
for path,dirs,files in os.walk(path):
    for file in files:
        if file not in ".DS_Store":
            parsedData=""
            path_to_file = path+"/"+str(file)
            print path_to_file
            docType = detector.from_file(path_to_file)
            if docType in tagRatioFileTypes:
                buffer = handleHtml(path_to_file,docType)
            else:
                try:
                    buffer=subprocess.check_output(['java', '-jar', tikaSnapshotPath, '-t', path_to_file])
                except:
                    errorFile.write(path_to_file+"\n")
                    continue
            if (buffer==None):
                errorFile.write(path_to_file+"\n")
                continue
            if (len(buffer)==0):
                    errorFile.write(path_to_file+"\n")
                    continue

            parsedData=parser.from_buffer(buffer)
            metaData=formatMeta(parsedData,docType,buffer)
            measurementJson[path_to_file]=metaData

json.dump(measurementJson,measurementFile,indent=4)
measurementFile.close()
errorFile.close()
