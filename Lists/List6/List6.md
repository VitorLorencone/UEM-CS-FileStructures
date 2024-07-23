# Lista 6

### Ex 1

Os Índices permitem uma busca direta e mais simplificada de um arquivo, sendo de fácil ordenação e escalabilidade, criando uma ordem sem modificar o arquivo fisicamente. Podem permitir leituras por chaves primárias ou secundárias

### Ex 2

Quando sua memória excede o possível da memória principal, sendo necessário armazená-lo em um outro arquivo, utilizando-se a memória secundária e dificultando a complexidade de tempo

### Ex 3

Com a chave secundária passando primeiro pela primária temos questões de segurança de dados e informações, além de que um eventual erro não afeta na raiz da organização de índices. 

Late Binding: Maio segurança, menor custo em alteração e remoção, Busca mais lenta

Early Binding: Menor segurança, maior custo de alteração e busca mais rápida

### Ex 4

É dividido por late e early binding, com registros fixos ou variáveis, podendo alterar todos os indíces primários e secundários ou não

### Ex 5

Não fiz

### Ex 6

A lista invertida permite o uso de uma lista encadeada para listar todas as chaves primárias de uma chave secundária, ela facilita escrita remoção de registros. Além disso, cada chave secundária terá uma única aparição, ocasionando na possibilidade de binary search na lista

### Ex 7

- Lista Invertida
Chave Primária / Prox  
0 COL / -1  
1 DG18 / 2  
2 RCA / -1  
3 LON / -1  
4 DG13 / 1  
5 ANG / 4  
6 WAR / -1  

- Índice Secundário
Chave Secundária / RRn  
Bethoven / 5
Corea / 6  
Dvorak / 0  
Prokofiev / 3  

### Ex 8

Porque ela é feita de forma lógica ordenada, não acompanhando sua ligação física, de modo que referências para uma mesma chave secundária podem estar espalhadas pela lista invertida, não indicando sua localidade

### Ex 9

Será feito depois

### Ex 10

Será feito depois

### Ex 11

Será feito depois