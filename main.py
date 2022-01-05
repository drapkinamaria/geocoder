from os.path import exists
from calculations import get_nodes, get_ways, simplify_words, find_best_way, \
    find_coords, get_district_filename
from display import print_coords
from files import read_file, download_district


def main():
    district = get_district_filename(input("Введите федеральный округ: "))
    if not exists(f".\\districts\\{district}"):
        print("Округ не найден. Идет скачивание.")
        download_district(district)
        print("Округ скачан.")
    print("Чтение файла.")
    data = read_file(f".\\districts\\{district}")
    print("Файл прочитан.")
    nodes = get_nodes(data)
    print("Узлы получены.")
    ways = get_ways(data)
    print("Пути получены.")

    words = input("Введите место: ").lower().split()
    simplify_words(words)

    variant = find_best_way(words, ways)
    if variant == ("", 0):
        raise ValueError("Лушего пути нет. Ошибка ввода.")
    coords = find_coords(ways[variant[0]], nodes)
    print_coords(coords)


if __name__ == '__main__':
    main()
