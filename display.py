def print_coords(coords):
    t = ["N", "LAT", "LON"]
    print("=======================================")
    print("Подходящие варианты:")
    print(f'{t[0]:5} {t[1]:15} {t[2]:10}')
    for i in range(len(coords)):
        print(f'{i:5} {coords[i]["lat"]:15} {coords[i]["lon"]:15}')
    print("=======================================")