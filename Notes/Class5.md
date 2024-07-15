# Aula 5

### Fragmentação em Arquivos

25Silva|Alan|(23)3666-1111|23Flores|Andre|3300-9874|30Santos|Cristina|(42)3568-4789|...

Imagine que queremos escrever no espaço do do registro de tamanho 23 uma alteração que aumenta seu tamanho, desse modo, não podemos reescrever parte do arquivo, é muito custoso

A solução mais comum é remover **logicamente** o registro antigo e gravar o novo no fim do arquivo

25Silva|Alan|(23)3666-1111|***23Flores|Andre|3300-9874|***
30Santos|Cristina|(42)3568-4789|27Flores|Andre|(21)3300-9874|..

***Fragmentado***

Ou seja, o arquivo cresce com a reescrita ou remoção do dado, mas nunca encolhe!! Isso é péssimo, gera arquivos inúteis com informações antigas que não puderam se reorganizar

Fragmentação Interna: Espaço perdido DENTRO DE UM REGISTRO  
Fragmentação Externa: Espaço perdido FORA DOS REGISTROS

Atualização de registro de tamanho variável gera fragmentação, de tamanho fixo não

Remoção de qualquer tipo de registro gera fragmentação, porque todas as remoções são lógicas, não vale a pena "puxar" o resto do arquivo

Se o novo registro a ser atualizado é menor que o antigo, insira o novo no lugar do antigo, gera fragmentação interna

Se o novo registro a ser atualizado é maior que o antigo, insira o novo no fim do arquivo gera fragmentação externa

Na remoção, insere-se um char especial, como '*' no início do registro removido, para indicar que ele não é mais válido

Reserve também um campo adicional para sinalizar a remoção.

### Reutilização Estática

Reutilização estática ou compactação, serve para encontrar uma utilidade para espaços fragmentados

Copia registros válidos para um novo arquivo e depois libera o antigo, fácil, mas requer espaço em disco

Compacta no mesmo lugar, lendo e regravando apenas os registros válidos, mais demorado, mas requer menos espaço em disco

### Reutilização Dinâmica

### PED ou SSR

Utiliza os espaços fragmentados para inserir novos registros

Para fazer isso rapidamente, precisa-se saber rapidamente se existem espaços disponívels, saber o valor de 'salto' para os espaços e, para isso, precisamos armazenar os endereços de espaços disponíveis

Para registros de tamanho fixo, podemos utilizar uma pilha para armazenar essas informações -> Pilha de Espaços Disponíveis, que armazena os rrns dos reigstros removidos

SSR = Stack Space Reusage

A PED fica no Próprio arquivo de registros

1 Dados do 1º registro *3dos do 2º registro Dados do 3ºregistro *-1dos do 4º registro Dados do 5º

Armazenamos o topo da PED no cabeçalho do arquivo, ele quarta o RRN do último registro removido

Se topo = -1, então a pilha está vazias

Quando um registro é removido, ele é marcado e inserido na PED
- Gravamos o char de remoção no início do 1º campo
- O RRN do registro será o novo topo da PED e um ponteiro para o topo ANTIGO é colocado no espaço que acabou de ser liberado, logo, após o caractere de remoção
- Só funciona para registros de tamanho FIXO

### LED ou LSR

Arquivos com registro de tamanho VARIÁVEL

Ao invés de uma pilha, usamos uma lista de espaços disponíveis (LED)

LSR = List Space Reusage

Os ponteiros da LED são os byte-offsets dos registros removidos

- Armazenamos a cabeça da LED no cabeçalho do arquivo
- A cabeça quarda o byte-offset do último registro removido
- Quando um registro é removido, ele é marcado e inserido na cabeça da LED
- Para reutilizar um espaço disponível, temos que verificar que o tamanho do registro é <= ao tamanho do espaço
- Se um espaço adequado for encontrado, então ele é removido da LED
- Senão, o novo registro é inserido no fim do arquivo e a LED não se altera
- Os valores de fragmentação interna que sobram podem retornar para a LED
- Se esse espaço que sobra for MUITO pequeno, ele se torna inútil e vira uma fragmentação externa

### Fragmentação Externa

- Reutilização Estática é a melhor ideia
- Pode ser reduzida com estratégias inteligentes de manutenção da LED

Podemos ter uma LED de primeiro ajuste - "First fit", que foi o visto até agora, ou seja, a **LED não é ordenada**

Podemos ter uma LED de melhor ajuste - "best fit", que ela é ordenada em ordem crescente de tamanho dos espaços disponíveis, que costuma ser mais trabalhoso. O espaço encontrado é o menor espaço disponível adequado.

Podemos ter uma LED de pior ajuste - "worst fit", que ela é ordenada em ordem decrescente de tamanho dos espaços disponíveis, em que reutiliza o espaço logo da cabeça se ele for adequado. A sobra é a maior possível, aumentando chances de reutilização. Se o espaço da cabeça não for adequado, já sabemos direto que ele deve ir ao fim do arquivo

**First Fit**
- Rápido e fácil de gerencial
- Precisa percorrer muitas vezes na inserção
- Sobras mal otimizadas

**Best Fit**
- A fragmentação interna é a menor possível
- Sobras de fragmentação externas são mais comuns e vão se acumulando
- Sobras pequenas, mas de fragmentação interna, se acumulam no topo da LED, deixando a busca mais demorada
- Difícil manutenção

**Worst Fit**
- A busca na LED é mais rápida, pois se olha apenas um elemento
- As sobras serão as maiores possíveis, aumentando as chances de reutilizações de sucesso
- A manutenção da LED é mais lenta e difícil