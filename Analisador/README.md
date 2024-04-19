# Entendendo o código

Este código é um analisador léxico, deixo aqui uma explicação sobre o código:

1. Importação de bibliotecas e definição de listas de tokens:
   
* O código começa importando a biblioteca re para trabalhar com expressões regulares, que serão usadas para identificar padrões no código fonte.
* Em seguida, são definidas três listas de tokens: PALAVRAS_CHAVE, OP_ARITMETICOS e DELIMITADORES, que contêm as palavras-chave, operadores aritméticos, operadores relacionais e delimitadores reconhecidos pela linguagem.
  
2.Expressões regulares:

* São definidas expressões regulares para identificar cadeias de caracteres entre aspas (PADRAO_CADEIA), números reais (PADRAO_REAL), números inteiros (PADRAO_INTEIRO) e identificadores (PADRAO_IDENTIFICADOR).

3.Classe Token:

* Define a classe Token, que representa um token do código fonte. Cada token possui um lexema (texto correspondente) e um tipo.

4.Função main:

* Recebe argumentos da linha de comando e chama a função analisar_codigo para analisar o código fonte.

5.Função analisar_codigo:

* Abre o arquivo de entrada e de saída.
* Itera sobre as linhas do arquivo de entrada, analisando cada linha com a função analisar_linha.
* Escreve os tokens encontrados no arquivo de saída.

6.Função analisar_linha:

* Remove comentários e espaços em branco.
* Itera sobre cada parte da linha, analisando-as com base no contexto de cadeias de caracteres.
* Retorna os tokens encontrados.

7.Função analisar_parte:

* Divide uma parte da linha em tokens e os analisa.
* Reconhece números, identificadores, palavras-chave e operadores.

8.Função analisar_ponto:

* Analisa partes separadas por ponto, tratando os casos específicos de números e identificadores.

9.Função analisar_token:

* Analisa um token individual, identificando palavras-chave, operadores, números, cadeias de caracteres e identificadores.

10.Função analisar_cadeia:

* Analisa cadeias de caracteres entre aspas, removendo os espaços extras.

11.Bloco __name__ == "__main__":

* Chama a função main passando os argumentos da linha de comando.
