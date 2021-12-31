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


def get_by_beginning(needle, text):
    index = text.find(needle)
    if index == -1:
        raise ValueError
    start = index + len(needle)
    end = text[start:].find("\"")
    return text[start:start + end]


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
            result[get_by_beginning("<tag k=\"", i)] = get_by_beginning("v=\"", i)
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


def main():
    row = "Екатеринбург Ленина 51"
    text = read_file("ekaterinburg.txt")
    nodes = get_nodes(text.split("\n"))
    ways = get_ways(text)


if __name__ == '__main__':
    main()
