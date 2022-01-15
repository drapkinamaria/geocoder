from os.path import exists
from pathlib import Path
from geopy.geocoders import Nominatim
from files import json_to_dict, read_file, save_to_json, download_district
from suffix_tree import SuffixTree


def process_nodes_and_ways(district, bad_words):
    filename = district.split(".")[0]
    nodes_path = f"./processed_data/{filename}_nodes.txt"
    ways_path = f"./processed_data/{filename}_ways.txt"
    Path("./processed_data").mkdir(parents=True, exist_ok=True)

    if exists(nodes_path) and exists(ways_path):
        nodes = json_to_dict(nodes_path)
        ways = json_to_dict(ways_path)
    else:
        if not exists(f"./districts/{district}"):
            download_district(district)
        data = read_file(f"./districts/{district}")
        nodes = get_nodes(data)
        ways = get_ways(data, bad_words)
        save_to_json(nodes_path, nodes)
        save_to_json(ways_path, ways)

    return nodes, ways


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
        result[i] = {"nodes": nodes, "tags": new_tags}
    return result


def find_intersections(words, tree):
    result = 0
    for i in words:
        if tree.has_substring(i):
            result += 1
    return result


def make_trees(ways):
    result = {}
    for k, v in ways.items():
        result[k] = SuffixTree(" ".join(v["tags"]))
    return result


def find_best_way(words, ways):
    result = ({}, 0)
    for k, v in ways.items():
        i = find_intersections(words, v)
        if i > result[1]:
            result = (k, i)
    return result


def find_coords(way, nodes):
    result = {}
    for i, v in enumerate(way["nodes"]):
        result[f"{i+1}"] = nodes[v]
    return result


def find_with_api(address):
    geolocator = Nominatim(user_agent="my-application@gmail.com")
    location = geolocator.geocode(address)
    return {"1": {"lat": location.latitude, "lon": location.longitude}}
