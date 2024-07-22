# List 3

### Ex 1

Eles podem ser criados através de classes, que validam seus dados e ficam responsáveis pela inserção póstuma, ou pelo uso de funções que lêem todas as informações necessárias e fazem a formatação correta tal como a validação dos dados, concatenando os valores em um buffer que será então inserido.

### Ex 2

**Número Fixo de Campos:** Com um número fixo de campos, sabemos a separação exata de cada registro e conseguimos fazer uma leitura fácil e sequencial. Entretanto, com essa limitação, não podemos variar o tamanho de campos e, para acharmos um próximo registro, precisamos fazer uma leitura sequencial para cada unidade de byte, passando por toda extensão do arquivo.

**Indicação de Tamanho:** Com a indicação de tamanho, conseguimos o benefício de ter campos variáveis e até conseguir navegar rapidamente pelos registros, porque não precisamos mais ler byte por byte, mas ainda temos uma busca sequencial O(n). De pontos negativos, temos o gasto extra de bytes que vão ocupar um espaço adicional do arquivo.

**Metadados:** Com os metadados conseguimos dar significado aos campos e valores, além de organizar o arquivo de uma forma muito melhor e mais significativa. Entretanto, os metadados podem consumir um espaço de armazenamento do arquivo muito considerável

### Ex 3

Porque é necessário ler o bloco todo para, então, recuperar a informação requerida, que é parte de um todo maior e, consequentemente, precisa da trasnferência de mais que o necessário.

### Ex 4

- a) Uma leitura por registro, logo, 10000 leituras, até achar o registro. Logo, em média são 5000 leituras

- b) 10000

- c) 10000/20 = 500 e 500/2 = 250 leituras de blocos, mas aumenta a taxa de transferência.

### Ex 5

O arquivo sequencial funciona por meio da leitura de todo o arquivo seguindo uma ordem específica e passando por tudo, logo, tem complexidade O(n). O acesso direto é feito por meio de já saber onde está o registro, logo, seu acesso tem complexidade O(1). Para realizar cada um, é preciso que o arquivo esteja adaptado para isso, logo, não é possível em um arquivo qualquer executar cada um. Entretanto, é comum que o sequencial seja possível em quase todos, mas o outro vai depender do mapeamento dos byte offsets ou rrns.

### Ex 6

- a) 36, já que 0x24 = 36
- b) Dump|Fred|821 Kluge|Hacker|PA|65535|

### Ex 7

Como 32 é divisor de 512 e também é uma potência de 2, é muito mais simples para que as inserções de registros fossem feitas em um mesmo setor, de modo a não causar a fragmentação, simplificando a escrita e a leitura. 