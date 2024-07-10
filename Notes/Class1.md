# Aula 1

### Hierarquia de memória

***Mais velocidade de acesso e custo alto***

- Registradores 
- Memória Cache
- Memória Primária (RAM)
- Memória Secundária (HD, SSD...)

***Mais capacidade de armazenamento e custo reduzido***

Memória RAM é **Volátil**, porque não armazena suas informações quando não há energia.

Memória ROM, como a maioria das secundárias é **não Volátil**, porque armazenam informações de forma permanente.  

**Arquivos** são estruturas lógicas que armazenam informações em uma memória secundária.

### Memória Secundária

Mesmo que não pareça, fitas magnéticas ainda são muito usadas, elas armazenam centenas de TB de capacidade e duram muitas décadas, além de serem pequenas e muito baratas.

Memórias eletrônicas costuma ser mais rápidas que memórias que dependem de processos mecânicos.

Fitas são dispostivos sequenciais, enquanto HD's e SSDS são dispositivos de acesso aleatório

***Discos Magnéticos***

- Hard Disks
  * Alta Capacidade
  * Lento em relação à RAM
- Floppy Disks (Disquetes)
  * Baixa capacidade
  * Baixo custo
  * Mais lento que o HD
- ZIP Disks (Prévia do Cartão de Memória)
  * Muita baixa capacidade
  * Mais lendo que os Disquetes

Todos eles são compostos de pratos eletromagnéticos são lidos e escritos por um cabeçote.

A cabeça é sempre parada, o que gira é o prato

Trilha é uma divisão do disco, composta por círculos concêntricos ao disco principal.

O pulso eletromagnético muda a polaridade de pequenas regiões no disco, sendo essa diferença de polaridade as responsáveis por diferir os bits 0 e 1.

Cada disco é dividido em Superfícies, que são divididas em trilhas, que por sua vez são divididas em setores

Um setor é a menor parte endereçável (512B até 4KB)

Na leitura, os dados dos setores são copiados em um *buffer* e, no buffer, temos o byte requisitado.

A setorização é feita de forma física pelo produtor do disco.

O conjunto de trilhas (circulos concentricos) de discos diferentes dispostos um acima do outro é chamado de cilindro

As informações em mesmo cilindro podem ser acessadas sem tempo adicional, porque o seek é mais rápido.

Número de Trilhas por superfície = Número de Cilindros

#### Ex1
- 512 bytes/setor
- 63 setores/trilha
- 16 trilhas/cilindro
- 4080 cilindros

Quantos cilindros são necessários para armazenar um 
arquivo de 50.000 registros de 256 bytes cada?

*Total de bytes = 50000 * 256 = 12800000 bytes*  
*512 bytes/setor => 512 * 63 = 32256 bytes/trilha*  
*32256 bytes/trilha => 32256*16 = 516096 bytes/cilindro*  
*Logo, são necessários 12800000/516096 = **24.8 cilndros***

### Clusters

Método que o S.O. usa para enxergar a organização do disco rígido.

Um cluster associa um endereço lógico a uma sequência de bytes de uma posição do disco rígido

Um arquivo é uma série de clusters

O Gerenciador de arquivos usa a tabela de alocação de arquivos (FAT) para mapear a posição dos clusters

Um cluster é um conjunto de setores, que são todos endereçados de maneira lógica na FAT

Tamanho do setor -> Depende do fabricante da memória secundária  
Tamanho do cluster -> Depende do fabricante do S.O.

Cada cluster serve para UM ÚNICO arquivo, então todo arquivo tem um tamanho mínimo de memória, definido pelo tamanho do cluster

Tamanho do cluster varia entre 512B até 64Kb

Pode, então, existir um arquivo de 1 byte, mas que ocupa 4kb na memória, porque ela deve ser reservada para o cluster que tem esse tamanho mínimo

### Custo de Acesso ao Disco

Dividido em 3:

- **Seek**: Tempo para mover o cabeçote até a trilha correta.
- **Latency**: Tempo para a rotação do disco fazer com que a cabeça esteja no setor correto. Ou seja, depende do RPM do disco.
- **Transfer**: Tempo para a leitura de um byte ser transferido para o buffer de leitura.

Seek time

- Estima-se que, em média, o tempo de seek é 1/3 do total de trilhas
- Entre 5 e 10 ms
- Buscas em mesmo cilindro possuem seek reduzido, porque o cabeçote já estará posicionado

Latency time

- Tempo médio é a metade do tempo de uma rotação
- Entre 8 e 4 ms

Transfer time

- Normalmente, o tempo para transferir uma trilha inteira é o tempo de uma rotação (é o que deve acontecer)
- (n°bytes tranferidos/n°bytes da trilha) * tempo de rotação
- Tempo de transferência de 1 KB em um disco com 32 setores de 512
 bytes por trilha (16.384b) e tempo de rotação de 8,2ms:
   * Transfer = 1024/16384 * 8.2 = 0.51ms

#### Ex2

Determinar o tempo necessário para ler um arquivo com 
40.000 registros de 256 bytes cada um, de maneira de acesso sequencial e depois aleatória

Tempo médio de seek 13 ms  
Tempo de latência 8,3 ms  
Tempo de transferência 16,7 ms/trilha ou 1.229 bytes/ms  
Bytes por setor 512  
Setores por trilha 100  
Trilhas por cilindro 12  
Trilhas por superfície 1.748  
Tamanho do cluster 10 setores (5.120 bytes)  

40000 registros de 256 bytes = 10240000 bytes  
51200 bytes por trilha  
614400 bytes por cilindro  
20 registros por cluster
2000 clusters para todo o arquivo  
Cada trilha possui 10 clusters  
Logo, são necessárias 200 trilhas

*Sequencial:* No pior caso, todas as 200 trilhas NÃO ESTÃO no mesmo cilindro, dessa forma, temos um tempo de seek para cada, um tempo de latência e um tempo de transferência  
Tempo = (13ms + 8.3ms + 16.7ms) * 200 = 7.6 segundos

Ou seja, no sequencial, todos os registros estão na mesma trilha

*Aleatória:* No pior caso, cada registro está em um cluster e trilha diferentes. Além disso, o tempo de transferência por cluster é 1.67ms, dessa forma:  
Tempo = (13ms + 8.3ms + 1.67ms) * 40.000 = 918.8 segundos

Ou seja, no aleatório, todos os registros não precisam estar na mesma trilha.

### SSD

Solid-State-Driver: Feito de forma eletrônica, com armazenamento em módulos de memória Flash

Por conta do uso eletrônico, não tem tempo de seek nem procura rotacional, mas tem a latência entre as operações e o tempo de transferência.

A menor unidade de medida é a página, variando de 2KB até 16KB. As páginas são armazenadas em blocos de 256KB até 4MB

Por conta de limitações eletrônicas de sobrescritas (que são muito reduzidas em HD), as páginas não podem ser apagadas quando quiser. Elas devem ser marcadas como mortas e apenas alteradas quando a memória flash encher e todo seu conteúdo útil for repassado para outro bloco.

As operações de escritas são distribuídas, para que o tempo de vida de cada uma esteja muito similar

Memórias secundárias são sempre o gargalo do sistema, ou seja, o limitante para a conclusão de uma operação que depende do acesso à memória!!!!!