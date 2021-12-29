import nested_dict as nd
import xml.etree.ElementTree as ET


f = open('ekaterinburg.txt', 'r', encoding="utf-8")
new_dictionary = nd.nested_dict()

#tree = ET.parse('ekaterinburg.txt')
#root = tree.getroot()
#for child in tree:
    #print(child.tag, child.attrib, child.text)


for line in f:
    if "id" in line and "lat" in line and "lon" in line:
        k = int(line.find("id"))
        d = int(line.find("lat"))
        t = int(line.find("lon"))
        id = line[k + 4: k + 13]
        lat = line[d + 5: d + 15]
        lan = line[t + 5: t + 15]
        new_dictionary[lat][lan] = id
print(new_dictionary)