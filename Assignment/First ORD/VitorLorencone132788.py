""" 
Aluno: Vitor Madeira Lorençone
RA: 132788
Profa: Valeria Delisandra Feltrim

Trabalho de gerenciamento de registros de um arquivo dados.dat, usando um arquivo de operações

Minha aplicação gera um ARQUIVO DE SAÍDA como log de execução, então essas informações não serão mostradas no terminal, mas sim
no arquivo log.txt, constanto todas as últimas operações realizadas

Execute por 'python VitorLorencone132788.py -p' ou 'python VitorLorencone132788.py -e arquivo_operacoes.txt', por exemplo.

Mudanças dessa versão do trabalho para a anterior:
1. Mudei praticamente TODOS os nomes de variáveis, porque estava muito confuso;
2. Adicionei diversas funções menores, "quebrando" o problema em outros menores e reciclando mais código, que não era feito antes;
3. Adicionei a classe RecordInfo para simplificar a escrita e leitura do código;
4. Correção do problema de INSERÇÃO no arquivo e na LED, que antes estava incorreto, apenas a busca e remoção funcionavam.

É importante ressaltar que toda estrutura, organização mental, método de coleta de flags e 
estratégias de execução são as mesmas da versão anterior!!

Coisas que eu quero conversar na apresentação do trabalho:
1. Questão da fragmentação externa que ocorre quando há uma sobra muito pequena de espaço depois da inserção.
Como você fez para identificar onde acabava um registro e começava o outro, sabendo que tinha uma fragmentação no meio deles?
OBS: O jeito que eu fiz foi incorporando essa fragmentação no novo registro escrito (veja na linha 283, principalmente)
2. Qual o melhor jeito de identificar e executar as flags?? Não acho que o jeito que eu fiz foi o melhor

Adorei o trabalho, professora!! Foi bem desafiador e recompensador na questão de aprendizado. 
"""

# Importação para a leitura das flags
import sys

# Constantes
DATA_FILE_PATH:str = 'dados.dat'
LOG_FILE_PATH:str = 'log.txt'
LED_SIZE_BYTES:int = 4
RECORD_SIZE_BYTES:int = 2
MIN_LED_LEFTOVER_BYTES:int = 15
NULL_LED_VALUE_HEX:bytes = int.to_bytes(256**LED_SIZE_BYTES - 1, LED_SIZE_BYTES)

class RecordInfo:
    """
    Classe que guarda as duas informações importantes de um registro: Seu offset no arquivo e seu tamanho em bytes
    """

    size:int
    offset:int

    def __init__(self, offset:int = -1, size:int = -1):
        self.size = size
        self.offset = offset

    def __str__(self):
        return f'[size: {self.size}, offset: {self.offset}]'

    def __repr__(self):
        return f'[size: {self.size}, offset: {self.offset}]'

    def isNull(self) -> bool:
        """
        Função que retorna True se o registro da LED é nulo, ou seja, se chegamos ao final
        """

        return self.size == -1 or self.offset == -1
        
