import argparse
import json
from datetime import datetime
from calculations import simplify_words, find_best_way, find_coords, \
    build_bad_words, process_nodes_and_ways, find_with_api
from display import print_coords
from files import read_file, save_to_file


def prepare_parser(districts):
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-d", help=f"Choose one district: {' '.join(districts)}",
        type=str)
    parser.add_argument("-s", help="Save result?", default=False,
                        action="store_true")
    parser.add_argument("--use_overpass", help="Use overpass?", default=False,
                        action="store_true")
    parser.add_argument("data", help="data", nargs="+")
    return parser


def main():
    districts = {
        "северо-кавказский": "north-caucasus-fed-district-latest.osm",
        "южный": "south-fed-district-latest.osm",
        "центральный": "central-fed-district-latest.osm",
        "приволжский": "volga-fed-district-latest.osm",
        "северо-западный": "northwestern-fed-district-latest.osm",
        "уральский": "ural-fed-district-latest.osm",
        "сибирский": "siberian-fed-district-latest.osm",
        "дальневосточный": "far-eastern-fed-district-latest.osm",
        "крымский": "crimean-fed-district-latest.osm"
    }
    parser = prepare_parser(districts)
    args = parser.parse_args()
    words = [x.lower() for x in args.data]
    bad_words = build_bad_words(read_file("bad_words.txt").split())
    simplify_words(words, bad_words)

    if args.use_overpass:
        coords = find_with_api(" ".join(words))
        district = "None"
    else:
        try:
            district = districts[args.d.lower()]
        except KeyError:
            raise KeyError("Неверное название региона.")

        nodes, ways = process_nodes_and_ways(district, bad_words)

        variant = find_best_way(words, ways)
        if variant == ("", 0):
            raise ValueError("Лушего пути нет. Ошибка ввода.")
        coords = find_coords(ways[variant[0]], nodes)
    print_coords(coords)

    if args.s:
        save_to_file(
            f"{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.txt",
            district, " ".join(words), json.dumps(coords))


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(e)
