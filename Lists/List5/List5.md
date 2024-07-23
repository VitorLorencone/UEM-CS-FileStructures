# Lista 5

### Ex 1

Porque, para grandes arquivos, adicionamos um tempo de seeks que devem ser feitos a uma memória secundária, dessa forma, não apenas as comparações em RAM interferem, mas os seeks, as transferências e até a latência

### Ex 2

O primeiro é um match e o segundo preciso implementar

### Ex 3

- 6000 registros
- 600 registros por entrada
- 200 registros por saída
- Merge simples

- a) Será dividido em 10 partições, cada uma com 600 registros. Durante o merge, ***pode ser lido 60 registros por partição por vez***

- b) 10² = 100 seeks, porque cada partição deve ser lida 10 vezes e são 10 partições

- c) 10² + 10*2 + 6000/200 = 100 + 20 + 30 = 150 seeks totais, sendo 30 deles para a escrita final.

### Ex 4

Porque ele faz uso de uma maior capacidade do buffer de leitura, podendo realizar menos seeks durante a leitura (que é mais demorado que o processamento interna) e, embora aumente o tempo de transferência, ainda é superior

### Ex 5

- 800 MB
- Entrada de 4 MB
- Saída de 200 KB
- Dois passos 20 x 10 vias + 20 vias

- Fase 1: Temos 800/4 = 200 partições, ou seja, precisamos de 400 seeks para leitura e escrita e uma transferência total de 1.6 GB
- Merge 1: Temos 20 * 10² seeks = 2000 seeks e 800 MB de transferência
- Saída 1: Temos 800MB/200KB = 4000 seeks + 800 MB de transferência
- Merge 2: temos 20² * 10 seeks = 4000 seeks e 800 MB de Transferência
- Saída 2: Temos 800MB/200KB = 4000 seeks + 800 MB de transferência

### Ex 6

- 10 GB
- Entrada de 20 MB
- Saída de 250 KB
- Calcular em 1 e em 2 passos 25x20+25

Ainda não feito