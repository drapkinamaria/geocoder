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


def get_way(row, text):
    local_text = text[text.find("<way "):text.rfind("</way>")]
    for way in local_text.split("</way>"):
        all_exists = False
        for i in row.split():
            if i not in way[way.find("<tag"):way.rfind("</tag")]:
                all_exists = True
                break
        if all_exists:
            return way


def main():
    row = "Екатеринбург Ленина 51"
    text = read_file("ekaterinburg.txt")
    nodes = get_nodes(text.split("\n"))
    way = get_way(row, text)
    x = 1


if __name__ == '__main__':
    main()
