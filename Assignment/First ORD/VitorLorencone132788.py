# LED com WORST FIT

# Aluno: Vitor Madeira Lorençone
# RA: 132788
# OBS: Toda operação feita com o programa gera um ARQUIVO de saída, chamado output.txt, em que constará todas as útlimas operações realizadas
# OBS: Minha LED deixa a sobra no começo do espaço

import sys

# Constantes
PATHFILE:str = 'dados.dat'
OUTPUTFILE:str = 'output.txt'
HEADERSIZE:int = 4
REGSIZE:int = 2
LEDOFFSETSIZE = 4
LEDMINIMUMSIZE = 10

# Função que executa as operações
def main(operations:str) -> None:

    # Acessa o arquivo de dados
    try:
        dataFile = open(PATHFILE, 'r+b')
    except OSError as e:
        print(e)
        exit()

    # Acessa o arquivo de operações
    try:
        if operations != '-p':
            opFile = open(operations, 'r', encoding="utf8")
    except OSError as e:
        print(e)
        exit()

    # Acessa o arquivo de output
    try: 
        outputFile = open(OUTPUTFILE, 'w', encoding="utf8")
    except OSError as e:
        print(e)
        exit()

    # LED
    LED:int = int.from_bytes(dataFile.read(HEADERSIZE), signed=True)

    # Retorna uma lista da LED com os offsets
    def ledList() -> list[list[int]]:
        lst:list = []
        dataFile.seek(0)
        led:int = int.from_bytes(dataFile.read(HEADERSIZE), signed=True)

        if led == -1:
            return lst

        dataFile.seek(led)
        ledSize:int = int.from_bytes(dataFile.read(REGSIZE), signed=True)
        
        while led != -1:
            lst.append([led, ledSize])
            dataFile.seek(led+REGSIZE+1)
            led = int.from_bytes(dataFile.read(LEDOFFSETSIZE), signed=True)
            if led != -1:
                dataFile.seek(led)
                ledSize:int = int.from_bytes(dataFile.read(REGSIZE), signed=True)
        return lst

    # Busca Sequencial
    def searchOperation(arg:str) -> None:
        dataFile.seek(HEADERSIZE)
        while size := int.from_bytes(dataFile.read(REGSIZE), signed=True):

            tempTell = dataFile.tell()
            if dataFile.read(1) == b'*':
                dataFile.seek(size-1, 1)
                continue
            else:
                dataFile.seek(tempTell)

            field:list[str] = dataFile.read(size).decode().split('|')
            field.pop()

            if field[0] == arg:
                outputFile.write(f'Busca pelo registro de chave "{arg}"\n')
                outputBuffer:str = ''

                for i in field:
                    outputBuffer += i + '|'
            
                outputBuffer += f' ({size} bytes)\n\n'
                outputFile.write(outputBuffer)
                return None

        outputFile.write(f'Busca pelo registro de chave "{arg}"\n')
        outputFile.write(f'Erro: registro não encontrado!\n\n')
        return None

    # Remoção de Registro
    def removeOperation(arg:str) -> None:
        dataFile.seek(0)
        LED:int = int.from_bytes(dataFile.read(HEADERSIZE), signed=True)

        while size := int.from_bytes(dataFile.read(REGSIZE), signed=True):
            offset:int = dataFile.tell() - REGSIZE

            tempTell = dataFile.tell()
            if dataFile.read(1) == b'*':
                dataFile.seek(size-1, 1)
                continue
            else:
                dataFile.seek(tempTell)
                
            field:list[str] = dataFile.read(size).decode().split('|')
            field.pop()

            if field[0] == arg:
                dataFile.seek(offset + REGSIZE)

                if LED == -1:
                    dataFile.write(b'\x2A')
                    dataFile.write(b'\xFF\xFF\xFF\xFF')
                    LED = offset
                elif LED != -1:
                    dataFile.seek(LED)
                    ledSize = int.from_bytes(dataFile.read(REGSIZE), signed=True)

                    if ledSize <= size:
                        dataFile.write(b'\x2A')
                        dataFile.write(int.to_bytes(LED, LEDOFFSETSIZE))
                        LED = offset
                    elif ledSize > size:
                        ledlst:list[list[int]] = ledList()
                        switchPoint:int = len(ledlst)-1
                        for i in range(len(ledlst)):
                            if size > ledlst[i][1]:
                                switchPoint = i-1
                                break
                        dataFile.seek(ledlst[switchPoint][0] + REGSIZE + 1)
                        temp:bytes = dataFile.read(LEDOFFSETSIZE)
                        dataFile.seek(ledlst[switchPoint][0] + REGSIZE + 1)
                        dataFile.write(int.to_bytes(offset, 4))
                        dataFile.seek(offset + REGSIZE)
                        dataFile.write(b'*')
                        dataFile.write(temp)
                    
                dataFile.seek(0)
                dataFile.write(int.to_bytes(LED, HEADERSIZE))

                outputFile.write(f'Remoção do registro de chave "{arg}"\n')
                outputFile.write(f'Registro removido! ({size} bytes)\n')
                outputFile.write(f'Local: offset = {offset} bytes ({hex(offset)})\n\n')
                return None

        outputFile.write(f'Remoção do registro de chave "{arg}"\n')
        outputFile.write(f'Erro: registro não encontrado!\n\n')
        return None

    # Inserção de Registro
    def insertOperation(arg:str) -> None:
        dataFile.seek(0)
        LED:int = int.from_bytes(dataFile.read(HEADERSIZE), signed=True)

        ledlst = ledList()
        insertionSize = len(arg.encode())

        if ledlst == [] or insertionSize > ledlst[0][1]:
            dataFile.seek(0,2)
            dataFile.write(int.to_bytes(insertionSize, REGSIZE))
            dataFile.write(arg.encode())

            outputFile.write(f'Inserção do registro de chave "{arg.split('|')[0]}" ({insertionSize} bytes)\n')
            outputFile.write(f'Local: Fim do Arquivo\n\n')

        elif insertionSize <= ledlst[0][1]:
            size = ledlst[0][1]
            dataFile.seek(ledlst[0][0])
            newSize:int = size - REGSIZE - insertionSize
            if newSize > LEDMINIMUMSIZE:
                dataFile.write(int.to_bytes(newSize, REGSIZE))
            else:
                dataFile.seek(REGSIZE, 1)
            newOffset:int = dataFile.tell() - REGSIZE

            offset = ledlst[0][0] + size - insertionSize
            dataFile.seek(offset)
            dataFile.write(int.to_bytes(insertionSize, 2))
            dataFile.write(arg.encode())

            dataFile.seek(ledlst[0][0] + REGSIZE)

            if newSize > ledlst[0][1] and newSize > LEDMINIMUMSIZE:
                dataFile.write(b'\x2A')
                dataFile.write(int.to_bytes(LED, LEDOFFSETSIZE))
                LED = newOffset
            elif newSize > LEDMINIMUMSIZE:
                switchPoint:int = len(ledlst)-1
                for i in range(len(ledlst)):
                    if newSize >= ledlst[i][1]:
                        switchPoint = i-1
                        break

                    dataFile.seek(ledlst[switchPoint][0] + REGSIZE + 1)
                    temp:bytes = dataFile.read(LEDOFFSETSIZE)
                    dataFile.seek(ledlst[switchPoint][0] + REGSIZE + 1)
                    dataFile.write(int.to_bytes(newOffset, 4))
                    dataFile.seek(newOffset + REGSIZE)
                    dataFile.write(b'*')
                    dataFile.write(temp)

            if ledlst[0][1] - insertionSize - REGSIZE < LEDMINIMUMSIZE and len(ledlst) == 1:
                ledlst = []
                LED = -1

            dataFile.seek(0)
            if LED == -1:
                dataFile.write(b'\xFF\xFF\xFF\xFF')
            else:
                dataFile.write(int.to_bytes(LED, HEADERSIZE))

            outputFile.write(f'Inserção do registro de chave "{arg.split('|')[0]}" ({insertionSize} bytes)\n')
            if size - insertionSize - REGSIZE > LEDMINIMUMSIZE:
                outputFile.write(f'Tamanho do Espaço Reutilizado: {size} bytes (Sobra de {newSize} bytes)\n')
            else:
                outputFile.write(f'Tamanho do Espaço Reutilizado: {size} bytes\n')
            outputFile.write(f'Local: offset = {offset -2*insertionSize + size - REGSIZE} bytes ({hex(offset -2*insertionSize + size - REGSIZE)})\n\n')
        return None

    if operations == '-p':
        ledlst = ledList()
        outputFile.write(f'LED -> ')
        for i in range(len(ledlst)):
            outputFile.write(f'[offset: {ledlst[i][0]}, tam: {ledlst[i][1]}] -> ')
        outputFile.write(f'[offset: -1]\n')
        outputFile.write(f'Total: {len(ledlst)} espaços disponíveis')
        return None

    # Coloca em memória todas as operações e seus argumentos
    opList:list = []
    argList:list = []

    for i in opFile.readlines():
        i = i.replace('\n', '')
        opList.append(i[0])
        i = i[2:]
        argList.append(i)

    # Execução de cada operação, em ordem
    for i in range(len(opList)):
        match(opList[i]):
            case 'b':
                searchOperation(argList[i])
            case 'i':
                insertOperation(argList[i])
            case 'r':
                removeOperation(argList[i])

    # Fecha os arquivos
    outputFile.close()
    dataFile.close()
    opFile.close()

# Seleção da função e flag utilizada
if __name__ == '__main__':

    if len(sys.argv) <= 1:
        print("Insira a flag requerida, como -p ou -e")
        exit()

    if sys.argv[1] == '-p':
        main('-p')
    elif sys.argv[1] == '-e':
        if len(sys.argv) <= 2:
            print("Insira o arquivo de operações!")
            exit()
        main(sys.argv[2])