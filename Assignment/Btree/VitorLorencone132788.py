""" 
Aluno: Vitor Madeira Lorençone
RA: 132788
Profa: Valeria Delisandra Feltrim

Trabalho de gerenciamento de registros de um arquivo através de uma Árvore-B, usando um arquivo de operações

Execute por 'python VitorLorencone132788.py -p' ou 'python VitorLorencone132788.py -e op.txt' ou 'python VitorLorencone132788.py -c', por exemplo.

Informações importantes:
1. Tudo foi escrito utilizando a ordenação Little endian
2. O valor nulo definido foi o -1

Coisas que eu quero conversar na apresentação do trabalho:
1. Como foi a sua organização de código?? Eu gostei do meu trabalho, mas acho que organizei de uma forma muito bagunçada!!

Perfeito o trabalho, profa!! Foi bem desafiador e recompensador!! 
"""

# Importação para a leitura das flags
import sys

# Constantes
# Ordem da Árvore-B
TREE_ORDER:int = 8

# Informações sobre tamanho em bytes dos dados da árvore
ROOT_SIZE_BYTES:int = 4
ELEMENT_SIZE_BYTES:int = 4
PAGE_SIZE_BYTES = ELEMENT_SIZE_BYTES * (1 + 2*(TREE_ORDER-1) + TREE_ORDER)

# Constantes que representam as informações do arquivo de dados
HEADER_SIZE_BYTES:int = 4
RECORD_SIZE_BYTES:int = 2

# Caminho para cada arquivo
DATA_FILE_PATH:str = 'games.dat'
TREE_FILE_PATH:str = 'btree.dat'
LOG_PRINT_FILE_PATH:str = 'log-impressao-' + DATA_FILE_PATH.split('.')[0] + '-ordem' + str(TREE_ORDER) + '.txt'

# Classe de Páginas

class Pages:
    """
    Classe que representa as páginas da árvore
    """
    def __init__(self):
        self.numKeys:int = 0
        self.keys:list[int] = [-1]*(TREE_ORDER - 1)
        self.offsets:list[int] = [-1]*(TREE_ORDER - 1)
        self.children:[list[int]] = [-1]*TREE_ORDER
    
    def isFull(self):
        """
        Função que retorna True quando a página está cheia!
        """
        return self.numKeys >= TREE_ORDER - 1

# Funções Auxiliares

def EOF(file)->bool:
    """
    Retorna True se está no fim do arquivo
    """
    currentOffset:int = file.tell()
    file.seek(0, 2)
    eofOffset:int = file.tell()
    file.seek(currentOffset)
    return currentOffset == eofOffset

def readTreeRoot(tree)->int:
    """
    lê a raiz da árvore-B do arquivo btree.dat
    """
    tree.seek(0)
    ans:int = int.from_bytes(tree.read(ROOT_SIZE_BYTES), signed=True, byteorder="little")
    return ans

def writeTreeRoot(tree, root:int)->None:
    """
    Escreve o valor *root* no arquivo btree.dat
    """
    tree.seek(0)
    tree.write(int.to_bytes(root, ROOT_SIZE_BYTES, signed=True, byteorder="little"))

def readPage(tree, rrn:int)->Pages:
    """
    lê a página que está no rrn especificado da árvore
    """

    resp:Pages = Pages()
    byte_offset:int = rrn*PAGE_SIZE_BYTES + ROOT_SIZE_BYTES
    tree.seek(byte_offset)

    resp.numKeys:int = int.from_bytes(tree.read(ELEMENT_SIZE_BYTES), signed=True, byteorder="little")
    for i in range(TREE_ORDER - 1):
        resp.keys[i]:int = int.from_bytes(tree.read(ELEMENT_SIZE_BYTES), signed=True, byteorder="little")
    for i in range(TREE_ORDER - 1):
        resp.offsets[i]:int = int.from_bytes(tree.read(ELEMENT_SIZE_BYTES), signed=True, byteorder="little")
    for i in range(TREE_ORDER):
        resp.children[i]:int = int.from_bytes(tree.read(ELEMENT_SIZE_BYTES), signed=True, byteorder="little")

    return resp

