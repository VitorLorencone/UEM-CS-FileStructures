# Importação para a leitura das flags
import sys

# Constantes
# Ordem da Árvore B
TREE_ORDER:int = 5

# Informações sobre tamanho em bytes dos dados da árvore
ROOT_SIZE_BYTES:int = 4
ELEMENT_SIZE_BYTES:int = 4
PAGE_SIZE_BYTES = ELEMENT_SIZE_BYTES * (1 + 2*(TREE_ORDER-1) + TREE_ORDER)

# Constante que representa o byte nulo
# \xFF\xFF\xFF\xFF
NULL_VALUE_HEX:bytes = int.to_bytes(256**ELEMENT_SIZE_BYTES - 1, ELEMENT_SIZE_BYTES, byteorder="little")

# Constantes que representam as informações do arquivo de dados
HEADER_SIZE_BYTES:int = 4
RECORD_SIZE_BYTES:int = 2

# Caminho para cada arquivo
DATA_FILE_PATH:str = 'games.dat'
TREE_FILE_PATH:str = 'btree.dat'
LOG_PRINT_FILE_PATH:str = 'log-impressao-' + DATA_FILE_PATH.split('.')[0] + '-ordem' + str(TREE_ORDER) + '.txt'
LOG_OP_FILE_PATH:str = 'log-operations-' + DATA_FILE_PATH.split('.')[0] + '-ordem' + str(TREE_ORDER) + '.txt'

class Pages:
    def __init__(self):
        self.numKeys:int = 0
        self.keys:list[int] = [-1]*(TREE_ORDER - 1)
        self.offsets:list[int] = [-1]*(TREE_ORDER - 1)
        self.children:[list[int]] = [-1]*TREE_ORDER
    
    def isFull(self):
        return self.numKeys >= TREE_ORDER - 1

def EOF(file)->bool:
    currentOffset:int = file.tell()
    file.seek(0, 2)
    eofOffset:int = file.tell()
    file.seek(currentOffset)
    return currentOffset == eofOffset

def readTreeRoot(tree)->int:
    tree.seek(0)
    ans:int = int.from_bytes(tree.read(ROOT_SIZE_BYTES), signed=True, byteorder="little")
    return ans

def writeTreeRoot(tree, root:int)->None:
    tree.seek(0)
    tree.write(int.to_bytes(root, ROOT_SIZE_BYTES, signed=True, byteorder="little"))

def readPage(tree, rrn:int)->Pages:
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
    pos:int = 0
    while pos < pag.numKeys and key > pag.keys[pos]:
        pos += 1
    if pos < pag.numKeys and key == pag.keys[pos]:
        return True, pos
    else:
        return False, pos

def searchTree(tree, key:int, rrn:int):
    if rrn == -1:
        return False, -1, -1
    else:
        pag:Pages = readPage(tree, rrn)
        found, pos = searchPage(key, pag)

        if found is True:
            return True, rrn, pos
        else:
            return searchTree(tree, key, pag.children[pos])

def insertInPage(tree, key:int, childR:int, pag:Pages):
    if pag.isFull():
        pag.keys.append(-1)
        #pag.offsets.push(-1)
        pag.children.append(-1)
    
    i:int = pag.numKeys
    while i > 0 and key < pag.keys[i-1]:
        pag.keys[i] = pag.keys[i-1]
        pag.children[i+1] = pag.children[i]
        i -= 1
    
    pag.keys[i] = key
    pag.children[i+1] = childR
    pag.numKeys += 1

def nextRRN(tree)->int:
    tree.seek(0, 2) # Fim do arquivo
    offset:int = seek.tell()
    return (offset - ROOT_SIZE_BYTES) // PAGE_SIZE_BYTES

def divide(tree, key:int, childR:int, pag:Pages):
    insertInPage(tree, key, childR, pag)

    middle:int = TREE_ORDER//2
    promKey:int = pag.keys[middle]
    promChildR:int = nextRRN()

    currentPage:Pages = Pages()
    currentPage.numKeys = middle
    currentPage.keys = pag.keys[:middle] + (TREE_ORDER - 1 - middle)*[-1]
    currentPage.children = pag.children[:middle+1] + (TREE_ORDER - 1 - middle)*[-1]

    newPage:Pages = Pages()
    newPage.numKeys = TREE_ORDER-1-middle
    newPage.keys = pag.keys[middle+1:] + (TREE_ORDER - 1 - middle)*[-1]
    newPage.children = pag.children[middle+1:] + (TREE_ORDER - middle)*[-1]

    return promKey, promChildR, currentPage, newPage

def insertInTree(tree, key, rrn):
    if rrn == -1:
        promKey:int = key
        promChildR:int = -1
        return promKey, promChildR, True
    else:
        pag:Pages = readPage(tree, rrn)
        found, pos = searchPage(key, pag)

    if found == True:
        print("ERROR: Duplicated Key")
        tree.close()
        exit()
    
    promKey, promChildR, promo = insertInTree(tree, key, pag.children[pos])

    if promo == False:
        return -1, -1, False
    else:
        if not pag.isFull():
            insertInPage(tree, promKey, promChildR, pag)
            writePage(tree, rrn, pag)
            return -1, -1, False
        else:
            promKey, promChildR, pag, newPag = divide(tree, promKey, promChildR, pag)
            writePage(tree, rrn, pag)
            writePage(tree, promChildR, newPag)
            return promKey, promChildR, True

def insertionManager(tree, root:int, insertionKeys:list[int]):
    for key in insertionKeys:
        promKey, promChildR, prom = insertInTree(tree, key, root)

        if prom == True:
            newPage:Pages = Pages()
            newPage.keys[0] = promKey
            newPage.children[0] = root
            newPage.children[1] = promChildR
            newPage.numKeys += 1

            newRRN:int = nextRRN(tree)
            writePage(tree, newRRN, newPage)
            root = newRRN
    
    return root

def CreateTree() -> None:
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

    insertKeyList:list[int] = []

    while not EOF(dataFile):
        recSize:int = int.from_bytes(dataFile.read(RECORD_SIZE_BYTES), signed=True, byteorder="little")
        rawField:bytes = dataFile.read(recSize)
        fields:list[str] = rawField.decode().split("|")

        insertKeyList.append(int(fields[0]))
    
    root = insertionManager(treeFile, root, insertKeyList)
    writeTreeRoot(treeFile, root)

    dataFile.close()
    treeFile.close()

def ExecuteTree(arg:str) -> None:
    try:
        # Acessa o arquivo de Dados
        dataFile = open(DATA_FILE_PATH, 'r+b')

        # Acessa o arquivo de Árvore
        treeFile = open(TREE_FILE_PATH, 'r+b')

        # Acessa o arquivo de Operações
        operationFile = open(arg, 'r', encoding="utf8")

        # Acessa o arquivo de Log de Operações
        logFile = open(LOG_OP_FILE_PATH, 'w', encoding="utf8")

    except OSError as e:
        print(e)
        exit()

    dataFile.close()
    treeFile.close()

def PrintTree() -> None:
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

    dataFile = open(DATA_FILE_PATH, 'r+b')
    treeFile = open(TREE_FILE_PATH, 'r+b')

    root:int = readTreeRoot(treeFile)
    if root == 0:
        writeTreeRoot(treeFile, root)
        writePage(treeFile, 0, Pages())

    insertKeyList:list[int] = [188]

    root = insertionManager(treeFile, root, insertKeyList)
    writeTreeRoot(treeFile, root)

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