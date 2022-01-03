from files import read_file
from Levenshtein import distance


def get_by_beginning(needle, text):
    index = text.find(needle)
    if index == -1:
        raise ValueError
    start = index + len(needle)
    end = text[start:].find("\"")
    return text[start:start + end]


def get_nodes(text):
    result = {}
    for line in text.split("\n"):
        try:
            i = get_by_beginning("id=\"", line)
            lat = get_by_beginning("lat=\"", line)
            lon = get_by_beginning("lon=\"", line)
            result[i] = {"lat": lat, "lon": lon}
        except ValueError:
            continue
    return result


def find_nodes(lines):
    result = []
    for i in lines:
        if "nd ref=\"" in i:
            result.append(get_by_beginning("nd ref=\"", i))
    return result


def find_tags(lines):
    result = {}
    for i in lines:
        if "<tag k=\"" in i:
            value = get_by_beginning("v=\"", i)
            if "улица" in value or "Улица" in value or \
                    "street" in value or "Street" in value:
                value = value.replace("улица", "").replace("Улица", "")
                value = value.replace("street", "").replace("Street", "")
                value = value.replace(" ", "")
            result[get_by_beginning("<tag k=\"", i)] = value
    return result


def get_ways(text):
    result = {}
    local_text = text[text.find("<way "):text.rfind("</way>")]
    for way in local_text.split("</way>"):
        try:
            i = get_by_beginning("id=\"", way)
        except ValueError:
            continue
        lines = way.split("\n")[1:]
        nodes = find_nodes(lines)
        tags = find_tags(lines)
        result[i] = {'nodes': nodes, 'tags': tags}
    return result


def check_distances(word, array):
    for i in array:
        if distance(word, i) < 2:
            return True
    return False


def find_variants_tier1(words, ways):
    result = []
    for way in ways.values():
        for word in words:
            if "tags" in way:
                if check_distances(word, way["tags"].values()):
                    result.append(way)
    return result


def find_variants_tier2(words, variants):
    result = []
    for variant in variants:
        all_here = True
        for word in words:
            if not check_distances(word, variant["tags"].values()):
                all_here = False
                break
        if all_here:
            result.append(variant)
    return result


def find_nodes_ids(variants, nodes):
    result = []
    for variant in variants:
        for node in variant["nodes"]:
            if node in nodes:
                result.append(node)
    return result


def find_coords(variants, nodes):
    result = []
    for i in find_nodes_ids(variants, nodes):
        result.append(nodes[i])
    return result


def print_coords(coords):
    t = ["N", "LAT", "LON"]
    print("=======================================")
    print("Подходящие варианты:")
    print(f'{t[0]:5} {t[1]:15} {t[2]:10}')
    for i in range(len(coords)):
        print(f'{i:5} {coords[i]["lat"]:15} {coords[i]["lon"]:15}')
    print("=======================================")


def main():
    print("Введите данные через пробел")
    print("Пример: Екатеринбург Восточная")
    words = "Екатеринбург Восточная".split()  # input().split()
    text = read_file("ekaterinburg.txt")
    nodes = get_nodes(text)
    ways = get_ways(text)
    vars_tier1 = find_variants_tier1(words, ways)
    vars_tier2 = find_variants_tier2(words, vars_tier1)
    final_vars = vars_tier2[:5] if vars_tier2 else vars_tier1[:5]
    coords = find_coords(final_vars, nodes)
    print_coords(coords)


if __name__ == '__main__':
    main()
