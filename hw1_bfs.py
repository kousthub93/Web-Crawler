import requests
from bs4 import BeautifulSoup
import re
import time


# Goal: Write web crawling

# the below functions deletes duplicates and adds to the master list.
def deleteDuplicates(uniqueLinks,tempLinks,list_crawled,list_master):
 for a in tempLinks:
  if a not in uniqueLinks:
   if len(a) > 1:
    if a not in list_crawled:
     uniqueLinks.append(a)

# Add unique links to the masterlist
 for a in uniqueLinks:
  if a not in list_master:
   list_master.append(a)

 return uniqueLinks


# the below function crawls the given nextUrl
# Removes references and external links from the fetched Urls
# Also returns the master list only with the Urls containing 'Rain' and also Urls with the anchor tags 
# containing texts with the string 'rain'
def hitUrl(nextUrl,list_crawled,list_master):

 list_crawled.append(nextUrl)

 uniqueLinks = []
 tempLinks = []

 time.sleep(1)

 data = requests.get(nextUrl)

 data_text = data.text

 soup = BeautifulSoup(data_text,'html.parser')

 dataInFocus = soup.find('div',{'id': 'mw-content-text'})

 for link in dataInFocus.find_all('a', {'href': re.compile("^/wiki")}):
  if ':' not in link.get('href'):
   finalUrl = "https://en.wikipedia.org" + link.get('href')
   listWithoutHash = finalUrl.split('#')
   tempLinks.append(str(listWithoutHash[0]))
 
 return deleteDuplicates(uniqueLinks,tempLinks,list_crawled,list_master)
 
# The below one is a recursive function which traverses to different depths upto depth 6
def nextLinkToCrawl(listInUse, list_depth1, list_depth2, list_depth3, list_depth4, list_depth5, list_depth6,list_crawled):
	
	for a in listInUse:
		if a not in list_crawled:
			return a
	

	if 0 == cmp(listInUse,list_depth1):
		if len(list_depth1)<1000:
			return nextLinkToCrawl(list_depth2,list_depth1, list_depth2, list_depth3, list_depth4, list_depth5, list_depth6,list_crawled)
	if 0 == cmp(listInUse,list_depth2):
		if len(list_depth2)<1000:
			return nextLinkToCrawl(list_depth3,list_depth1, list_depth2, list_depth3, list_depth4, list_depth5, list_depth6,list_crawled)
	if 0 == cmp(listInUse,list_depth3):
		if len(list_depth3)<1000:
			return nextLinkToCrawl(list_depth4,list_depth1, list_depth2, list_depth3, list_depth4, list_depth5, list_depth6,list_crawled)
	if 0 == cmp(listInUse,list_depth4):
		if len(list_depth4)<1000:
			return nextLinkToCrawl(list_depth5,list_depth1, list_depth2, list_depth3, list_depth4, list_depth5, list_depth6,list_crawled)
	if 0 == cmp(listInUse,list_depth5):
		if len(list_depth5)<1000:
			return nextLinkToCrawl(list_depth6,list_depth1, list_depth2, list_depth3, list_depth4, list_depth5, list_depth6,list_crawled)

	return 'links not found'

# the below function checks whether nextPageUrl is part of which depth
def listBelongsTo(nextPageUrl,list_depth1,list_depth2,list_depth3,list_depth4,list_depth5,list_depth6):

	if nextPageUrl in list_depth1:
		return list_depth1

	elif nextPageUrl in list_depth2:
		return list_depth2

	elif nextPageUrl in list_depth3:
		return list_depth3

	elif nextPageUrl in list_depth4:
		return list_depth4

	else:
		return list_depth5


# main crawler implementing breadth for seacrh algorithm

def mainWebCrawler(url):
	
	list_master = []
	list_depth1 = []
	list_depth2 = []
	list_depth3 = []
	list_depth4 = []
	list_depth5 = []
	list_depth6 = []
	list_crawled = []
	

	list_master.append(url)
	list_depth1.append(url)

	while len(list_master) < 1000:

		nextPageUrl = nextLinkToCrawl(list_depth1,list_depth1,list_depth2,list_depth3,list_depth4,list_depth5,list_depth6,list_crawled)
		if nextPageUrl == 'links not found':
			print "crawling ends:no further links found"
			break
		
		else:
			
			listx = listBelongsTo(nextPageUrl,list_depth1,list_depth2,list_depth3,list_depth4,list_depth5,list_depth6)

			if listx == list_depth1:
				list_depth1_urls = hitUrl(nextPageUrl,list_crawled,list_master)
				for a in list_depth1_urls:
					list_depth2.append(a)
			elif listx == list_depth2:
				list_depth2_urls = hitUrl(nextPageUrl,list_crawled,list_master)
				for b in list_depth2_urls:
					if (b not in list_depth1) and (b not in list_depth2):
						list_depth3.append(b)
			elif listx == list_depth3:
				list_depth3_urls = hitUrl(nextPageUrl,list_crawled,list_master)
				for c in list_depth3_urls:
					if (c not in list_depth2) and (b not in list_depth3):
						list_depth4.append(c)

			elif listx == list_depth4:
				list_depth4_urls = hitUrl(nextPageUrl,list_crawled,list_master)
				for d in list_depth4_urls:
					if (d not in list_depth3) and (d not in list_depth4):
						list_depth5.append(d)

			elif listx == list_depth5:
				list_depth5_urls = hitUrl(nextPageUrl,list_crawled,list_master)
				for e in list_depth5_urls:
					if (e not in list_depth4) and (e not in list_depth5):
						list_depth6.append(e)

# open a file to write the fetched URLS
	file = open('TASK 1-E.txt', 'w')
	
	for i,url in enumerate(list_master):
		if i < 1000:
		 file.write(str(url.lower()) + "\n")

	file.close()

url = "https://en.wikipedia.org/wiki/Tropical_cyclone"
mainWebCrawler(url)