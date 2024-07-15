def main() -> None:
    PATHFILE:str = 'Lists/List2/Files/out8.bin'
    try:
        file = open(PATHFILE, 'rb')

        while stringSize := int.from_bytes(file.read(2)):
            print(file.read(stringSize).decode())

    except OSError as e:
        print(e)

if __name__ == '__main__':
    main()