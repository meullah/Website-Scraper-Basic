import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urlsplit
from urlvalidator import validate_url, validate_email, ValidationError


class Scraper:
    """
    Class for scraping parent and its child websites to single depth
    """

    def __init__(self, url):
        _ = urlsplit(url)
        self.BASE_URL = _.scheme + '://' + _.netloc
        try:
            response = requests.get(url)
        except requests.ConnectionError as exception:
            print("URL does not exist on Internet")
        else:
            self.soup = BeautifulSoup(response.content, 'html.parser')
            self.writeToFile(data=self.soup)

    def getAvailableURLs(self):
        """
        :return: child_urls
        :type:List
        """
        child_urls = []
        for link in self.soup.find_all('a'):
            url = str(link.get('href'))
            if "http" in url:
                child_urls.append(url)
            elif url.find('/') == 0:
                child_urls.append(self.BASE_URL + url)
        return child_urls

    def writeToFile(self, data):
        """
        Writes scraped data to file
        :param data:
        :return:
        """
        # todo Add Try Catch | Exception Handling

        filename = re.sub('\W+', ' ', data.title.string) + '.html'
        with open(filename, 'w', encoding="utf-8")as file:
            file.write(str(data))

    def scrapeAllChildURLs(self):
        """
        Scrapes all the available links on the page and write their HTML in a file
        :return: None
        """
        for _url in self.getAvailableURLs():
            print("Scrapping :  " + _url)
            self.getScrapedData(_url)

    def getScrapedData(self, uri):
        """
        Given a URL it scraps all the HTML data and write into a file
        :param uri:
        :type uri:str
        :return:
        """
        try:
            response = requests.get(uri)
        except requests.ConnectionError as exception:
            print("URL does not exist on Internet")
        else:
            new_soup = BeautifulSoup(response.content, 'html.parser')
            self.writeToFile(data=new_soup)
