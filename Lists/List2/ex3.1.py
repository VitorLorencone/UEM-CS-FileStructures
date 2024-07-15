# Remove Espaços

def main() -> None:
    PATH = 'Lists/List2/Files/'
    try:
        NAME:str = input("Digite o nome do arquivo: ")
        source = open(PATH+NAME, "rb")
        NAME = NAME[:NAME.find('.')] + '_noSpaces' + NAME[NAME.find('.'):]
        processed = open(PATH+NAME, 'wb')

        while c := source.read(1):
            if c == b' ':
                continue
            processed.write(c)

        source.close()
        processed.close()

    except OSError as e:
        print(e)

if __name__ == '__main__':
    main()