def writePage(tree, rrn:int, pag:Pages)->None:
    """
    Escreve a página no rrn especificado
    """

    byte_offset:int = rrn*PAGE_SIZE_BYTES + ROOT_SIZE_BYTES
    tree.seek(byte_offset)

    tree.write(int.to_bytes(pag.numKeys, ELEMENT_SIZE_BYTES, signed=True, byteorder="little"))
    for i in range(TREE_ORDER - 1):
        tree.write(int.to_bytes(pag.keys[i], ELEMENT_SIZE_BYTES, signed=True, byteorder="little"))
    for i in range(TREE_ORDER - 1):
        tree.write(int.to_bytes(pag.offsets[i], ELEMENT_SIZE_BYTES, signed=True, byteorder="little"))
    for i in range(TREE_ORDER):
        tree.write(int.to_bytes(pag.children[i], ELEMENT_SIZE_BYTES, signed=True, byteorder="little"))

def searchPage(key:int, pag:Pages):
    """
    Procura por uma chave dentro de uma página
    """

    pos:int = 0
    while pos < pag.numKeys and key > pag.keys[pos]:
        pos += 1
    if pos < pag.numKeys and key == pag.keys[pos]:
        return True, pos
    else:
        return False, pos

def searchTree(tree, key:int, rrn:int):
    """
    Procura por uma chave dentro de uma árvore
    """

    if rrn == -1:
        return False, -1, -1
    else:
        pag:Pages = readPage(tree, rrn)
        found, pos = searchPage(key, pag)

        if found is True:
            return True, rrn, pos
        else:
            return searchTree(tree, key, pag.children[pos])

def insertInPage(tree, key:int, offset:int, childR:int, pag:Pages):
    """
    Insere uma chave na página
    """

    if pag.isFull():
        pag.keys.append(-1)
        pag.offsets.append(-1)
        pag.children.append(-1)
    
    i:int = pag.numKeys
    while i > 0 and key < pag.keys[i-1]:
        pag.keys[i] = pag.keys[i-1]
        pag.offsets[i] = pag.offsets[i-1]
        pag.children[i+1] = pag.children[i]
        i -= 1
    
    pag.keys[i] = key
    pag.offsets[i] = offset
    pag.children[i+1] = childR
    pag.numKeys += 1

def nextRRN(tree)->int:
    """
    Busca o próximo rrn para criação de uma página no arquivo da árvore-B
    """

    tree.seek(0, 2) # Fim do arquivo
    offset:int = tree.tell()
    return (offset - ROOT_SIZE_BYTES) // PAGE_SIZE_BYTES

def divide(tree, key:int, offset:int, childR:int, pag:Pages):
    """
    Divide uma página e promove um chave, sendo uma das principais funções de inserção na árvore-B!
    """

    insertInPage(tree, key, offset, childR, pag)

    middle:int = TREE_ORDER//2
    promKey:int = pag.keys[middle]
    promOffset:int = pag.offsets[middle]
    promChildR:int = nextRRN(tree)

    currentPage:Pages = Pages()
    currentPage.numKeys = middle
    currentPage.keys = pag.keys[:middle]
    currentPage.keys += (TREE_ORDER - 1 - len(currentPage.keys))*[-1]
    currentPage.offsets = pag.offsets[:middle]
    currentPage.offsets += (TREE_ORDER - 1 - len(currentPage.offsets))*[-1]
    currentPage.children = pag.children[:middle+1]
    currentPage.children += (TREE_ORDER - len(currentPage.children))*[-1]

    newPage:Pages = Pages()
    newPage.numKeys = TREE_ORDER-middle-1
    newPage.keys = pag.keys[middle+1:]
    newPage.keys += (TREE_ORDER - 1 - len(newPage.keys))*[-1]
    newPage.offsets = pag.offsets[middle+1:]
    newPage.offsets += (TREE_ORDER - 1 - len(newPage.offsets))*[-1]
    newPage.children = pag.children[middle+1:]
    newPage.children += (TREE_ORDER - len(newPage.children))*[-1]

    return promKey, promOffset, promChildR, currentPage, newPage

