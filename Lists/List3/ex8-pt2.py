# Lê Registros

REGSIZE = 128
HEADERSIZE = 4

def main() -> None:
    PATHFILE:str = 'Lists/List3/Files/People.bin'
    
    try:
        file = open(PATHFILE, 'rb')
    
    except OSError as e:
        print(e)

    def ReadFields(size = REGSIZE):
        fields = file.read(size).decode().split('|')
        fields.pop()
        return fields

    while fields := ReadFields():
        print("\nRegistro: ")
        for i in range(len(fields)):
            print(f'   Campo {i+1} - {fields[i]}')

    file.close()

if __name__ == '__main__':
    main()