def main() -> None:
    PATHFILE:str = 'Practice/Files/pessoasFixo.bin'
    HEADERSIZE:int = 4
    REGSIZE = 64

    try:
        file = open(PATHFILE, 'rb')

        def ReadFields(size:int) -> list[str]:
            fields:list[str] = file.read(size).decode().split('|')
            fields.pop()
            return fields

        MAXREG:int = int.from_bytes(file.read(HEADERSIZE))

        rrn = int(input("Digite o valor de busca: "))

        if rrn > MAXREG-1 or rrn < 0:
            print("Registro não encontrado")
            file.close()
            exit()

        offset:int = rrn*REGSIZE + HEADERSIZE
        file.seek(offset)

        fields = ReadFields(REGSIZE)

        print('\nRegistro Encontrado:\n')
        for i in range(len(fields)):
            print(f'Campo {i+1} - {fields[i]}')
        
        file.close()

    except OSError as e:
        print(e)

if __name__ == '__main__':
    main()