import re
from urllib.parse import urlparse
from database import Database
from ExecuteTokenizer import Tokenizer
from bs4 import BeautifulSoup
from utils.robotTXT import getRobot


database = Database()
tokenizer = Tokenizer()
robotTXT = getRobot()

def scraper(url, resp):
    url = url.split('#')[0]
    if resp.raw_response == None:
        return list()
    if resp.status == 200:
        if tokenizer.executeTokenize(database,url,resp):
            links = extract_next_links(url, resp)
            return [link for link in links if is_valid(link)]
        return list()
    elif resp.status >= 400 and resp.status <=599:
        database.addInvalidUrl(url)
        return list()
    elif resp.status >= 600:
        database.addInvalidUrl(url)
        return list()
    return list()

def extract_next_links(url, resp):
    output = []
    soup = BeautifulSoup(resp.raw_response.content, features = "lxml")
    for link in soup.find_all("a"):
        if link.get("href") != None:
            if "/pdf/" and ".zip" and ".odc" not in link.get("href"):
                output.append(link.get("href").split("#")[0])
    return output

# TODO: implement the is_valid function 
def is_valid(url):
    try:
        parsed = urlparse(url)
        count = 0
        specUrl = ""
        for i in ["ics.uci.edu","cs.uci.edu","informatics.uci.edu",
                                     "stat.uci.edu","today.uci.edu/department/information_computer_sciences"]:
            if i in parsed.netloc:
                count += 1
                specUrl = i
        if count != 0:
            url = parsed.geturl()
            calender = parsed.geturl().rfind("/calender/")
            if calender != -1 and specUrl == "today.uci.edu/department/information_computer_sciences":
                database.robotTXT+=1
                return False
            for disallow in robotTXT[specUrl]["Disallow"]:
                if disallow in url:
                    cont = 0
                    for allow in robotTXT[specUrl]["Allow"]:
                        if allow in url:
                            cont+=1
                    if cont == 0:
                        database.robotTXT+=1
                        return False
            if "reply" and "wics.ics.uci.edu" in parsed.geturl():
                return False
            elif "pdf" in parsed.geturl():
                return False
            elif "zip" in parsed.geturl():
                return False
            elif "ppsx" in parsed.geturl():
                return False
            elif "CollabCom" in parsed.geturl():
                return False
            elif "ps.Z" in parsed.geturl():
                return False
            elif "MjolsnessCunhaPMAV24Oct2012" in parsed.geturl():
                return False
            elif "calender" and "date" not in parsed.geturl():
                    if "?replytocom" not in parsed.geturl():
                        return not re.match(
                            r".*\.(css|js|bmp|gif|jpe?g|ico"
                            + r"|png|tiff?|mid|mp2|mp3|mp4"
                            + r"|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf"
                            + r"|ps|eps|tex|ppt|pptx|doc|docx|xls|xlsx|names|ppsx"
                            + r"|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso"
                            + r"|epub|dll|cnf|tgz|sha1"
                            + r"|thmx|mso|arff|rtf|jar|csv"
                            + r"|rm|smil|wmv|swf|wma|zip|rar|gz|odc|ps.Z|.r|replytocom)$", parsed.path.lower())
                    else:
                        return False
        else:
            return False
    except TypeError:
        print ("TypeError for ", parsed)
        raise

    except TypeError:
        print ("TypeError for ", parsed)
        raise


