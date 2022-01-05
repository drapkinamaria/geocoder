import time
import urllib.request
import bz2


def read_file(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        return file.read()


def download_district(district):
    url = f"http://download.geofabrik.de/russia/{district}.bz2"
    try:
        file = urllib.request.urlretrieve(url, f"./districts/{district}.bz2")
    except Exception:
        raise ValueError("Ссылка скачивания больше недействительна.")
    time.sleep(3)
    z = bz2.BZ2File(f"./districts/{district}.bz2")
    open(f"./districts/{district}", 'wb').write(z.read())
    time.sleep(3)
