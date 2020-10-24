import logging
from datamodel.search.WenhankXimanw_datamodel import WenhankXimanwLink, OneWenhankXimanwUnProcessedLink, \
    add_server_copy, get_downloaded_content
from spacetime.client.IApplication import IApplication
from spacetime.client.declarations import Producer, GetterSetter, Getter, ServerTriggers
from lxml import html, etree
import re, os
from time import time
from uuid import uuid4
import requests
from urlparse import urlparse, parse_qs, urljoin
from bs4 import BeautifulSoup
import StringIO

logger = logging.getLogger(__name__)
LOG_HEADER = "[CRAWLER]"

subdomains = {}
mostOutLinksPage = ['None', 0]
outPutLinksLength = 0

@Producer(WenhankXimanwLink)
@GetterSetter(OneWenhankXimanwUnProcessedLink)
@ServerTriggers(add_server_copy, get_downloaded_content)
class CrawlerFrame(IApplication):
    def __init__(self, frame):
        self.starttime = time()
        self.app_id = "WenhankXimanw"
        self.frame = frame

    def initialize(self):
        self.count = 0
        l = WenhankXimanwLink("http://www.ics.uci.edu/")
        print l.full_url
        self.frame.add(l)

    def update(self):
        unprocessed_links = self.frame.get(OneWenhankXimanwUnProcessedLink)
        if unprocessed_links:
            link = unprocessed_links[0]
            print "Got a link to download:", link.full_url
            downloaded = link.download()
            links = extract_next_links(downloaded)
            for l in links:
                if is_valid(l):
                    self.frame.add(WenhankXimanwLink(l))

    def shutdown(self):
        print (
            "Time time spent this session: ",
            time() - self.starttime, " seconds.")




def write_analysis():
    analysis = open('analysis.txt', 'w')
    analysis.write('Subdomains: ' + str(subdomains))
    analysis.write('\n')
    analysis.write('Most out link pages: ' + str(mostOutLinksPage))


def extract_next_links(rawDataObj):
    outputLinks = []
    global subdomains
    global mostOutLinksPage
    '''
    rawDataObj is an object of type UrlResponse declared at L20-30
    datamodel/search/server_datamodel.py
    the return of this function should be a list of urls in their absolute form
    Validation of link via is_valid function is done later (see line 42).
    It is not required to remove duplicates that have already been downloaded.
    The frontier takes care of that.

    Suggested library: lxml
    '''
    if rawDataObj.error_message is not None:
        print 'Error: ', rawDataObj.error_message

    url = rawDataObj.url
    if rawDataObj.is_redirected:
        url = rawDataObj.final_url

    soup = BeautifulSoup(rawDataObj.content, 'lxml')
    links = soup.find_all('a')
    linkCount = 0
    for link in links:
        try:
            if 'href' in link.attrs:
                newurl = link.attrs['href']
                parsedLink = urlparse(newurl)
                # check subdomains for all newurl.
                if parsedLink.scheme == 'http' and 'ics.uci.edu' in parsedLink.netloc:
                    if parsedLink.netloc not in subdomains:
                        subdomains[parsedLink.netloc] = 1
                    else:
                        subdomains[parsedLink.netloc] += 1
                if newurl.startswith('#'):
                    break
                # solve for relative url
                if newurl.startswith('/'):
                    newurl = urljoin(url, newurl)
                    linkCount += 1
                # dont craw url without scheme
                if newurl.startswith('http'):
                    outputLinks.append(newurl)
                    linkCount += 1
        except:
            pass

    # update most out link page collection
    print len(outputLinks), 'compare to ', mostOutLinksPage[1]
    if len(outputLinks) > mostOutLinksPage[1]:
        print 'most link updated'
        mostOutLinksPage[0] = rawDataObj.url
        mostOutLinksPage[1] = len(outputLinks)

    write_analysis()
    return outputLinks


