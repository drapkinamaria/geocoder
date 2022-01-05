from os.path import exists
from calculations import get_nodes, get_ways, simplify_words, find_best_way, \
    find_coords, get_district_filename
from display import print_coords
from files import read_file, download_district


def main():
    district = get_district_filename(input("Введите федеральный округ: "))
    words = input("Введите место: ").lower().split()
    simplify_words(words)

    if not exists(f".\\districts\\{district}"):
        print("\rОкруг не найден. Идет скачивание.", end="")
        download_district(district)
        print("\rОкруг скачан.", end="")
    print("\rЧтение файла.   [1/4]", end="")
    data = read_file(f".\\districts\\{district}")
    print("\rФайл прочитан.  [2/4]", end="")
    nodes = get_nodes(data)
    print("\rУзлы получены.  [3/4]", end="")
    ways = get_ways(data)
    print("\rПути получены.  [4/4]", end="")

    variant = find_best_way(words, ways)
    if variant == ("", 0):
        raise ValueError("Лушего пути нет. Ошибка ввода.")
    coords = find_coords(ways[variant[0]], nodes)
    print_coords(coords)


if __name__ == '__main__':
    main()
