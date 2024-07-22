# Aula 6

É mais comum fazermos pesquisas por:
- Qual registro armazena os dados de João? (SIM!!)
- Qual registro armazena os dados do rrn 134? (NÃO!!!)

Ou seja, busca por **CHAVE**

### Busca por chave

- Em um arquivo DESORDENADO, ela é sequencial
- Podemos substituir a busca sequencial por uma busca ordenada, ou seja, busca binária

### Busca Binária

- Requer a ORDENAÇÃO
- REQUER TAMANHOS FIXOS
- Complexidade O(lg(n))
- Existe um custo para garantir a ORDENAÇÃO e MANTER o arquivo assim.
- A cada Inserção o Arquivo deve ser REORDENADO e escrito em um novo arquivo, necessitando do dobro da memória
- Com a ordenação interna, ela não aumenta a memória, mas aumenta a complexidade e não é útil para arquivos grandes
- Minimiza o acesso ao disco
- É o melhor tipo, mas o mais complexo
- Manter um arquivo ordenado é custoso para inserções frequentes
- Só é viável a ordenação interna em arquivos pequenos, porque senão requer muitas chamadas do buffer, que não consegue carregar tudo

### Keysort

- Para ordenação interna
- Limitado pela RAM

1. Leia o arquivo e coloque em uma lista as CHAVES e os RESPECTIVOS RRN's/byte-offset de cada registro (Ou seja, leitura sequencial)
2. Ordene usando qualquer algoritmo de ordenação interna
3. Reescreva (em outro arquivo) o resultado

- A lista em memória RAM deve ser uma tupla de valores, porque precisa da chave e do rrn ou offset
- É ordenação interna porque não se faz acesso ao disco
- Cada registro será lido duas vezes para a escrita final
- Ou seja, é uma ordenação O(n)

### Índices

- Faz também uma lista de chaves, mas a usa como um índice para o arquivo de registros
- Grave o índice em um arquivo de índices à parte
- Faça busca binária APENAS no Índice
- Não tem restrição de tamanho fixo para os dados!!
- Ótimo para ordenar na PED e na LED