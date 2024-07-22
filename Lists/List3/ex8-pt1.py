# Escreve Registros

REGSIZE = 128
HEADERSIZE = 4

def main() -> None:
    PATHFILE:str = 'Lists/List3/Files/People.bin'
    
    try:
        file = open(PATHFILE, 'ab')
    
    except OSError as e:
        file = open(PATHFILE, 'wb')

    file.seek(0, 2)

    buffer:str = ''
    print("Adicionar Registro: ")
    buffer += input("Digite a Chave: ") + '|'
    buffer += input("Digite a Nome: ") + '|'
    buffer += input("Digite a CEP: ") + '|'
    buffer = buffer.encode()

    if len(buffer) > REGSIZE:
        print("Registro Muito grande")
        exit()
    elif len(buffer) < REGSIZE:
        buffer = buffer.ljust(REGSIZE, b'\0')

    file.write(buffer)

    file.close()

if __name__ == '__main__':
    main()