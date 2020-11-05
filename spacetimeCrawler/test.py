import re

def sortfunction(url:str):
        match = re.search(r"http[s]?:\/\/(www.)?(.+)",url[0])
        return match.group(2).lower()

subDomain = {"http://xtune.ics.uci":2,"http://psearch.ics.uci.edu":3,"https://emj.ics.uci.edu":6,"https://aiclub.ics.uci.edu":7}

subdomain = sorted(subDomain.items(),key=sortfunction)
print(subdomain)