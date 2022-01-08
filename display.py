def print_coords(coords):
    t = ["N", "LAT", "LON"]
    print("=======================================")
    print("Подходящие варианты:")
    print(f'{t[0]:5} {t[1]:15} {t[2]:10}')
    for i, v in coords.items():
        print(f'{i:5} {v["lat"]:15} {v["lon"]:15}')
    print("=======================================")