def main(arg:str) -> None:
    """
    Função principal de execução
    """

    try:
        # Acessa o arquivo de Dados
        dataFile = open(DATA_FILE_PATH, 'r+b')

        # Acessa o arquivo de Log
        logFile = open(LOG_FILE_PATH, 'w', encoding="utf8")

        # Acessa o arquivo de operações, se necessário.
        if arg != '-p':
            operationFile = open(arg, 'r', encoding="utf8")

    except OSError as e:
        print(e)
        exit()

    def EOF() -> bool:
        """
        Função que retorna True se o ponteiro de L/E chegou ao fim do arquivo
        """

        currentOffset = dataFile.tell()
        dataFile.seek(0,2)

        endOffset = dataFile.tell()
        dataFile.seek(currentOffset)

        return currentOffset == endOffset

    def readFields(offset:int, size:int) -> list[str]:
        """
        Função que lê os campos de um registro de offset: *offset* e tamanho: *size* e retorna todos em uma lista de strings
        """

        dataFile.seek(offset) # Coloca o ponteiro no registro requerido

        rawField:bytes = dataFile.read(size)

        if int.to_bytes(rawField[0]) == b'*': # Verifica se o registro foi deletado
            return []

        fields:list[str] = rawField.decode().split('|') # Recupera todos os campos e aloca eles em uma lista
        fields.pop() # Remove o último campo vazio
        return fields

    def findRecord(primaryKey:str) -> RecordInfo:
        """
        Função que realiza uma busca sequencial pelo arquivo para encontrar e retornar o registro de uma chave primária: *primaryKey*.
        """

        dataFile.seek(LED_SIZE_BYTES) # Para fixar o ponteiro no começo do arquivo

        while not EOF(): # Verifica se chegamos no fim do arquivo

            recordSize:int = int.from_bytes(dataFile.read(RECORD_SIZE_BYTES), signed = True) # Lê o tamanho do registro
            recordOffset:int = dataFile.tell() # Lê o offset do registro
            fields:list[str] = readFields(recordOffset, recordSize) # Lê os campos do registro

            if fields == []: # Verifica se o registro não é inválido, tipo um registro removido
                continue

            if fields[0] == primaryKey: # Verfica se encontrou a chave procurada
                return RecordInfo(recordOffset - RECORD_SIZE_BYTES, recordSize) # Retorna as informações do Registro encontrado

        return RecordInfo() # Registro não existe

    def getLedHead() -> RecordInfo:
        """
        Retorna o registro da cabeça da LED, ou seja, onde está o próximo offset e o tamanho desse primeiro espaço
        """

        dataFile.seek(0)
        ledOffset = int.from_bytes(dataFile.read(LED_SIZE_BYTES), signed = True) # Recupera o offset do próximo espaço da LED
        
        if ledOffset == -1:
            return RecordInfo()

        dataFile.seek(ledOffset)
        ledSize = int.from_bytes(dataFile.read(RECORD_SIZE_BYTES), signed = True) # Recupera o tamanho do primeiro espaço vazio da LED

        return RecordInfo(ledOffset, ledSize)

    def getNextLed(currentLedOffset:int) -> RecordInfo:
        """
        Função que retorna o próximo espaço da LED dado um offset já conhecido (como o da cabeça da LED): *currentLedOffset*
        Ótima função para navegar por todos os espaços da LED recuperando espaço e a referência do próximo espaço
        """
        
        if currentLedOffset == -1:
            return RecordInfo()
        
        dataFile.seek(currentLedOffset + RECORD_SIZE_BYTES + 1) # Ignora o tamanho do registro e o '*'
        nextLedOffset:int = int.from_bytes(dataFile.read(LED_SIZE_BYTES), signed = True) # Recupera o próximo offset

        if nextLedOffset != -1:
            dataFile.seek(nextLedOffset)
            nextLedSize:int = int.from_bytes(dataFile.read(RECORD_SIZE_BYTES), signed = True) # Recupera o próximo tamanho
        else:
            return RecordInfo()

        return RecordInfo(nextLedOffset, nextLedSize)

    def updateLED(value:RecordInfo) -> None:
        """
        Função que atualiza a LED, ou seja, adiciona um novo espaço vazio *value* e ordena os espaços necessários
        """
        # Essa função trabalha com duas posições da LED já conhecidas, para inserir entre elas, antes da primeira ou depois da última
        currentLed:RecordInfo = getLedHead()
        previousLed:RecordInfo = RecordInfo(0, 0)

        while value.size < currentLed.size: # Procura o local correto de inserção seguindo o padrão Worst Fit
            previousLed = currentLed
            currentLed = getNextLed(currentLed.offset)

        # Realiza a inserção, corrigindo todos os espaços da LED em ordem
        dataFile.seek(previousLed.offset)
        if previousLed.size > 0:
            dataFile.write(int.to_bytes(previousLed.size, RECORD_SIZE_BYTES))
            dataFile.write(b'*')
        dataFile.write(int.to_bytes(value.offset, LED_SIZE_BYTES))

        dataFile.seek(value.offset)
        dataFile.write(int.to_bytes(value.size, RECORD_SIZE_BYTES))
        dataFile.write(b'*')
        if not currentLed.isNull():
            dataFile.write(int.to_bytes(currentLed.offset, LED_SIZE_BYTES))
        else:
            dataFile.write(NULL_LED_VALUE_HEX)

    def searchOperation(primaryKey:str) -> None:
        """
        Função que executa por trás do comando 'b', ele busca um registro com chave primária *primaryKey*
        """

        recordInfo:RecordInfo = findRecord(primaryKey) # Realiza a busca sequencial do registro

        if recordInfo.isNull():
            logFile.write(f'Busca pelo registro de chave "{primaryKey}"\n')
            logFile.write(f'Erro: Registro não encontrado\n\n')
            return None  

        dataFile.seek(recordInfo.offset + RECORD_SIZE_BYTES)
        recordContent:str = dataFile.read(recordInfo.size).decode() # Recupera o conteúdo do registro

        # Imprime os resultados em um arquivo de Log
        logFile.write(f'Busca pelo registro de chave "{primaryKey}"\n')
        logFile.write(f'{recordContent} ({recordInfo.size} bytes)\n')
        logFile.write(f'Local: offset = {recordInfo.offset} bytes ({hex(recordInfo.offset)} bytes)\n\n')

    def removeOperation(primaryKey:str) -> None:
        """
        Função que executa por trás do comando 'r', ela remove um registro com chave primária *primaryKey*
        """

        record = findRecord(primaryKey) # Procura o registro

        if record.isNull():
            logFile.write(f'Remoção do registro de chave "{primaryKey}"\n')
            logFile.write(f'Erro: Registro não encontrado\n\n')
            return None

        updateLED(record) # Realiza a inserção do registro removido na LED

        # Imprime os resultados em um arquivo de Log
        logFile.write(f'Remoção do registro de chave "{primaryKey}"\n')
        logFile.write(f'Registro removido! ({record.size} bytes)\n')
        logFile.write(f'Local: offset = {record.offset} bytes ({hex(record.offset)})\n\n')

    def insertOperation(recordContent:str) -> None:
        """
        Função que executa por trás do comando 'i', ela insere um registro *recordContent*
        """

        primaryKey:str = recordContent.split('|')[0] # Encontra a chave primária do registro
        record:RecordInfo = RecordInfo(-1, len(recordContent.encode()))
        ledHead:RecordInfo = getLedHead() # Salva o valor atual da cabeça da LED

        if record.size > ledHead.size: # Verifica se o arquivo deve ser inserido no final
            dataFile.seek(0,2) # final do arquivo
            dataFile.write(int.to_bytes(record.size, RECORD_SIZE_BYTES))
            dataFile.write(recordContent.encode())

            logFile.write(f'Inserção do registro de chave "{primaryKey}" ({record.size} bytes)\n')
            logFile.write(f'Local: fim do arquivo\n\n')

            return None

        leftoverBytes:int = ledHead.size - record.size # Calcula a sobra de espaço

        # Passa a LED em um valor, já que o primeiro será usado para inserção
        nextLedOffset:int = getNextLed(ledHead.offset).offset
        dataFile.seek(0)
        if nextLedOffset == -1:
            dataFile.write(NULL_LED_VALUE_HEX)
        else:
            dataFile.write(int.to_bytes(nextLedOffset, LED_SIZE_BYTES))

        dataFile.seek(ledHead.offset)

        if leftoverBytes >= MIN_LED_LEFTOVER_BYTES:
            # Inserção em que o espaço restante pode ser aproveitado
            dataFile.write(int.to_bytes(record.size, RECORD_SIZE_BYTES))
            dataFile.write(recordContent.encode())

            leftoverBytes -= RECORD_SIZE_BYTES
            leftoverRecord = RecordInfo(dataFile.tell(), leftoverBytes)

            # Atualiza a LED com o novo espaço vazio
            updateLED(leftoverRecord)

        else:
            # Inserção em que o espaço que sobra não pode ser aproveitado, logo, não precisa atualizar a LED
            dataFile.write(int.to_bytes(ledHead.size, RECORD_SIZE_BYTES))
            dataFile.write(recordContent.encode().ljust(ledHead.size, b'\x20'))

            leftoverBytes = 0

        # Imprime os resultados em um arquivo de Log
        logFile.write(f'Inserção do registro de chave "{primaryKey}" ({record.size} bytes)\n')

        if leftoverBytes == 0:
            logFile.write(f'Tamanho do espaço reutilizado: {ledHead.size} bytes\n')
        else:
            logFile.write(f'Tamanho do espaço reutilizado: {ledHead.size} bytes (Sobra de {leftoverBytes} bytes)\n')
        
        logFile.write(f'Local: offset = {ledHead.offset} bytes ({hex(ledHead.offset)})\n\n')

    # Verificação do tipo de execução necessária

    # Execução da flag -p
    if arg == '-p':
        logFile.write(f'LED -> ')
        countFreeSpaces:int = 0
        ledInfo:RecordInfo = getLedHead()

        while not ledInfo.isNull():
            countFreeSpaces += 1
            logFile.write(f'[offset: {ledInfo.offset}, tam: {ledInfo.size}] -> ')
            ledInfo = getNextLed(ledInfo.offset)

        logFile.write(f'[offset: -1]\n')
        logFile.write(f'Total: {countFreeSpaces} espaços disponíveis')

    # Execução da Flag -e
    else:
        # Coloca em memória todas as operações e seus argumentos
        operationInfo:list[list[str]] = []

        for i in operationFile.readlines():
            i = i.replace('\n', '')
            operationInfo.append([i[0], i[2:]])

        # Fecha o arquivo de operações
        operationFile.close()

        # Execução de cada operação, em ordem
        for tasks in operationInfo:
            match(tasks[0]):
                case 'b':
                    searchOperation(tasks[1])
                case 'i':
                    insertOperation(tasks[1])
                case 'r':
                    removeOperation(tasks[1])

    print(f"Arquivo {LOG_FILE_PATH} gerado com o resultado do código executado")

    # Fecha os arquivos
    logFile.close()
    dataFile.close()

# Seleção da função e flag utilizada
if __name__ == '__main__':

    # Escrita sem as flags
    if len(sys.argv) <= 1:
        print("Insira a flag requerida, como -p ou -e [Arquivo de Operações]")

    # Execução da flag -p
    elif sys.argv[1] == '-p':
        main('-p')

    # Escrita com a flag -e, mas sem o arquivo de operações
    elif sys.argv[1] == '-e' and len(sys.argv) <= 2:
        print("Insira o arquivo de operações")

    # Execução da flag -e
    elif sys.argv[1] == '-e' and len(sys.argv) > 2:
        main(sys.argv[2])

    else:
        print("Algo deu errado na sintaxe das flags")