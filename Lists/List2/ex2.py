def main() -> None:
    try:
        PATH:str = "Lists/List2/Files/"
        NAME:str = "Ex1.txt" #input("Digite o nome do Arquivo: ")
        file = open(PATH+NAME, 'rb')

        lines:int = 1
        size:int = 0
        while c := file.read(1):
            if c == b'\n':
                lines += 1
            size += 1
        print(f'Tamanho do arquivo é {size} bytes.')
        print(f'O arquivo tem {lines} linhas.')
        
        file.close()

    except OSError as e:
        print(e)

if __name__ == '__main__':
    main()

# Abrir com leitura em bytes
# Fazer letra por letra para não sobrecarregar o buffer
# verificar com o b'\n'