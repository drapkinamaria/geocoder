from Levenshtein import distance


def get_district_filename():
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
    print(f"Федеральные округа: {' '.join(districts.keys())}")
    while True:
        try:
            return districts[input("Введите федеральный округ: ").lower()]
        except KeyError:
            print("Неверное название федерального округа. Попробуйте еще раз.")


def get_by_beginning(needle, text):
    index = text.find(needle)
    if index == -1:
        raise ValueError
    start = index + len(needle)
    end = text[start:].find("\"")
    return text[start:start + end]


def build_bad_words(array):
    result = []
    for i in array:
        result.append(f"{i}.")
        result.append(i)
    return result


def simplify_words(array, bad_words):
    for i in array:
        if i in bad_words:
            array.remove(i)


def get_nodes(text):
    result = {}
    local_text = text[:text.find("<way")]
    for line in local_text.split("\n"):
        try:
            i = get_by_beginning("id=\"", line)
            lat = get_by_beginning("lat=\"", line)
            lon = get_by_beginning("lon=\"", line)
            result[i] = {"lat": lat, "lon": lon}
        except ValueError:
            continue
    return result


def find_in_lines(needle, lines):
    result = []
    for i in lines:
        if needle in i:
            result.append(get_by_beginning(needle, i).lower())
    return result


def simplify_tags(tags, bad_words):
    result = []
    for tag in tags:
        elements = tag.split()
        for i in elements:
            if i in bad_words:
                elements.remove(i)
        result.append("_".join(elements))
    return result


def get_ways(text, bad_words):
    result = {}
    local_text = text[text.find("<way "):text.rfind("</way>")]
    for way in local_text.split("</way>"):
        try:
            i = get_by_beginning("id=\"", way)
        except ValueError:
            continue
        lines = way.split("\n")[1:]
        if len(lines) == 1:
            continue
        nodes = find_in_lines("nd ref=\"", lines)
        tags = find_in_lines(" v=\"", lines)
        new_tags = simplify_tags(tags, bad_words)
        result[i] = {'nodes': nodes, 'tags': new_tags}
    return result


def count_intersections(first, second):
    result = 0
    for i in first:
        for j in second:
            if distance(i, j) <= 1:
                result += 1
    return result


def find_best_way(words, ways):
    result = ("", 0)
    for key, value in ways.items():
        i = count_intersections(words, value["tags"])
        if i > result[1]:
            result = (key, i)
    return result


def find_coords(way, nodes):
    result = {}
    for i, v in enumerate(way["nodes"]):
        result[f"{i+1}"] = nodes[v]
    return result
