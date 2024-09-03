# Importação para a leitura das flags
import sys

# Constantes
TREE_ORDER:int = 5

ROOT_SIZE_BYTES:int = 4
ELEMENT_SIZE_BYTES:int = 4
RRN_SIZE_BYTES = ELEMENT_SIZE_BYTES * (1 + 2*(TREE_ORDER-1) + TREE_ORDER)

# \xFF\xFF\xFF\xFF
NULL_VALUE_HEX:bytes = int.to_bytes(256**ELEMENT_SIZE_BYTES - 1, ELEMENT_SIZE_BYTES, byteorder="little")

HEADER_SIZE_BYTES:int = 4
RECORD_SIZE_BYTES:int = 2

DATA_FILE_PATH:str = 'games.dat'
TREE_FILE_PATH:str = 'btree.dat'
LOG_PRINT_FILE_PATH:str = 'log-impressao-' + DATA_FILE_PATH.split('.')[0] + '-ordem' + str(TREE_ORDER) + '.txt'
LOG_OP_FILE_PATH:str = 'log-op-teste-' + DATA_FILE_PATH.split('.')[0] + '-ordem' + str(TREE_ORDER) + '.txt'

class Pages:
    def __init__(self):
        self.numKeys:int = 0
        self.keys:list[int] = [-1]*(TREE_ORDER - 1)
        self.offsets:list[int] = [-1]*(TREE_ORDER - 1)
        self.children:[list[int]] = [-1]*TREE_ORDER

def readTreeRoot(tree)->int:
    tree.seek(0)
    ans:int = int.from_bytes(tree.read(ROOT_SIZE_BYTES), signed=True, byteorder="little")
    return ans

def writeTreeRoot(tree, root:int)->None:
    treeFile.seek(0)
    treeFile.write(int.to_bytes(root, ROOT_SIZE_BYTES, byteorder="little"))

def readPage(tree, rrn:int)->Pages:
    resp:Pages = Pages()
    byte_offset:int = rrn*RRN_SIZE_BYTES + ROOT_SIZE_BYTES
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
    byte_offset:int = rrn*RRN_SIZE_BYTES + ROOT_SIZE_BYTES
    tree.seek(byte_offset)

    tree.write(int.to_bytes(pag.numKeys, ELEMENT_SIZE_BYTES, byteorder="little"))
    for i in range(TREE_ORDER - 1):
        tree.write(int.to_bytes(pag.keys[i], ELEMENT_SIZE_BYTES, byteorder="little"))
    for i in range(TREE_ORDER - 1):
        tree.write(int.to_bytes(pag.offsets[i], ELEMENT_SIZE_BYTES, byteorder="little"))
    for i in range(TREE_ORDER):
        tree.write(int.to_bytes(pag.children[i], ELEMENT_SIZE_BYTES, byteorder="little"))

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

#def insertInPage(tree, key, childR, pag):

def CreateTree() -> None:
    try:
        # Acessa o arquivo de Dados
        dataFile = open(DATA_FILE_PATH, 'r+b')

        # Acessa o arquivo de Árvore
        treeFile = open(TREE_FILE_PATH, 'w+b')

    except OSError as e:
        print(e)
        exit()

    ROOT_RRN:int = -1
    writeTreeRoot(ROOT_RRN, treeFile)
    treeFile.write(int.to_bytes())

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
        operationFile = open(LOG_OP_FILE_PATH, 'w+b', encoding="utf8")

    except OSError as e:
        print(e)
        exit()

    dataFile.close()
    treeFile.close()

def PrintTree() -> None:
    try:
        # Acessa o arquivo de Dados
        dataFile = open(DATA_FILE_PATH, 'r+b')

        # Acessa o arquivo de Árvore
        treeFile = open(TREE_FILE_PATH, 'r+b')

        # Acessa o arquivo de Log de Impressão
        logFile = open(LOG_PRINT_FILE_PATH, 'w+b')

    except OSError as e:
        print(e)
        exit()

    dataFile.close()
    treeFile.close()
    
# Seleção da função e flag utilizada
if __name__ == '__main__':

    a = open("btree.dat", "r+b")
    print(searchTree(a, 20, 8))

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