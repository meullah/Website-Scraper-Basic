from Scraper import Scraper

if __name__ == '__main__':
    website = Scraper("https://www.google.com")
    website.scrapeAllChildURLs()


