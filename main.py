import re
from collections import defaultdict
from xml.etree.ElementTree import XML

from files import read_file
import nested_dict as nd


def get_nodes(lines):
    new_dictionary = nd.nested_dict()
    for line in lines:
        if "id" in line and "lat" in line and "lon" in line:
            k = int(line.find("id"))
            d = int(line.find("lat"))
            t = int(line.find("lon"))
            id = line[k + 4: k + 13]
            lat = line[d + 5: d + 14]
            lan = line[t + 5: t + 15]
            new_dictionary[lat][lan] = id
    return new_dictionary


def etree_to_dict(t):
    d = {t.tag: {} if t.attrib else None}
    children = list(t)
    if children:
        dd = defaultdict(list)
        for dc in map(etree_to_dict, children):
            for k, v in dc.items():
                dd[k].append(v)
        d = {t.tag: {k: v[0] if len(v) == 1 else v for k, v in dd.items()}}
    if t.attrib:
        d[t.tag].update((k, v) for k, v in t.attrib.items())
    if t.text:
        text = t.text.strip()
        if children or t.attrib:
            if text:
                d[t.tag]["#text"] = text
        else:
            d[t.tag] = text
    return d


def simplify_nodes_ids(nds):
    if len(nds) == 1:
        return [nds['ref']]
    result = []
    for i in nds:
        result.append(i['ref'])
    return result


def get_way(row, text):
    local_text = text[text.find("<way "):text.rfind("</way>")]
    for way in local_text.split("</way>"):
        all_exists = True
        for i in row.split():
            if i not in way:
                all_exists = False
                break
        if all_exists:
            return way


def main():
    row = "Екатеринбург Ленина 51"
    text = read_file("ekaterinburg.txt")
    nodes = get_nodes(text.split("\n"))
    way = get_way(row, text)


if __name__ == '__main__':
    main()