#     if rawDataObj.error_message:
#         print 'NetError: ' + rawDataObj.error_message
#
#     print '\nthe url for current rawdataobj is ' + rawDataObj.url + '\n'
#     try:
#         url = rawDataObj.url
#         if rawDataObj.is_redirected:
#             url = rawDataObj.final_url
#
#         soup = BeautifulSoup(rawDataObj.content, 'lxml')
#         links = soup.find_all('a')
# #        print links
#         for l in links:
#             link = l['href']
#             parsedLink = urlparse(link)
#             print parsedLink
#             if parsedLink.scheme not in {'http', 'https'}:
#                 print 'this should be a relativelink' + parsedLink
#                 base = urlparse(rawDataObj.url).netloc
#
#                 print 'the base is ' + base
#                 if link[0] == '/':
#                     link = link[1:]
#                 print 'the relative link is ' + link
#                 absoluteLink = urljoin(base, link)
#                 print 'the absolute link after join is ' + absoluteLink + '\n'
#                 outputLinks.append(absoluteLink)
#             else:
#                 print 'the link being crawled is ' + link
#                 outputLinks.append(link)
#
#
#     except:
#         pass
#     print 'the links number found on this page is: ' + str(len(outputLinks)) + '\n'
#     return outputLinks

# if rawDataObj.error_message:
#     print 'NetError: ', rawDataObj.error_message
#
# try:
#     url = rawDataObj.url
#     if rawDataObj.is_redirected:
#         url = rawDataObj.final_url
#
#     soup = BeautifulSoup(rawDataObj, "lxml")
#
#     for link in soup.find_all('a', href=True):
#         interlink = link['href']
#         parsed = urlparse(interlink)
#         if parsed.scheme not in set(['http', 'https']):
#             absolte_link = urljoin(url, interlink)
#             if interlink.startwith('http') or interlink.startwith('https'):
#                 outputLinks.append(absolte_link)
#         else:
#             outputLinks.append(interlink)
# except:
#     pass
# return outputLinks


def is_valid(url):
    '''
    Function returns True or False based on whether the url has to be
    downloaded or not.
    Robot rules and duplication rules are checked separately.
    This is a great place to filter out crawler traps.
    python2.7 applications/search/crawler.py -a amazon.ics.uci.edu -p 9100
    python2.7 applications/search/check_frontier.py -a amazon.ics.uci.edu -p 9100
    python2.7 applications/search/reset_frontier.py -a amazon.ics.uci.edu -p 9100
    '''
    parsed = urlparse(url)
    if parsed.scheme not in set(["http", "https"]):
        return False

    bad_subdomains = ['graphmod', 'grape', 'ganglia', 'abrc']

    try:
        # ingore calendar traps in calendar.ics.uci.edu
        if "calendar" in parsed.hostname:
            return False
        # ingore links if the server is down
        elif requests.get(url).status_code != requests.codes.ok:
            return False
        # ignore broken links that mixed with tag <a></a>
        elif '<a>' in parsed.query or '</a>' in parsed.query:
            return False;
        # ignore bad parameters replytocom
        elif 'replytocom' in parsed.query:
            return False
        # ignore long long url
        elif len(url) > 200:
            return False
        # ignore ~ihler in path, stuck in infinite loop
        elif '~ihler' in parsed.path:
            return False
        # ignore ~dechter in path, stuck in infinite loop
        elif '~dechter' in parsed.path:
            return False
        # dont know why pubs always return 500 internal error or stays in loop
        elif 'pubs' in parsed.path:
            return False
        # error 503 for http://www.ics.uci.edu/about/equity
        elif 'about/equity' in parsed.path:
            return False
        # ignore url with parameters view_news e.g.http://www.ics.uci.edu/community/news/view_news?id=1263
        elif 'view_news.php' in parsed.netloc:
            return False
        # ignore url in bad subdomains
        for sub in bad_subdomains:
            if sub in parsed.hostname:
                return False
    except:
        pass
    try:
        return ".ics.uci.edu" in parsed.hostname \
               and not re.match(".*\.(css|js|bmp|gif|jpe?g|ico" + "|png|tiff?|mid|mp2|mp3|mp4" \
                                + "|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf" \
                                + "|ps|eps|tex|ppt|pptx|doc|docx|xls|xlsx|names|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso|epub|dll|cnf|tgz|sha1" \
                                + "|thmx|mso|arff|rtf|jar|csv" \
                                + "|rm|smil|wmv|swf|wma|zip|rar|gz)$", parsed.path.lower())

    except TypeError:
        print ("TypeError for ", parsed)
        return False
