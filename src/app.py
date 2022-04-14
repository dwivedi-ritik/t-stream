#! /usr/bin/python
import sys
import subprocess

from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt
from piratebay import *
from spinner import Spinner , add_cursor


def write_table(movie_list):
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("ID", width=12)
    table.add_column("Title")
    table.add_column("Seeders", justify="right")
    table.add_column("Leeches", justify="right")

    for i , obj in enumerate( movie_list ):
        table.add_row(str(i+1) , obj["title"] , str(obj["seeders"]) , str(obj["leeches"]))

    console.print(table)
    return

def greet_bye():
    print("\nsee ya 👋")

def stream(mag_url):
    subprocess.run(["peerflix" , mag_url , "--mpv"])


console = Console()

try:
        
    if len(sys.argv) > 1:
        query = "".join(sys.argv[1:])
    else:
        query = Prompt.ask("What you want watch today ?")

    print("  Finding torrents" , end="\r")

    with Spinner():
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

stream(mag_url)





