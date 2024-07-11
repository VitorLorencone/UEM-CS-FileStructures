# Lista 1

Supondo um disco com as características abaixo, responda as questões a seguir.
- 8 superfícies 
- 4.096 trilhas/superfície 
- 110 setores/trilha 
- 512 bytes/setor 
- Velocidade de rotação = 5.400 RPM 
- Tempo médio de seek = 12 ms 
- Latência média = 5,6 ms 

## Principais Anotações
- Em um mesmo cilindro, temos apenas um seek e uma latência, mas o tempo de transferência deve ser para o número de bytes lidos.
- Em uma leitura sequencial, todos os registros estão dispostos em mesmas trilhas, logo, consideramos o tempo de transferência por trilha e um seek e uma latência para cada
- Em uma leitura aleatória, todos os registros estão separados aleatoriamente, dessa forma, precisamos do tempo de seek e latência para cada registro, além disso, devemos considearar o tempo de transferência POR REGISTRO, e não por trilha.
- Mesmo que o registro seja menor que o setor, a menor unidade possível de leitura do tempo de transfer é o do setor, logo, isso deve ser considerado para os cálculos.

### Ex 1

Nº de cilíndros = Nº de trilhas por superfície  
Logo, ***há 4096 cilindros.***

### Ex 2

512 B/setor -> 4 registros/Setor  
4 registros/Setor -> 440 registros/trilha  
Cada cilindro possui 8 trilhas -> 8 trilhas/cilindro  
8 trilhas/cilindro -> 3520 registro/cilindro  
Logo, precisamos de 80000/3520 = ***22.73 cilindros***

### Ex 3

Transfer time = tempo de 1 rotação = 1/90 = ***11.11ms***  
Isso é algo que eu já devo saber

### Ex 4

Vou precisar do tempo de seek, da latência e do transfer, logo: 11.11 + 5.6 + 12 = ***28.71ms***

### Ex 5

Vou precisar do tempo de seek, da latência e do tempo de transferência de um setor  
1 trilha possui 110 setores e leva 11.11 ms, logo, um setor leva 11.11/110 = 0.101 ms  
Enfim, 0.101 + 5.6 + 12 = ***17.701 ms***

### Ex 6

Precisamos, para cada uma, de um seek, um tempo de latência e o transfer de uma trilha, logo: (11.11 + 5.6 + 12)*110 = 3158.1 ms = ***3.1581 segundos***

### Ex 7

Como todas as trilhas de um cilindro podem ser lidas com um único seek e uma única latência, só precisamos considerar cada um deles uma única vez e o transfer de 8 trilhas, já que são mais informações, logo: 8*11.11 + 12 + 5.6 = ***106.48 ms***

### Ex 8 a)

Um arquivo de 80.000 registros com as trilhas aleatoriamente distribuidas pelo disco

Se o Arquivo está disposto de forma sequencial, então todos os registros foram gravados em mesmas trilhas

Dessa forma:

4 registros/setor -> 440 registros por trilha -> precisamos de 181.82 trilhas para armazenar todos.

Precisamos então do seek e latência para cada trilha, com o tempo de transferência por trilha, dessa forma:

(11.11 + 5.6 + 12) * 181.82 = 5220,05 ms = ***5,22005 segundos***

### Ex 8 b)

Agora, cada registro está em uma trilha diferente, dessa forma, vamos também considerar o tempo de transferência por setor, e não por trilha:

(0.101 + 5.6 + 12) * 80.000 = ***23.6 minutos***