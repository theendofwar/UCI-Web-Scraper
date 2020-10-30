from collections import defaultdict
import nltk

class Database():
    def __init__(self):
        # uniqueUrl store all the uniqueUrl into a set
        self.uniqueUrl = set()
        #invalidUrl store all the invalidUrl into a set
        self.invalidUrl =set()
        # longestPage keep track of the longestPage
        self.longestPage = {"url":"a url","num":0}
        # commonWord store all the common word the crawler parse
        self.commonWord = defaultdict(int)
        # subDomain store all the number of subdomain ics.uci.edu has
        self.subDomain = defaultdict(int)

    # add the uniqueUrl to the database
    def addUniqueUrl(self,url:str)->None:
        self.uniqueUrl.add(url)

    #update longest page in the database
    def updateLongestpage(self,url:str, wordnum:int):
        if wordnum>self.longestPage[1]:
            self.longestPage["url"] = url
            self.longestPage["num"] = wordnum

    #update commonword into database
    def updateCommonword(self,word:str)->None:
        self.commonWord[word]+=1

    #update number of subdomain into database
    def updateSubDomain(self,url:str):
        self.subDomain[url]+=1
    #update invalidUrl to the database
    def addInvalidUrl(self,url:str):
        self.invalidUrl.add(url)
    #automaticly write the report after the crawler finish all the work
    def writeReport(self):
        pass