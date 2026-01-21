from webmap import Crawler

URL = "https://scrapeme.live/shop/"

if __name__ == "__main__":
    webMapperObject: Crawler = Crawler(URL)
    webMapperObject.run()