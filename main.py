from input_parsing import build_place


def main():
    place = build_place("екатеринбург 66 ул. фурманова".lower().split())


if __name__ == '__main__':
    main()