def insertInTree(tree, key, offset, rrn):
    """
    Insere uma chave na árvore
    """

    if rrn == -1:
        promKey:int = key
        promOffset:int = offset
        promChildR:int = -1
        return promKey, promOffset, promChildR, True
    else:
        pag:Pages = readPage(tree, rrn)
        found, pos = searchPage(key, pag)

    if found == True:
        print(f"Erro: chave \"{key}\" já existente!")
        return -2, -2, -2, False
    
    promKey, promOffset, promChildR, promo = insertInTree(tree, key, offset, pag.children[pos])

    if promo == False:
        return -1, -1, -1, False
    else:
        if not pag.isFull():
            insertInPage(tree, promKey, promOffset, promChildR, pag)
            writePage(tree, rrn, pag)
            return -1, -1, -1, False
        else:
            promKey, promOffset, promChildR, pag, newPag = divide(tree, promKey, promOffset, promChildR, pag)
            writePage(tree, rrn, pag)
            writePage(tree, promChildR, newPag)
            return promKey, promOffset, promChildR, True

def insertionManager(tree, root:int, insertionKeys:list[tuple]):
    """
    Gerencia as inserções em uma árvore-B
    """

    for key, offset in insertionKeys:
        promKey, promOffset, promChildR, prom = insertInTree(tree, key, offset, root)

        if prom == True:
            newPage:Pages = Pages()
            newPage.keys[0] = promKey
            newPage.offsets[0] = promOffset
            newPage.children[0] = root
            newPage.children[1] = promChildR
            newPage.numKeys += 1

            newRRN:int = nextRRN(tree)
            writePage(tree, newRRN, newPage)
            root = newRRN
    
    return root

def retrieveInfoDataFile(file, offset:int)->str:
    """
    Faz uma busca direta no arquivo de dados para recuperar algum registro
    """

    file.seek(offset)
    recSize:int = int.from_bytes(file.read(RECORD_SIZE_BYTES), signed=True, byteorder="little")
    info:str = file.read(recSize).decode()
    return info

def InsertInfoDataFile(file, info:str):
    """
    Faz uma inserção no arquivo da dados
    """

    file.seek(0,2)
    offset:int = file.tell()
    size:int = len(info)
    file.write(int.to_bytes(size, RECORD_SIZE_BYTES, signed=True, byteorder="little"))
    file.write(info.encode())

    file.seek(0)
    header:int = int.from_bytes(file.read(HEADER_SIZE_BYTES), signed=True, byteorder="little")
    file.seek(0)
    file.write(int.to_bytes(header+1, HEADER_SIZE_BYTES, signed=True, byteorder="little"))

    return offset, size

# Funções de Operações

def CreateTree() -> None:
    """
    Função principal para a criação da árvore-B
    """

    try:
        # Acessa o arquivo de Dados
        dataFile = open(DATA_FILE_PATH, 'r+b')

        # Acessa o arquivo de Árvore
        treeFile = open(TREE_FILE_PATH, 'w+b')

    except OSError as e:
        print(e)
        exit()

    root:int = readTreeRoot(treeFile)
    if root == 0:
        writeTreeRoot(treeFile, root)
        writePage(treeFile, 0, Pages())

    dataFile.seek(0)
    header:int = int.from_bytes(dataFile.read(HEADER_SIZE_BYTES), signed=True, byteorder="little")

    insertKeyList:list[tuple] = []

    while not EOF(dataFile):
        offset:int = dataFile.tell()

        recSize:int = int.from_bytes(dataFile.read(RECORD_SIZE_BYTES), signed=True, byteorder="little")
        rawField:bytes = dataFile.read(recSize)
        fields:list[str] = rawField.decode().split("|")

        key:int = int(fields[0])

        insertKeyList.append((key, offset))
    
    root = insertionManager(treeFile, root, insertKeyList)
    writeTreeRoot(treeFile, root)

    dataFile.close()
    treeFile.close()

