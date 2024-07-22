def main() -> None:
    PATHFILE:str = 'Practice/Files/personsGOTFixo.bin'
    HEADERSIZE:int = 4
    REGSIZE = 64

    try:
        file = open(PATHFILE, 'r+b')

    except OSError as e:
        file = open(PATHFILE, 'w+b')
        file.write(int.to_bytes(0, HEADERSIZE))

    MAXREG:int = int.from_bytes(file.read(4))

    def ReadFields(size:int):
        field = file.read(size).decode().split('|')
        field.pop()
        return field

    def InsertFields(rrn:int = MAXREG):
        buffer:str = ''
        file.seek(0)
        MAXREG = int.from_bytes(file.read(4))

        print("Digite os dados para o registro: ")
        buffer += input("Sobrenome: ") + '|'
        buffer += input("     Nome: ") + '|'
        buffer += input(" Endereço: ") + '|'
        buffer += input("   Cidade: ") + '|'
        buffer += input("   Estado: ") + '|'
        buffer += input("      CEP: ") + '|'
        buffer:bytes = buffer.encode()

        if len(buffer) > REGSIZE:
            print("Registro Excede limite permitido")
        elif len(buffer) < REGSIZE:
            buffer = buffer.ljust(REGSIZE, b'\0')
        
        print(MAXREG)
        if rrn == MAXREG:
            MAXREG += 1
            file.seek(0)
            file.write(int.to_bytes(MAXREG, HEADERSIZE))
        
        file.seek(rrn*REGSIZE + HEADERSIZE)
        file.write(buffer)
        file.seek(0)

    try:
        while True:

            print("Programa para Inserção e Alteração:\n ")
            print("Suas Opções são: ")
            print("1 - Inserir um Novo Registro")
            print("2 - Buscar ou Alterar um Registro")
            print("3 - Terminar Programa\n")

            option:int = int(input("Digite a opção: "))

            match(option):
                case 1:
                    InsertFields(MAXREG)
                
                case 2:

                    rrn:int = int(input("Digite o RRN do registro: "))

                    if rrn < 0 or rrn > MAXREG - 1:
                        print("Registro não encontrado")
                        continue
                    
                    file.seek(rrn*REGSIZE + HEADERSIZE)
                    fields = ReadFields(REGSIZE)

                    print('\nRegistro Encontrado:\n')
                    for i in range(len(fields)):
                        print(f'Campo {i+1} - {fields[i]}')

                    update = input('\nDeseja Alterar o registro? (S/N): ')
                    if(update == 'S' or update == 's'):
                        InsertFields(rrn)

                case 3:
                    file.close()
                    exit()
            
            file.seek(0)

    except OSError as e:
        print(e)

if __name__ == '__main__':
    main()