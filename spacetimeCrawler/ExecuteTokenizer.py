import nltk
from nltk.corpus import stopwords 
from simhash import Simhash
from bs4 import BeautifulSoup
from database import Database
from urllib.parse import urlparse

class Tokenizer():
    # set of stop words from nltk
    _StopWord = set(stopwords.words('English'))

    def __init__(self):
        # TODO: find a better way to detact duplicate
        self.simHash = dict()

    #execute the process of tokenize, parsing through webpage and store data in database, assum the resp is not empty
    def executeTokenize(self,database:Database,url:str,resp)->bool:
        # check if the this url is in the database or not
        if url in database.uniqueUrl or url in database.invalidUrl:
            return False
        return self.tokenize(database,url,resp)

    # a helper method to execute tokenize 
    def tokenize(self,database,url:str,resp)->bool:
        # beautifulsoup will parse all the html
        soup = BeautifulSoup(resp.raw_response.content, features = "lxml")
        # get text return all the text in this page
        all_text = soup.get_text()
        if all_text != "":
            if Simhash(all_text).value in self.simHash.keys():
                return False
            self.simHash[Simhash(all_text).value] = 1
            database.addUniqueUrl(url)
            words = nltk.word_tokenize(all_text)
            # count the total word in this page
            wordcount = 0
            for word in words:
                if word.isalnum() and word not in Tokenizer._StopWord:
                    wordcount += 1
                    database.updateCommonword(word)
            database.updateLongestpage(url,wordcount)
            # update the number of subdomain in database
            if "ics.uci.edu" in url:
                database.updateSubDomain(urlparse(url)[0] + "://" + urlparse(url)[1])
        return True
    