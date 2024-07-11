# Aula 3

### Organização Campos e Registros

Campo é a menor unidade de formação com significado

Um registro é uma junção de Campos

### Estruturas de Campos

Para manter a integridade das informações temos:

**Método 1:** Definir Campos de tamanho FIXO  
**Método 2:** Iniciar cada campo com um indicador de tamanho, para sabermos quando ele começa e acaba. Tamanho VARIÁVEL  
**Método 3:** Separar os campos por um delimitador. Tamanho Variável  
**Método 4:** Usar uma expressão do tipo *palavra-chave = valor* para identificar um campo e seu conteúdo. Tamanho Variável

### Método 1 - Tamanho Fixo

Silva Flores000Alan Andre0Rua BragaMaringa0PR871220

- Força os dados em campos de tamanho fixo
- Aumento do tamanho do arquivo, mesmo que com menos conteúdo que o caso real.
- Alguns campos podem não caber no tamanho máximo
- Facilita a implementação em linguagens, pois os tamanhos já são definidos

### Método 2 - Indicador de Tamanho

05Silva04ALan13Rua Tiete 12307Maringa02PR0587100

- O tamanho é armazenado antes do valor do campo
- Tamanho limitado pelo número de bytes definido para indicar isso, ex 1 byte = 255 valores
- Tamanho 0 indica campo ausente

### Método 3 - Delimitador

Silva|Alan|Rua Tiete 123|Maringa|PR|87100

- O delimitador deve ser um caractere especial que nunca mais aparece, como o |
- Permite campos de fato variáveis

### Método 4 - *palavra-chave = valor*

<last=Silva><first=Alan><address=Rua Tiete 123><city=Maringa><state=PR><zip=87100>

- Cada campo tem uma palavra-chave que o descreve - metadados
- Facilita a identificação de conteúdo do arquivo
- Facilita tratar campos ausentes
- Aumenta bastante o tamanho do arquivo

### Estruturas de Registros

Junção de campos que também devem ser separados, uma forma conceitual

Mais um nível de organização

Para manter a integridade das informações temos:

**Método 1:** Definir Campos de tamanho FIXO  
**Método 2:** Número fixo de campos. Tamanho variável  
**Método 3:** Registros com indicação de tamanho  
**Método 4:** Registros apontados por índices
**Método 5:** Registros com delimitadores

### Método 1 - Registros de tamanho fixo

Pode ser registro de tamanho fixo com campos de tamanho fixo ou variável

Ex de registro de tamanho fixo com campos de tamanho variável

Silva|Alan|Rua Joa 12|Maringa|PR|87100\0\0\0\0\0\0\0\0

- Cada registro tem um tamanho fixo de bytes
- Não limita cada campo, mas a soma do tamanho de todos os campos
- Bem fácil de implementar
- O regitro funciona como um container
- Em campos de tamanho fixo, a soma do tamanho dos campos sempre será o tamanho do registro

Fragmentação interna: Muito espaço vazio, já que o tamanho do registro sempre é fixo, enquanto os dados dentro dele podem ser menores que isso.

### Método 2 - Registros com numero fixo de campos

- Registo de tamanho variável
- Campos de tamanho fixo ou variável
- Existe um número fixo de campos
- Não há fragmentação interna
- Difícil diferenciar quando começa um outro registro

### Método 3 - Indicador de tamanho

42Silva|Alan|Rua Tiete 123|Maringa|PR|87100|

- O registro começa com um indicador do seu tamanho em bytes
- O tamanho dele é limitado ao número de bytes reservados para isso
- É preciso conhecer o tamanho final para a gravação do registro
- Usa-se um buffer para armazenar os dados e calcular o tamanho antes de enviar para o arquivo

### Método 4 - Registros apontados por índices

- Uso de um arquivo de índices que aponta para os registros no arquivo de dados
- Cada entrada do índice mantém o offset do registro original
- A diferença dos offsets entre dois registros consecutivos é o tamanho do registro
- Os registros no arquivo de enderços são consecutivos e correspondentes aos dos arquivos de dados

**Arquivo de dados:**  
Silva|Alan|Rua Tiete 123|Maringa|PR|87100ZFlores|Andre|Rua Braga 34|Sarandi ...

**Arquivo de indices:**  
00 42 ...

### Método 5 - Registros com delimitadores

- Mesma ideia de delimitar campos
- Muito comum separar por linhas, com o '\n'

### Conclusão

Podemos combinar vários e formar diversos tipos de métodos de guardar registros!!