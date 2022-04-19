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
        """
        Function for the GET call on the url.
       
        Returns:
        int: Status code for the url (valid/invalid)
  
        """
        try:
            validators.url(self.url)
        except Exception as error:
            print("\n\""+ self.url + "\" is not a valid url\n") 
            return 1 
    
    def loadMetadata(self):
        self.load(fetch, metadata)

    def getCurrentUTCTimestamp(self):
        """
        Get current timestamp in UTC format.
        
        Returns:
        str: Formatted UTC timestamp
  
        """
        utc_time = datetime.datetime.utcnow()
        return utc_time.strftime('%Y-%m-%d %H:%M:%S')

    def addMetadata(self):
        """
        Update/Add metadata of the downloaded url to the json file .
 
        """
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
        """
        Get metadata of the downloaded url from the json file and dup to stdout .
  
        """
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
        """
        Validate the provided url, make a GET request for the same and store it in a file.
  
        """       
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
        """
        Load the metadata json file .
  
        """
        cwd = os.getcwd()
        
        path = os.path.join(cwd, directory)
        try:
            with open(path+"/"+name,'r') as fp:
                self.metaData = json.load(fp)
        except Exception as e:
            pass
        
    def findLinksCount(self):
        """
        Get links count from the webpage.
  
        """
        soup = BeautifulSoup(self.webPage.content, "html.parser")
        self.linksCount = len(soup.findAll('a'))
    
    def findImagesCount(self):
        """
        Get images count from the webpage.
  
        """
        soup = BeautifulSoup(self.webPage.content, "html.parser")
        self.imagesCount = len(soup.findAll('img'))


class saveToDisk:
    def __init__(self, filename) -> None:
        self.filename = filename

    def save(self, content):
        """
        Save data to a file.
  
        """
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
    """
    Driver code for the script.
  
    Instantiates the "fetch" class for every url in the list passed as argument from the CLI.
  
    """
    parser = argparse.ArgumentParser(description ='.')  
    # Adding flags "--operation" and "--urls" for the CLI
    parser.add_argument('-o','--operation', type = str, help ='Operation Type (download/metadata)')
    parser.add_argument('-u','--urls', type = str, nargs ='+', help ='Urls for the Webpages')
    
    args = parser.parse_args()
    
    # If operation is "download", then fetch the latest web-page
    # If operation is "metadata", then fetch the latest metadata info for the last successful download
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
