import nested_dict as nd

f = open('ekaterinburg.txt', 'r')
new_dictionary = nd.nested_dict()
for line in f:
    if "id" in line and "lat" in line and "lon" in line:
        k = int(line.find("id"))
        d = int(line.find("lat"))
        t = int(line.find("lon"))
        print(line)
        id = line[k + 4: k + 13]
        lat = line[d + 5: d + 15]
        lan = line[t + 5: t + 15]
        print(id)
        print(lat)
        print(lan)
        #new_dictionary[lat][lan] = id