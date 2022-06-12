#! /usr/bin/python
import sys
import subprocess
import json
import os
from pathlib import Path

from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt
from piratebay import *
from spinner import Spinner , add_cursor


def write_table(movie_list):
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("ID", width=12)
    table.add_column("Title")
    table.add_column("Size", justify="right")
    table.add_column("Seeders", justify="right")
    table.add_column("Leeches", justify="right")

    for i , obj in enumerate( movie_list ):
        table.add_row(str(i+1) , obj["title"] , str(obj["size"]),str(obj["seeders"]) , str(obj["leeches"]))

    console.print(table)
    return

def greet_bye():
    print("\nsee ya 👋")


def parse_config():
    app_dir = "/".join(os.path.realpath(__file__).split("/")[:-2])
    config_path = os.path.join(app_dir , "config.json")

    default_value = ("webtorrent" , "mpv")
    players = ["mpv" , "vlc"]
    clients = ["webtorrent" , "peerflix"]

    if not Path(config_path).is_file():
        return default_value

    with open(config_path) as f:
        config = json.loads(f.read())
    
    if config["config"]["player"] and config["config"]["client"]:
        if config["config"]["player"] in players and config["config"]["client"] in clients:
            return (  config["config"]["client"] , config["config"]["player"] )
    
    return default_value
        
def stream(mag_url):
    client , player = parse_config()
    subprocess.run([client , mag_url , f"--{player}" ])


console = Console()

try:
    if len(sys.argv) > 1:
        query = "".join(sys.argv[1:])
    else:
        query = Prompt.ask("What you want to watch today ?")

    print("  Finding torrents" , end="\r")

    with Spinner():
        if query == "1":
            movie_list = pirate()["movie_info"]
        else:
            movie_list = pirate(query=query)["movie_info"]

    if len(movie_list) == 0:
        greet_bye()
        exit(1)

    write_table(movie_list)

    movie_ind = Prompt.ask("Select your fav" , default="1")
    if int(movie_ind) >= len(movie_list):
        mag_url = movie_list[-1]["magnet_url"]
    else:
        mag_url = movie_list[int(movie_ind)-1]["magnet_url"]

except KeyboardInterrupt:
    add_cursor()
    greet_bye()
    exit(1)

print("Enjoy! Less seeds may take more time\nStreaming will start after 1% of downloading")
stream(mag_url)





