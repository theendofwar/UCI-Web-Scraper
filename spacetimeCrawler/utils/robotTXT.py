import requests
from bs4 import BeautifulSoup
import re
from collections import defaultdict

def getRobot():
    robotTXT = dict()
    urlList = ["https://today.uci.edu/robots.txt","https://www.informatics.uci.edu/robots.txt","https://www.stat.uci.edu/robots.txt","https://www.cs.uci.edu/robots.txt","https://www.ics.uci.edu/robots.txt"]
    for url in urlList:
        resp = requests.get(url)
        if resp.status_code == 200:
            if url == "https://today.uci.edu/robots.txt":
                url = "today.uci.edu/department/information_computer_sciences"
            elif url == "https://www.informatics.uci.edu/robots.txt":
                url = "informatics.uci.edu"
            elif url == "https://www.stat.uci.edu/robots.txt":
                url = "stat.uci.edu"
            elif url == "https://www.cs.uci.edu/robots.txt":
                url = "cs.uci.edu"
            elif url == "https://www.ics.uci.edu/robots.txt":
                url = "ics.uci.edu"
            soup = BeautifulSoup(resp.content, features = "lxml")
            all_text = soup.get_text()
            allow = re.findall(r"Allow: \/.+",all_text)
            disallow = re.findall(r"Disallow: \/.+",all_text)
            robotTXT[url] = defaultdict(set)
            for word in allow:
                robotTXT[url]["Allow"].add(word.split(" ")[1])
            for word in disallow:
                robotTXT[url]["Disallow"].add(word.split(" ")[1])
    return robotTXT

