# Analisador Léxico da Linguagem Algorítmica (LA)

Este é um analisador léxico simples para a linguagem Algorítmica (LA). Ele é capaz de analisar um arquivo-fonte escrito em LA e identificar os tokens presentes no código, como palavras-chave, identificadores, números, cadeias de caracteres, operadores aritméticos, operadores relacionais, operadores de memória e delimitadores.

## Pré-requisitos

Python 3.x

## Utilização
Para utilizar o analisador léxico, basta executar o script trabalho1.py passando como argumentos o arquivo de entrada contendo o código-fonte em LA e o arquivo de saída onde o resultado da análise será gravado.

```python
Python3 trabalho1.py <arquivo_de_entrada> <arquivo_de_saida>
```
## Sintaxe Suportada

O analisador léxico reconhece os seguintes elementos da linguagem LA:

Palavras-chave: como "algoritmo", "declare", "real", "inteiro", "se", "senao", entre outras.
Operadores aritméticos: "+", "-", "*", "/", "%".
Operadores relacionais: "<", ">", "=", "<-", "<>", "!=", "<=", ">=", "==".
Operadores de memória: "&", "^".
Delimitadores: ":", ";", ",", "(", ")", "[", "]", "/", "..", "^", "&".
Identificadores: sequências de caracteres alfanuméricos começando com uma letra ou sublinhado.
Números inteiros: sequências de dígitos.
Números reais: sequências de dígitos com um ponto decimal.
Cadeias de caracteres: sequências de caracteres entre aspas duplas.

## Saída

O analisador léxico produz um arquivo de saída contendo a lista de tokens encontrados no código-fonte, bem como eventuais mensagens de erro indicando símbolos não identificados, comentários não fechados ou cadeias de caracteres não fechadas.

## Exemplo
Um exemplo de uso do analisador léxico:

```python
Python3 trabalho1.py entrada.txt saida.txt
```
Isso irá analisar o arquivo entrada.txt e gravar o resultado da análise no arquivo saida.txt.

## Casos de teste

O trabalho possui 37 casos de teste, para automatizar o processo de testar as saidas,o arquivo tes.py faz os arquivos saida.txt para todos casos de teste, como utilizar:

```python
Python3 tes.py
```



