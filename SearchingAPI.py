import requests
import WebScrapper

def searchArticle(query):
    listOfContents = []
    api_key = '3db5520cbbdda6695022b40c7ad0c2f3c2bda6edbb3a1b7a6a7f4ab199125eda'
    url = "https://serpapi.com/search"

    params = {
        "q":  query,
        "api_key": api_key,
        "engine": "google",
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        search_results = response.json()

        if "organic_results" in search_results:
            for result in search_results["organic_results"]:
                title = result["title"]
                url = result["link"]
                listOfContents.append(WebScrapper.web_scrapper(url))
                snippet = result["snippet"]
                print(f"Title: {title}")
                print(f"URL: {url}")
                print(f"Description: {snippet}")
                print("-" * 50)
    else:
        print(f"Error: {response.status_code}, {response.text}")

    return listOfContents