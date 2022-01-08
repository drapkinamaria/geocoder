import json
from datetime import datetime
from os.path import exists
from calculations import get_nodes, get_ways, simplify_words, find_best_way, \
    find_coords, get_district_filename, build_bad_words
from display import print_coords
from files import read_file, download_district, save_to_file


def main():
    bad_words = build_bad_words(read_file("bad_words.txt").split())
    district = get_district_filename()
    words = input("Введите место: ").lower().split()
    simplify_words(words, bad_words)
    save_to_json = input("Сохранить результаты (да/нет): ")

    if not exists(f".\\districts\\{district}"):
        print("\rОкруг не найден. Идет скачивание.", end="")
        download_district(district)
    print("\rЧтение файла.     [1/3]", end="")
    data = read_file(f".\\districts\\{district}")
    print("\rПолучение узлов.  [2/3]", end="")
    nodes = get_nodes(data)
    print("\rПолучение путей.  [3/3]", end="")
    ways = get_ways(data, bad_words)

    variant = find_best_way(words, ways)
    if variant == ("", 0):
        raise ValueError("Лушего пути нет. Ошибка ввода.")
    coords = find_coords(ways[variant[0]], nodes)
    print_coords(coords)

    if save_to_json == "да":
        save_to_file(
            f"{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.txt",
            district,
            " ".join(words),
            json.dumps(coords))


if __name__ == '__main__':
    main()
