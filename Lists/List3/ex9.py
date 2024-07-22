def main() -> None:
    PATHFILE = 'Practice/Files/pessoasVar.bin'
    try:
        file = open(PATHFILE, 'rb')
        transactions = open('Lists/List3/ex9Transactions.txt', 'r')
        output = open('Lists/List3/ex9Answers.txt', 'w')

        def ReadFields(size, content) -> list[str]:
            fields:list[str] = content.split('|')
            fields.pop()
            return fields

        primaryKey:list[str] = transactions.readlines()
        for i in range(len(primaryKey)):
            primaryKey[i] = primaryKey[i].replace('\n', '')
        print(primaryKey)

        for j in range(len(primaryKey)):
            while keySize := int.from_bytes(file.read(2)):
                content = file.read(keySize).decode()
                fields = ReadFields(keySize, content)

                if primaryKey[j] == fields[0]:
                    output.write(content + '\n')
            file.seek(0)
        file.close()
        output.close()
        transactions.close()
        exit()
        
        print('\nRegistro Não Encontrado')
        file.close()

    except OSError as e:
        print(e)

if __name__ == '__main__':
    main()