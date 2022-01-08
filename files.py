import time
import urllib.request
import bz2
from pathlib import Path


def read_file(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        return file.read()


def save_to_file(filename, *args):
    Path('./results').mkdir(parents=True, exist_ok=True)
    with open(f"./results/{filename}", 'w', encoding='utf-8') as file:
        for i in args:
            file.write(i + "\n")


def download_district(district):
    url = f"http://download.geofabrik.de/russia/{district}.bz2"
    Path('./districts').mkdir(parents=True, exist_ok=True)
    try:
        urllib.request.urlretrieve(url, f"./districts/{district}.bz2")
    except Exception:
        raise ValueError("Ссылка скачивания больше недействительна.")
    time.sleep(3)
    z = bz2.BZ2File(f"./districts/{district}.bz2")
    open(f"./districts/{district}", 'wb').write(z.read())
    time.sleep(3)
