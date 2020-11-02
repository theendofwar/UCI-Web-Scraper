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
        infile = open("report.txt","w")

        #write the unqiue page
        infile.write("The unique link crawl by crawler")
        for link in self.uniqueUrl:
            infile.write(f"{link}\n")

        #write out the longest page
        infile.write(f"The longest page find in{self.longestPage['url']} and the number of words is {self.longestPage['num']}\n")

        #write out the 50 common word 
        infile.write("50 common word are:")
        commonword = sorted(self.commonWord.items(),key=lambda x: x[1],reverse=True)
        for key,value in commonword[:51]:
            infile.write(f"{key} --> {value}\n")

        #write out the domain in ics.uci.edu
        infile.write("list of subdomain in ics.uci.edu are:")
        subdomain = sorted(self.commonWord.items(),key=lambda x: x[0][7:],reverse=True)
        for key,value in subdomain:
            infile.write(f"{key} --> {value}\n")
