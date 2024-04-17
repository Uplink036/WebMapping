from scrapper import getHTMLResponse, getSoup, printParsedHTML, getAllLinks


def main():
    URL = "https://scrapeme.live/shop/"
    html_response = getHTMLResponse(URL)
    printParsedHTML(html_response.content)
    soup = getSoup(html_response)
    links = getAllLinks(soup)
    print(links)
    website_count = {}
    for link in links:
        if link in website_count:
            website_count[link] += 1
        else:
            website_count[link] = 1

if __name__ == "__main__":
    main()