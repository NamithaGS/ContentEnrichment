
import json
import string
import re
stopwords=[u'', u'A', u'ABOUT', u'ABOVE', u'AFTER', u'AGAIN', u'AGAINST', u'ALL', u'AM', u'AN', u'AND', u'ANY', u'ARE', u"AREN'T", u'AS', u'AT', u'BE', u'BECAUSE', u'BEEN', u'BEFORE', u'BEING', u'BELOW', u'BETWEEN', u'BOTH', u'BUT', u'BY', u"CAN'T", u'CANNOT', u'COULD', u"COULDN'T", u'DID', u"DIDN'T", u'DO', u'DOES', u"DOESN'T", u'DOING', u"DON'T", u'DOWN', u'DURING', u'EACH', u'FEW', u'FOR', u'FROM', u'FURTHER', u'HAD', u"HADN'T", u'HAS', u"HASN'T", u'HAVE', u"HAVEN'T", u'HAVING', u'HE', u"HE'D", u"HE'LL", u"HE'S", u'HER', u'HERE', u"HERE'S", u'HERS', u'HERSELF', u'HIM', u'HIMSELF', u'HIS', u'HOW', u"HOW'S", u'I', u"I'D", u"I'LL", u"I'M", u"I'VE", u'IF', u'IN', u'INTO', u'IS', u"ISN'T", u'IT', u"IT'S", u'ITS', u'ITSELF', u"LET'S", u'ME', u'MORE', u'MOST', u"MUSTN'T", u'MY', u'MYSELF', u'NO', u'NOR', u'NOT', u'OF', u'OFF', u'ON', u'ONCE', u'ONLY', u'OR', u'OTHER', u'OUGHT', u'OUR', u'OURS\tOURSELVES', u'OUT', u'OVER', u'OWN', u'SAME', u"SHAN'T", u'SHE', u"SHE'D", u"SHE'LL", u"SHE'S", u'SHOULD', u"SHOULDN'T", u'SO', u'SOME', u'SUCH', u'THAN', u'THAT', u"THAT'S", u'THE', u'THEIR', u'THEIRS', u'THEM', u'THEMSELVES', u'THEN', u'THERE', u"THERE'S", u'THESE', u'THEY', u"THEY'D", u"THEY'LL", u"THEY'RE", u"THEY'VE", u'THIS', u'THOSE', u'THROUGH', u'TO', u'TOO', u'UNDER', u'UNTIL', u'UP', u'VERY', u'WAS', u"WASN'T", u'WE', u"WE'D", u"WE'LL", u"WE'RE", u"WE'VE", u'WERE', u"WEREN'T", u'WHAT', u"WHAT'S", u'WHEN', u"WHEN'S", u'WHERE', u"WHERE'S", u'WHICH', u'WHILE', u'WHO', u"WHO'S", u'WHOM', u'WHY', u"WHY'S", u'WITH', u"WON'T", u'WOULD', u"WOULDN'T", u'YOU', u"YOU'D", u"YOU'LL", u"YOU'RE", u"YOU'VE", u'YOUR', u'YOURS', u'YOURSELF', u'YOURSELVES']
#freqListFile = open("/Users/charanshampur/solr/lucene_solr_4_10/solr/example/solr-webapp/webapp/MyHtml/freqList.json","w")
freqListFile = open("freqList.json","w")
inputJsonFile = open("/Users/charanshampur/Sites/MyHtml/circle.json","r")
removeWords=["FOR","LOGIN","SALE","NEW","FREE","``","BUY","SYSTEM","WANT","REPORT","WITHIN","S","...","TO","SAN","P","W/","ALL","'S","W","M","PAGE","ITEMS"]
jsonStr=inputJsonFile.readline()
#print "NLTK succesfully loaded<br>"
jsonLoad = json.loads(jsonStr)
#print "Json succesfully loaded"
wordCloud={}
for item in jsonLoad:
    if "title" in item:
        if type(item["title"]) is list:
            text = item["title"][0]
        else:
            text = item["title"]
        text = re.sub(r"[(}{)|\\/><\[\],.;:@#?!&$_-]+", ' ', text)
        try:
            tokens=(str(text).split())
        except:
            continue
        tokens=[w for w in tokens if w not in string.punctuation]
        for token in tokens:
            if token.upper() not in removeWords and not token.isdigit() and token.upper() not in stopwords:
                if token.upper() not in wordCloud:
                    wordCloud[token.upper()]=1
                else:
                    wordCloud[token.upper()]+=1

wordCloud=sorted(wordCloud.items(), key=lambda x: x[1],reverse=True)
wordJson=[]
wordDict={}
for i in range(0,120):
    wordDict["text"]=wordCloud[i][0]
    if int(wordCloud[i][1])>80:
        normalizedSize=80
    else:
        normalizedSize=wordCloud[i][1]
    wordDict["size"]=normalizedSize
    wordJson.append(dict(wordDict))

jsonarray = json.dumps(wordJson,indent=4)
freqListFile.write(jsonarray)
freqListFile.close()
print "success"