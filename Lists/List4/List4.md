# Lista 4

### Ex 1

A fragmentação interna se refere ao processo de um pequeno espaço de dados dentro de um registro, podendo estar presente apenas em um campo, por exemplo.

A fragmentação externa se refere ao processo de um espaço restante de dados fora de um registro, podendo estar associado a um arquivo inteiro

A compactação, para a fragmentação externa, é muito útil, visto que ela reescreve o arquivo, removendo-se os espaços fragmentados, deixando os registros mais sólidos, mas requer um grande espaço em disco

Para a a compactação em fragmentação interna, ela não vai modificar os campos dos registros, dessa forma, ela não afeta uma fragmentação interna.

### Ex 2

Porque, em tamanho variável, é preciso guardar o byte offset dos próximos registros, além de que o espaço restante em um registro pode ser diferente do restante em outro, o que ocasiona situações em que queremos escolher o melhor espaço disponível, algo que não acontece na PED, já que todos são iguais.

### Ex 3

- **a)** 

Topo da PED -> 6

João... Pedro... Luiz... *-1 Paula... *3 *5

- **b)** 

Topo da PED -> 1

João... *6 Luiz... *-1 Paula... *3 *5

- **c)**

Topo da PED -> 6

João... Maria... Luiz... *-1 Paula... *3 *5

### Ex 4

Byte-offset // Tam do Registro  
28 // 28  
58 // 30  
150 // 123  
4 // 22  
90 // 58  

XX 22-reg1-/ 28-reg2-/ 30-reg3-/ 58-reg4-/ 123-reg5

#### ***FIRST FIT***

TOPO LED = -1

Remoção de 28, 150 e 90

TOPO LED = 90

XX 22-reg1-/ 28*-1 -1/ 30-reg3-/ 58* 150/ 123* 28

Inserção do registro 6 de 22 bytes

TOPO LED = 150

XX 22-reg1-/ 28* -1/ 30-reg3-/ 22-reg6-/ 123* 28

O registro é inserido no offset 90

#### ***BEST FIT***

TOPO LED = -1

Remoção de 28, 150 e 90

TOPO LED = 28

XX 22-reg1-/ 28* 90/ 30-reg3-/ 58* 150/ 123* -1

Inserção do registro 6 de 22 bytes

TOPO LED = 90

XX 22-reg1-/ 22-Reg6-/ 30-reg3-/ 58* 150/ 123* -1

O registro será inserido no offset 28

#### ***WORST FIT***

TOPO LED = -1

Remoção de 28, 150 e 90

TOPO LED = 150

XX 22-reg1-/ 28* -1/ 30-reg3-/ 58* 28/ 123* 90

Inserção do registro 6 de 22 bytes

TOPO LED = 90

XX 22-reg1-/ 28* -1/ 30-reg3-/ 58* 28/ 22-Reg6-

O registro será inserido no offset 150

### Ex 5

- a)

LEAD HEAD: -1

Cabeçalho... 21 Soares|... |60 Valdares|... |35 Martineli|... |54 Fonseca|... |45 Martins|...

Offset do Martins é 194

- b)

LEAD HEAD: 101

Cabeçalho... 21 Soares|... |60 Valdares|... |35 *-1tineli|... |54 Fonseca|... |45 Martins|...

- c)

LEAD HEAD: 39

Cabeçalho... 21 Soares|... |60 *101ares|... |35 *-1tineli|... |54 Fonseca|... |45 Martins|...

- d)

LEAD HEAD: 101

Cabeçalho... 21 Soares|... |60 Casale...\0|... |35 *-1tineli|... |54 Fonseca|... |45 Martins|...

Fragmentação interna de 28 bytes

- e)

LEAD HEAD: 101

Cabeçalho... 21 *-1res|... |60 Casale...\0|... |35 *16tineli|... |54 Fonseca|... |45 Martins|...

### Ex 6

- **BEST FIT**

- a)

LEAD HEAD: -1

Cabeçalho... 21 Soares|... |60 Valdares|... |35 Martineli|... |54 Fonseca|... |45 Martins|...

Offset do Martins é 194

- b)

LEAD HEAD: 101

Cabeçalho... 21 Soares|... |60 Valdares|... |35 *-1tineli|... |54 Fonseca|... |45 Martins|...

- c)

LEAD HEAD: 101

Cabeçalho... 21 Soares|... |60 *-1dares|... |35 *39tineli|... |54 Fonseca|... |45 Martins|...

- d)

LEAD HEAD: 39

Cabeçalho... 21 Soares|... |60 *-1dares|... |35 Casale|...\0|... |54 Fonseca|... |45 Martins|...

- e)

LEAD HEAD: 16

Cabeçalho... 21 *39res|... |60 *-1dares|... |35 Casale|...\0|... |54 Fonseca|... |45 Martins|...

- **FIRST FIT**

- a)

LEAD HEAD: -1

Cabeçalho... 21 Soares|... |60 Valdares|... |35 Martineli|... |54 Fonseca|... |45 Martins|...

Offset do Martins é 194

- b)

LEAD HEAD: 101

Cabeçalho... 21 Soares|... |60 Valdares|... |35 *-1tineli|... |54 Fonseca|... |45 Martins|...

- c)

LEAD HEAD: 39

Cabeçalho... 21 Soares|... |60 *101ares|... |35 *-1tineli|... |54 Fonseca|... |45 Martins|...

- d)

LEAD HEAD: 101

Cabeçalho... 21 Soares|... |60 Casale...|\0|... |35 *-1tineli|... |54 Fonseca|... |45 Martins|...

- e)

LEAD HEAD: 16

Cabeçalho... 21 *101es|... |60 Casale...|\0|... |35 *-1tineli|... |54 Fonseca|... |45 Martins|...

### Ex 7

Ainda não feito

### Ex 8

Porque a worst fit, embora mais rápida para inserir, já que precisa exercutar apenas uma comparação, é a que mais gera fragmentação interna, já que ela aloca o MAIOR espaço, para qualquer que seja o tamanho do registro. Dessa forma, worst fit é usado quando o espaço restante volta para a LED

### EX 9

O gerenciamento por PED ou LED é corrompido com a ordenação do arquivo, já que vai modificar todos os RRNs ou byte-offsets, que não pode ser corrigido na PED/LED

### Ex 10

Keysort fará, por meio da ordenação interna, uma lista ordenada das chaves com seu byte offset:

ANG - 167  
COL - 211  
DGC - 256  
LON - 32  
RCA - 77  
WAR - 132  

Agora, com as chaves ordenadas internamentes, um novo arquivo é escrito, seguindo essa ordem, de modo que:

ANG - 32  
COL - 76  
DGC - 121  
LON - 177  
RCA - 222  
WAR - 277