def ExecuteTree(arg:str) -> None:
    """
    Função principal para a execução do arquivo de operações
    """

    try:
        # Acessa o arquivo de Dados
        dataFile = open(DATA_FILE_PATH, 'r+b')

        # Acessa o arquivo de Árvore
        treeFile = open(TREE_FILE_PATH, 'r+b')

        # Acessa o arquivo de Operações
        operationFile = open(arg, 'r', encoding="utf8")

        #Path do arquivo de Log
        LOG_OP_FILE_PATH:str = 'log-' + arg.split('.')[0] + DATA_FILE_PATH.split('.')[0] + '-ordem' + str(TREE_ORDER) + '.txt'

        # Acessa o arquivo de Log de Operações
        logFile = open(LOG_OP_FILE_PATH, 'w', encoding="utf8")

    except OSError as e:
        print(e)
        exit()

    root:int = readTreeRoot(treeFile)

    # Coloca em memória todas as operações e seus argumentos
    operationInfo:list[list[str]] = []

    for i in operationFile.readlines():
        i = i.replace('\n', '')
        operationInfo.append([i[0], i[2:]])

    # Execução de cada operação, em ordem
    for tasks in operationInfo:

        root:int = readTreeRoot(treeFile)

        match(tasks[0]):
            case 'b':
                key:int = int(tasks[1])
                found, rrn, pos = searchTree(treeFile, key, root)
                logFile.write(f"Busca pelo registro de chave \"{key}\"\n")

                if found:
                    pag:Pages = readPage(treeFile, rrn)
                    offset:int = pag.offsets[pos]
                    rec:str = retrieveInfoDataFile(dataFile, offset)

                    logFile.write(f"{rec} ({len(rec)} bytes - offset {offset})\n\n")
                else:
                    logFile.write(f"Erro: registro nao encontrado!\n\n")

            case 'i':
                key = int(tasks[1].split("|")[0])
                found, rrn, pos = searchTree(treeFile, key, root)
                logFile.write(f"Insercao do registro de chave \"{key}\"\n")

                if found:
                    logFile.write(f"Erro: chave \"{key}\" já existente!\n\n")
                else:
                    offset, size = InsertInfoDataFile(dataFile, tasks[1])
                    root = insertionManager(treeFile, root, [(key, offset)])
                    writeTreeRoot(treeFile, root)
                    logFile.write(f"{tasks[1]} ({size} bytes - offset {offset})\n\n")

    dataFile.close()
    treeFile.close()
    operationFile.close()
    logFile.close()

def PrintTree() -> None:
    """
    Função principal para a impressão da árvore-B
    """

    try:
        # Acessa o arquivo de Árvore
        treeFile = open(TREE_FILE_PATH, 'r+b')

        # Acessa o arquivo de Log de Impressão
        logFile = open(LOG_PRINT_FILE_PATH, 'w', encoding="utf8")

    except OSError as e:
        print(e)
        exit()

    treeFile.seek(0)
    logFile.seek(0)
    root:int = readTreeRoot(treeFile)

    rrn:int = 0
    while not EOF(treeFile):
        pag:Pages = readPage(treeFile, rrn)
        text:str = f"Pagina {rrn}:\nChaves = {str(pag.keys)}\nOffsets = {str(pag.offsets)}\nFilhos = {str(pag.children)}\n"

        if rrn == root:
            logFile.write("- - - - - - - - - - Raiz  - - - - - - - - - -\n")        
            logFile.write(text)
            logFile.write("- - - - - - - - - - - - - - - - - - - - - - -\n\n")
        else:
            logFile.write(text + "\n")

        rrn += 1
    
    logFile.write(f"O índice \"{TREE_FILE_PATH}\" foi impresso com sucesso!")

    treeFile.close()
    logFile.close()
    
# Seleção da função e flag utilizada
if __name__ == '__main__':
    """
    Função principal para a execução do código
    """

    # Escrita sem as flags
    if len(sys.argv) <= 1:
        print("Insira a flag requerida, como -p, -c ou -e")

    # Execução da flag -p
    elif sys.argv[1] == '-p':
        PrintTree()

    # Escrita com a flag -e, mas sem o arquivo de operações
    elif sys.argv[1] == '-e' and len(sys.argv) <= 2:
        print("Insira o arquivo de operações")

    # Execução da flag -e
    elif sys.argv[1] == '-e' and len(sys.argv) > 2:
        ExecuteTree(sys.argv[2])

    elif sys.argv[1] == '-c':
        CreateTree()

    else:
        print("Algo deu errado na sintaxe das flags")