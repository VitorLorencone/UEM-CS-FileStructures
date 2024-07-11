# Aula 2

### Arquivos

Um arquivo é uma estrutura lógica criada em uma memória secundária, que permite o armazenamento sequencial e PERMANENTE de dados

É uma sequência de bytes

**Arquivo físico:** Ponto de vista do ARMAZENAMENTO  
**Arquivo Lógico:** Ponto de vista da APLICAÇÃO

Um arquivo lógico está associado a um arquivo físico ou outros dispositivos I/O (Entrada e saída), como teclado (stdin) e o vídeo (stdout e stderr)

Operações com os arquivos não se preocupam com o armazenamento

Para os arquivos lógicos, cria-se um ponteiro R/W que indica a posição do próximo byte a ser lido/esrito

*Cada caractere é representado por 1 ou 2 bytes, de acordo com a codificação utilizada*

Cada arquivo lógico é adicionado em um **descritor**, ele é feito para associar um número inteiro a um arquivo. Cada linguagem tem o seu.

### Tipos de Arquivos

**Texto:** Sequência de strings já interpretadas como texto. Ele também é binário, mas já interpretado com alguma codificação.

**Binário:** Sequência de bytes (0x12 -> 2 dígitos hex). Cabe ao programador interpretar essa sequência.

### Opreações em Arquivos

- Criar
- Abrir
- Ler
- Escrever
- Movimentar o ponteiro
- Fechar

#### Criar e Abrir

***open(filename:str, mode:str) -> file object***  
arq = open("name", "wb")

***Modos de Abertura:*** "r" (read), "w" (write), "a" (append), "x" (exclusive), "r+", "w+", "rb", "wb", "x+b"...

Por padrão, usa-se a tag "t" para texto e "b" para binário.

**r:** Leitura, arquivo deve existir  
**w:** Escrita, pode criar o arquivo caso não existam  
**x:** Abre um novo arquivo para escrita, ele não deve existir  
**a:** Abre para escrita no final do arquivo, operações de reposicionar ponteiro serão ignoradas  
**t:** Modo texto  
**b:** Mode binário  
**+:** Permite leitura e escrita da tag inicial  

close(): Fecha o arquivo e encerra a associação entre arquivo físico e lógica. Muito importante, previne perda de dados.

def read(size) -> str  
- size = -1 => Ler arquivo todo

def readline(size) -> str  
- Lê até uma quebra de linha
- size indica quantidade máxima de caracteres

def readlines(hint) -> str  
- Retorna as linhas como uma lista de strings

def write(s) -> int
- Escreve a string s no arquivo

def writelines(lines) -> None
- Escreve um lista de strings

### Detecção EOF

EOF = End of File

Em python temos um retorno vazio para indicar o fim, como "" ou b""

### Posicionamento do Ponteiro

def seek(offset, whence) -> int
- Posiciona o ponteiro no offset calculado
- whence
  * = 0 -> A partir do início do arquivo, padrão
  * = 1 -> A partir da posição atual do ponteiro
  * = 2 -> A partir do fim do arquivo

def tell() -> int
- Retorna a posição atual do ponteiro de R/W

### Arquivos e S.O.

**Marcação de fim de linha:** 
- DOS/Windows usa dois bytes, decimal ASCII 1310 ou hex 0D0A
- Unix/Linus usa um byte, decimal ASCII 10 ou hex 0A
- \n é a representação de nova linha para todos os sistemas, apenas a marcação deles nos arquivos que muda.

### Arquivos Binários em Python

