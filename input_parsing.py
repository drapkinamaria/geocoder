from files import read_file


def remove_designations(data, designations):
    for i in designations:
        try:
            data.remove(i)
        except ValueError:
            pass


def check_city(data, place):
    for i in read_file("cities.txt").split("\n"):
        if i in data:
            place["city"] = i
            remove_designations(data,
                                ["город", "город.", "гор", "гор.", "г", "г."])
            data.pop(data.index(i))
            break


def check_number(data, place):
    for i in data:
        if i.isdigit():
            place["number"] = i
            remove_designations(data, ["дом", "дом.", "д", "д."])
            data.pop(data.index(i))
    pass


def check_street(data, place):
    remove_designations(data, ["улица", "улица.", "ул", "ул."])
    if len(data) > 1:
        raise ValueError
    else:
        place["street"] = data[0]
    pass


def build_place(data):
    place = {
        "city": "екатеринбург",
        "street": "",
        "number": "",
    }
    check_city(data, place)
    check_number(data, place)
    check_street(data, place)
    return place
