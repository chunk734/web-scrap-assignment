import requests
import os
from bs4 import BeautifulSoup
from validator_collection import validators
import datetime
import argparse
import json

directory = "fetch"
metadata = "metadata"

class fetch:
    def __init__(self, url) -> None:
        self.url = url
        self.webPage = ""
        self.linksCount = 0
        self.imagesCount = 0
        self.metaData = {"metadata": []}
    
    def validateURL(self):
        try:
            validators.url(self.url)
        except Exception as error:
            print("\n\""+ self.url + "\" is not a valid url\n") 
            return 1 
    
    def loadMetadata(self):
        self.load(fetch, metadata)

    def getCurrentUTCTimestamp(self):
        utc_time = datetime.datetime.utcnow()
        return utc_time.strftime('%Y-%m-%d %H:%M:%S')

    def addMetadata(self):
        flag = 0
        url = self.url.split("://")[1]
        for i in range(len(self.metaData["metadata"])):
            if url in self.metaData["metadata"][i]:
                flag = 1
                self.metaData["metadata"][i][url]["last_updated_time"] = self.getCurrentUTCTimestamp()
                self.metaData["metadata"][i][url]["num_links"] = self.linksCount
                self.metaData["metadata"][i][url]["num_images"] = self.imagesCount
                break
        if flag == 0:
            self.metaData["metadata"].append({url:{"last_updated_time":self.getCurrentUTCTimestamp(), "num_links":self.linksCount, "num_images": self.imagesCount}})
    
    def saveMetadata(self):
        instance_metadata = saveToDisk("metadata")
        instance_metadata.save(self.metaData)

    def getMetadata(self):
        flag = 0
        self.loadMetadata()
        url = self.url.split("://")[1]
        for i in range(len(self.metaData["metadata"])):
            if url in self.metaData["metadata"][i]:
                flag = 1
                print("****************************************************")
                print("site: "+ url)
                print("num_links: " + str(self.metaData["metadata"][i][url]["num_links"]))
                print("images: " + str(self.metaData["metadata"][i][url]["num_images"]))
                print("last_fetch: " + str(self.metaData["metadata"][i][url]["last_updated_time"]) + " UTC")
                print("****************************************************")
        if flag == 0:
            print("\nWebPage \"" + url +"\" currently not present. Try downloading the page first.\n")

    def getWebpage(self):
        if self.validateURL():
            return
        try:
            self.webPage = requests.get(self.url)
        except Exception as error:
            print("\nWebpage \""+self.url+"\" download failed")
            #print("\nExecption while fetching the webpage: "+ error)
            return
        soup = BeautifulSoup(self.webPage.content, "html.parser")
        if self.webPage.status_code != 200:
                print("\nWebpage \""+self.url+"\" download failed")
                print("\nStatus Code for \""+ self.url+"\": "+ str(self.webPage.status_code))
                print(soup.prettify())
                return
        self.findLinksCount()
        self.findImagesCount()
        self.saveWebPage(soup.prettify())
        self.loadMetadata()
        self.addMetadata()
        self.saveMetadata()

    def saveWebPage(self, page):
        instance_save = saveToDisk(self.url.split("://")[1])
        instance_save.save(page)
        print("\nWebpage \""+ self.url +"\" downloaded successfully\n")

    def load(self, path, name):
        cwd = os.getcwd()
        
        path = os.path.join(cwd, directory)
        try:
            with open(path+"/"+name,'r') as fp:
                self.metaData = json.load(fp)
        except Exception as e:
            pass
        
    def findLinksCount(self):
        soup = BeautifulSoup(self.webPage.content, "html.parser")
        self.linksCount = len(soup.findAll('a'))
    
    def findImagesCount(self):
        soup = BeautifulSoup(self.webPage.content, "html.parser")
        self.imagesCount = len(soup.findAll('img'))

class saveToDisk:
    def __init__(self, filename) -> None:
        self.filename = filename

    def save(self, content):
        cwd = os.getcwd()
        
        path = os.path.join(cwd, directory)
        try: 
            os.mkdir(path) 
        except OSError as error: 
            pass
        with open(path+"/"+self.filename,'w') as fp:
            if self.filename == "metadata":
                json.dump(content, fp)
            else:
                fp.write(content)

def main():
    parser = argparse.ArgumentParser(description ='.')
  
    # Adding Arguments
    parser.add_argument('-o','--operation', type = str, help ='Operation Type (download/metadata)')
    parser.add_argument('-u','--urls', type = str, nargs ='+', help ='Urls for the Webpages')
    
    args = parser.parse_args()

    if args.operation == "download":
        for url in args.urls:
            instance_fetch = fetch(url)
            instance_fetch.getWebpage()  
    elif args.operation == "metadata":
        for url in args.urls:
            instance_fetch = fetch(url)
            instance_fetch.getMetadata()
    else:
        print("\n----------Invalid operation----------\n")

if __name__=="__main__":
    main()
