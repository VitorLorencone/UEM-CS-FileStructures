# Aula 4

### Acesso a registros

Registro é a unidade de informação

**Métodos de Indexação**
- 1º registro, 2º registro...
- Chave = "Silva"...

**Chave primária:** Identifica UNICAMENTE cada registro, não existem repetições.

**Chave Secundária:** Pode repetir em 2 ou mais registros, não há unicidade.

Conceitos comuns em Bancos de Dados

### Busca Sequencial

Ler o arquivo sequencialmente, registro por registro, procurando-se a chave

Tem complexidade de tempo O(n) em que n representa o número de regitros

Podemos reduzir o número de seeks se decidirmos carregar vários blocos de registros por vez na RAM, diminuindo o tempo de busca em memória secundária

Usar blocos como organização física e de melhor desempenho

Leituras físicas demoram mais que leituras em RAM, dessa forma, embora a leitura por blocos também tenha tempo linear, o número de seeks é muito menor e, consequentemente, a operação é mais rápida

É importante que o bloco seja múltiplo do tamanho do cluster suportado

### Acesso Direto

Um registro é acessado pelo seu endereço

Ótimo para registros de tamanho fixo, mas que não são normalmente tão bons.

Custo O(1), porque simplesmente acessa

São marcados por uma ordem de registros RRN (Relative Record Number)

Começa do RRN 0

offset = RRN * tamanho do registro + tamanho do cabeçalho

### Header

É um registro de cabeçalho, normalmente pode ser utilizado para indicar o número total de registros, tamanho dos registros, por exemplo

Enfim, qualquer variável que se queira armazenar de modo permanente