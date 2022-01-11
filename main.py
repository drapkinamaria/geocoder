import json
from datetime import datetime
from calculations import simplify_words, find_best_way, find_coords, \
    get_district_filename, build_bad_words, process_nodes_and_ways
from display import print_coords
from files import read_file, save_to_file


def main():
    bad_words = build_bad_words(read_file("bad_words.txt").split())
    district = get_district_filename()
    words = input("Введите место: ").lower().split()
    simplify_words(words, bad_words)
    save = input("Сохранить результаты (да/нет): ")

    nodes, ways = process_nodes_and_ways(district, bad_words)

    variant = find_best_way(words, ways)
    if variant == ("", 0):
        raise ValueError("Лушего пути нет. Ошибка ввода.")
    coords = find_coords(ways[variant[0]], nodes)
    print_coords(coords)

    if save == "да":
        save_to_file(
            f"{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.txt",
            district,
            " ".join(words),
            json.dumps(coords))


if __name__ == '__main__':
    main()
