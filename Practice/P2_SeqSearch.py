def main() -> None:
    PATHFILE = 'Practice/Files/pessoasVar.bin'
    try:
        file = open(PATHFILE, 'rb')

        def ReadFields(size) -> list[str]:
            fields:list[str] = file.read(size).decode().split('|')
            fields.pop()
            return fields

        primaryKey:str = input("Digite o Sobrenome: ")

        while keySize := int.from_bytes(file.read(2)):
            fields = ReadFields(keySize)

            if primaryKey == fields[0]:
                print('\nRegistro Encontrado:\n')
                for i in range(len(fields)):
                    print(f'Campo {i+1} - {fields[i]}')
                file.close()
                exit()
        
        print('\nRegistro Não Encontrado')
        file.close()

    except OSError as e:
        print(e)

if __name__ == '__main__':
    main()