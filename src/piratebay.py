#! /usr/bin/python
from pprint import pprint
import unicodedata

import requests
from bs4 import BeautifulSoup

def get_json(soup):
    table = soup.table
    tables = table.find_all("td")

    json_obj = {
        "movie_info":[]
    }
    seeders = []
    movie_sizes = []

    for el in table.find_all("td"):
        if el.font:
            size = el.font.text.split(",")[1][6:]
            movie_sizes.append(size)

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

    for i , _ in enumerate(json_obj["movie_info"]):
        json_obj["movie_info"][i]["size"] = unicodedata.normalize("NFKD" ,  movie_sizes[i])

    return json_obj

def pirate(query = None):
    if not query:
        url = "https://tpb.party/top/200"
    else:
        url = f"https://tpb.party/search/{query}"
    print(url)
    res = requests.get(url)
    if res.status_code != 200:
        raise ValueError("Ops didn't get valid response")
    content = res.content
    soup = BeautifulSoup(content , "html.parser")
    obj = get_json(soup)
    return obj
