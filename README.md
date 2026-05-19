# Sistema Nutricional

Projeto em Python para cadastro de usuário, cálculo de taxa metabólica basal, definição de meta calórica diária e registro de alimentos consumidos ao longo dos dias.

O sistema utiliza programação orientada a objetos e banco de dados SQLite para armazenar o histórico alimentar.

## Objetivo do projeto

O objetivo do programa é permitir que o usuário:

- cadastre seus dados pessoais;
- calcule sua Taxa Metabólica Basal (TMB);
- calcule seu Gasto Energético Total (GET);
- defina uma meta diária de calorias de acordo com o objetivo;
- cadastre alimentos consumidos;
- visualize o resumo diário;
- acesse o histórico alimentar;
- acompanhe se atingiu ou ultrapassou a meta calórica;
- reinicie o histórico salvo no banco de dados.

## Tecnologias utilizadas

- Python 3
- SQLite
- Biblioteca `sqlite3`

A biblioteca `sqlite3` já vem instalada junto com o Python, então não é necessário instalar dependências externas.

## Estrutura principal do projeto

O projeto está concentrado no arquivo:

```text
sistema_calorias.py
```

Durante a execução, o programa cria automaticamente o banco de dados:

```text
alimentos.db
```

Esse banco armazena os alimentos cadastrados pelo usuário.

## Classes implementadas

### Usuario

Representa o usuário do sistema.

Atributos principais:

```text
nome
idade
peso
altura
objetivo
nivel_ativo
```

Métodos principais:

```text
calcular_gasto_energetico_total()
set_idade()
set_peso()
set_altura()
```

A classe `Usuario` é a classe base para os tipos de usuário do sistema.

### Homem

Classe filha de `Usuario`.

Método principal:

```text
calcular_metabolismo_basal()
```

Essa classe calcula a Taxa Metabólica Basal usando a fórmula aplicada para usuários do gênero masculino.

### Mulher

Classe filha de `Usuario`.

Método principal:

```text
calcular_metabolismo_basal()
```

Essa classe calcula a Taxa Metabólica Basal usando a fórmula aplicada para usuários do gênero feminino.

### Alimento

Representa um alimento consumido pelo usuário.

Atributos principais:

```text
nome_alimento
gramas
cal
proteina
carbo
gordura
```

Método principal:

```text
registrar_alimento(dia)
```

Esse método salva o alimento no banco de dados SQLite, associando o registro ao dia atual.

## Funções implementadas

### linha()

Exibe uma linha separadora no terminal para melhorar a organização visual do programa.

### mensagem_erro()

Mostra uma mensagem quando ainda não há alimentos registrados.

### exibir_historico(contagem_dias=None)

Exibe os alimentos registrados.

Quando recebe um número de dia, mostra apenas o resumo daquele dia.  
Quando não recebe parâmetro, mostra o histórico completo.

A função agrupa os alimentos pelo nome e soma:

```text
gramas
calorias
proteínas
carboidratos
gorduras
```

### calculo_calorias(contagem_dias)

Calcula o total de calorias registradas em um determinado dia.

Essa função é usada para verificar se o usuário atingiu ou ultrapassou a meta calórica diária.

### cadastro_usuario()

Solicita os dados do usuário no terminal e retorna um objeto da classe `Homem` ou `Mulher`.

## Como executar o programa

### 1. Verifique se o Python está instalado

No terminal, execute:

```bash
python --version
```

ou:

```bash
python3 --version
```

Se aparecer uma versão do Python, como `Python 3.11.0`, está tudo certo.

### 2. Baixe ou copie o arquivo do projeto

O arquivo principal deve estar salvo como:

```text
sistema_calorias.py
```

### 3. Abra o terminal na pasta do projeto

No VS Code, você pode fazer assim:

1. Abra a pasta do projeto.
2. Clique em **Terminal**.
3. Clique em **New Terminal** ou **Novo Terminal**.

### 4. Execute o programa

No Windows, use:

```bash
python sistema_calorias.py
```

No Mac ou Linux, use:

```bash
python3 sistema_calorias.py
```

## Como usar o sistema

Ao iniciar o programa, ele pedirá os dados do usuário:

```text
Nome
Idade
Gênero
Peso
Altura
Objetivo
Nível de atividade física
```

Depois disso, o sistema calcula:

```text
Taxa Metabólica Basal
Gasto Energético Total
Meta diária de calorias
```

Em seguida, aparece o menu principal:

```text
[1] Cadastrar um alimento
[2] Acessar resumo diário
[3] Acessar histórico
[4] Avançar dia
[5] Visualizar meta de calorias
[6] Reiniciar histórico
[7] Encerrar programa
```

## Exemplo de uso

### Cadastro de usuário

```text
Qual o seu nome? João
Qual a sua idade? 21
Qual o seu gênero? [M/F] M
Qual o seu peso (kg)? 70
Qual a sua altura (cm)? 178
```

### Cadastro de alimento

```text
Qual alimento você comeu? arroz
Quanto você comeu? (g) 150
Quantas calorias por porção? (cal) 190
Quanto de proteína? (g) 4
Quanto de carboidrato? (g) 42
Quanto de gordura? (g) 1
```

### Exemplo de resumo diário

```text
arroz -> 150g (190cal) | 4g de proteina | 42g de carboidratos | 1g de gordura
```

### Exemplo de meta de calorias

```text
Falta ainda 350.50 calorias pra atingir o objetivo!
```

ou:

```text
Você atingiu o objetivo!
```

## Banco de dados

O programa usa SQLite e cria automaticamente o arquivo:

```text
alimentos.db
```

A tabela criada se chama:

```text
alimentos_dia
```

Ela possui os seguintes campos:

```text
nome_alimento
gramas
cal
proteina
carbo
gordura
dia
```

Cada alimento cadastrado é salvo nessa tabela.

## Observações importantes

- O histórico alimentar fica salvo no arquivo `alimentos.db`.
- Se o programa for fechado, os registros continuam salvos.
- A opção `Reiniciar histórico` apaga todos os alimentos registrados.
- O programa roda no terminal.
- Não é necessário instalar bibliotecas externas.

## Possíveis melhorias futuras

Algumas melhorias que podem ser adicionadas futuramente:

- validação mais completa das entradas do usuário;
- tratamento para opções inválidas no menu;
- cadastro de múltiplos usuários;
- edição ou remoção de alimentos específicos;
- exportação do relatório em PDF;
- interface gráfica;
- separação do código em múltiplos arquivos;
- uso de propriedades com `@property`;
- cálculo automático dos macronutrientes ideais.
