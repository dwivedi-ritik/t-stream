import requests
from pprint import pprint
from bs4 import BeautifulSoup

def get_json(soup):
    table = soup.table
    tables = table.find_all("td")

    json_obj = {
        "movie_info":[]
    }
    seeders = []
    for el in table.find_all("td"):
        if el.div and el.div.a:
            json_obj["movie_info"].append({
                "title": el.div.text.strip("\n"),
                "magnet_url": el.find_all("a")[1]["href"]
            })
        if el.get("align"):
            seeders.append(el.text)

    k = 0
    for i in range(0 , len(seeders) , 2): 
        json_obj["movie_info"][k]["seeders"] = seeders[i]
        json_obj["movie_info"][k]["leeches"] = seeders[i+1]
        k += 1
    return json_obj

def pirate(query , top = False):
    if top and query is None:
        url = "https://tpb.party/top/200"
    else:
        url = f"https://tpb.party/search/{query}"
    res = requests.get(url)
    if res.status_code != 200:
        raise ValueError("Ops didn't get valid response")
    content = res.content
    soup = BeautifulSoup(content , "html.parser")
    obj = get_json(soup)
    return obj
