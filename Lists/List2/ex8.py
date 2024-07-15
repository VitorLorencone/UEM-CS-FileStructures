def main() -> None:
    PATHFILE:str = 'Lists/List2/Files/out8.bin'
    try:
        file = open(PATHFILE, 'wb')
        while c := input("Frase: "):
            bline = c.encode()
            size:bytes = len(bline).to_bytes(2)
            file.write(size)
            file.write(bline)

    except OSError as e:
        print(e)

if __name__ == '__main__':
    main()