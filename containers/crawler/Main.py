from webmap import Crawler

if __name__ == "__main__":
    URL = "https://scrapeme.live/shop/"
    webMapperObject = Crawler(URL)
    webMapperObject.run()