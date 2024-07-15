# Remove Espaços Repetidos

def main() -> None:
    PATH = 'Lists/List2/Files/'
    try:
        NAME:str = input("Digite o nome do arquivo: ")
        source = open(PATH+NAME, "rb")
        NAME = NAME[:NAME.find('.')] + '_noDoubleSpaces' + NAME[NAME.find('.'):]
        # Poderia usar o .rstrip
        processed = open(PATH+NAME, 'wb')

        bAnterior:bytes = b''
        while bAtual := source.read(1):
            if bAnterior == b' ' and bAtual == b' ':
                continue
            processed.write(bAtual)
            bAnterior = bAtual

        source.close()
        processed.close()

    except OSError as e:
        print(e)

if __name__ == '__main__':
    main()