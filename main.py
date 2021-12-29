import nested_dict as nd

f = open('ekaterinburg.txt', 'r', encoding="utf-8")
new_dictionary = nd.nested_dict()
count = 0


for line in f:
    if "id" in line and "lat" in line and "lon" in line:
        count += 1
        k = int(line.find("id"))
        d = int(line.find("lat"))
        t = int(line.find("lon"))
        id = line[k + 4: k + 13]
        lat = line[d + 5: d + 15]
        lan = line[t + 5: t + 15]
        new_dictionary[lat][lan] = id
print(new_dictionary)