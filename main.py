from calculations import get_nodes, get_ways, simplify_words, find_best_way, \
    find_coords
from display import print_coords
from files import read_file


def main():
    data = read_file(r".\districts\crimean-fed-district-latest.osm")
    nodes = get_nodes(data)
    ways = get_ways(data)

    words = "г. Екатеринбург Льва_Толстого улица".lower().split()
    simplify_words(words)

    variant = find_best_way(words, ways)
    if variant == ("", 0):
        raise ValueError("Лушего пути нет. Ошибка ввода.")
    coords = find_coords(ways[variant[0]], nodes)
    print_coords(coords)


if __name__ == '__main__':
    main()
