import re

# Lista de palavras-chave, operadores e delimitadores
PALAVRAS_CHAVE = [
    "algoritmo", "declare", "real", "inteiro", "literal", "leia", "escreva",
    "se", "entao", "senao", "fim_se", "fim_algoritmo", "fim", "constante", "tipo",
    "logico", "registro", "fim_registro", "procedimento", "var", "falso", "enquanto",
    "verdadeiro", "faca", "ate", "fim_enquanto", "fim_procedimento", "caso", "fim_caso", "seja",
    "para", "fim_para","funcao", "fim_funcao", "retorne", "constante","e","ou", "nao"
]

OP_ARITMETICOS = ["+", "-", "*", "/", "%"]
OP_RELACIONAIS = ["<", ">", "=", "<-", "<>", "!=", "<=", ">=", "=="]
OP_MEMORIA = ["&", "^"]
DELIMITADORES = [":", ";", ",", "(", ")", "[", "]", "/", "..", "^", "&"]



# Expressão regular para cadeias de caracteres entre aspas
PADRAO_CADEIA = re.compile(r'\s*"(.*?)"\s*')
# Expressão regular para números reais
PADRAO_REAL = re.compile(r'\b\d+\.\d+\b')  # Atualizado para reconhecer números reais com ponto decimal
# Expressão regular para números inteiros
PADRAO_INTEIRO = re.compile(r'\b\d+\b')
# Expressão regular para identificadores
PADRAO_IDENTIFICADOR = re.compile(r'\b[a-zA-Z_]\w*\b')


class Token:
    def __init__(self, lexema, tipo):
        self.lexema = lexema
        self.tipo = tipo

    def get_lexema(self):
        return self.lexema

    def get_tipo(self):
        return self.tipo


def main(args):
    if len(args) != 3:
        print("Uso: python Lala.py <arquivo_de_entrada> <arquivo_de_saida>")
        return

    arquivo_entrada = args[1]
    arquivo_saida = args[2]

    analisar_codigo(arquivo_entrada, arquivo_saida)


def analisar_codigo(arquivo_entrada, arquivo_saida):
    try:
        with open(arquivo_entrada, 'r') as reader, open(arquivo_saida, 'w') as writer:
            numero_linha = 1
            simbolo_nao_identificado = False  

            for linha in reader:
                tokens = analisar_linha(linha, numero_linha)
                for token in tokens:
                    if token.tipo == "SIMBOLO_NAO_IDENTIFICADO":
                        writer.write(f"Linha {numero_linha}: {token.lexema} - simbolo nao identificado\n")
                        simbolo_nao_identificado = True  
                        break  
                    if token.tipo == "COMENTARIO_NAO_FECHADO":
                        writer.write(f"Linha {numero_linha}: comentario nao fechado\n")
                        simbolo_nao_identificado = True 
                        break 
                    if token.tipo == "CADEIA_NAO_FECHADA":
                        writer.write(f"Linha {numero_linha}: cadeia literal nao fechada\n")
                        simbolo_nao_identificado = True  
                        break 
                    elif token.tipo == "IDENT":
                        writer.write(f"<'{token.lexema}',{token.tipo}>\n")
                    elif token.tipo == "CADEIA":
                        writer.write(f"<'{token.lexema}',{token.tipo}>\n")
                    elif token.tipo == "NUM_INT":
                        writer.write(f"<'{token.lexema}',{token.tipo}>\n")
                    elif token.tipo == "NUM_REAL":
                        writer.write(f"<'{token.lexema}',{token.tipo}>\n")
                    else: 
                        writer.write(f"<'{token.lexema}','{token.tipo}'>\n")
                
                # Verifica se um símbolo não identificado foi encontrado e, se sim, interrompe a escrita no arquivo
                if simbolo_nao_identificado:
                    break
                
                numero_linha += 1

            print("Análise léxica concluída com sucesso. Saída gravada em:", arquivo_saida)
    except IOError as e:
        print("Ocorreu um erro ao ler ou gravar o arquivo:", e)

def analisar_linha(linha, numero_linha):
    tokens = []
    # Remove comentários
    linha = re.sub(r'\{.*?\}', '', linha)
    # Remove espaços em branco no início e no fim da linha
    linha = linha.strip()

    # Variável para controlar se estamos dentro de uma cadeia de caracteres
    dentro_cadeia = False

    if '{' in linha and '}' not in linha: 
        tokens.append(Token("", "COMENTARIO_NAO_FECHADO"))

    for parte in linha.split('"'):
        if dentro_cadeia:

            if '"' in linha and linha.count('"') % 2 != 0:
                
                tokens.append(Token("", "CADEIA_NAO_FECHADA"))
            else:
                tokens.extend(analisar_cadeia('"' + parte + '"'))
                

        else:
            # Se não estamos dentro de uma cadeia de caracteres, analisamos a parte normalmente
            tokens.extend(analisar_parte(parte))

        # Alterna o estado da variável dentro_cadeia
        dentro_cadeia = not dentro_cadeia

    return tokens






def analisar_parte(parte):
    tokens = []
    # Adiciona espaço antes e depois de cada delimitador para facilitar a divisão
    for delim in DELIMITADORES:
        parte = parte.replace(delim, " " + delim + " ")

    # Dividir a parte em tokens
    partes_separadas = parte.split()

    for p in partes_separadas:
        if p.strip():
            if '.' in p and p.count('.') == 1:
                # Verifica se há apenas um ponto na parte
                partes_ponto = p.split('.')
                if all(part.isdigit() for part in partes_ponto):
                    # Verifica se ambas as partes separadas por ponto são dígitos
                    tokens.append(Token(p, "NUM_REAL"))
                else:
                    # Se não forem ambos dígitos, considera como identificador
                    tokens.extend(analisar_ponto(p,'.'))
            elif '-' in p and p.count('-') == 1 and all(part.isdigit() for part in p.split('-')):
                tokens.extend(analisar_ponto(p, '-'))
            elif p.startswith("-"):
                if p[1:].isdigit():
                    tokens.append(Token("-", "-"))
                    tokens.append(Token(p[1:], "NUM_INT"))
                else:
                    if p == "-" and not PADRAO_IDENTIFICADOR.match(p):
                        tokens.append(Token("-", "-"))
                    else:
                        tokens.append(Token("-", "-"))
                        tokens.append(Token(p[1:], "IDENT"))
                

            elif p in PALAVRAS_CHAVE:
                # Verifica se é uma palavra-chave
                tokens.append(Token(p, p))
            elif p.isdigit():
                # Verifica se é um número inteiro positivo
                tokens.extend(analisar_token(p))
            else:
                # Se não for um número, verifica se é um identificador
                match_identificador = PADRAO_IDENTIFICADOR.match(p)
                if match_identificador:
                    # Se for um identificador, verifique se há um símbolo não alfanumérico anexado
                    identificador = match_identificador.group()
                    simbolo_nao_alfanumerico = p[len(identificador):]
                    if simbolo_nao_alfanumerico and not simbolo_nao_alfanumerico.isalnum() and simbolo_nao_alfanumerico not in DELIMITADORES:
                        # Se houver um símbolo não alfanumérico anexado, tratamos como símbolo não identificado
                        tokens.append(Token(identificador, "IDENT"))
                        tokens.append(Token(simbolo_nao_alfanumerico, "SIMBOLO_NAO_IDENTIFICADO"))
                    else:
                        # Se não houver símbolo não alfanumérico anexado, tratamos como identificador normal
                        tokens.append(Token(p, "IDENT"))
                else:
                    # Se não for um identificador, tratamos como um token normal
                    tokens.extend(analisar_token(p))
                    

    return tokens



def analisar_ponto(parte, ponto):
    tokens = []
    partes = parte.split(ponto)
    for i, parte in enumerate(partes):
        if parte.strip():
            if i != len(partes) - 1:
                if parte.isdigit():
                    tokens.append(Token(parte, "NUM_INT"))
                else:
                    tokens.append(Token(parte, "IDENT"))

            else:
                tokens.append(Token(ponto, ponto))
                if parte.isdigit():
                    tokens.append(Token(parte, "NUM_INT"))
                else:
                    match_identificador = PADRAO_IDENTIFICADOR.match(parte)
                    if match_identificador:
                        identificador = match_identificador.group()
                        simbolo_nao_alfanumerico = parte[len(identificador):]
                        if simbolo_nao_alfanumerico and not simbolo_nao_alfanumerico.isalnum() and simbolo_nao_alfanumerico not in DELIMITADORES:
                            tokens.append(Token(identificador, "IDENT"))
                            tokens.append(Token(simbolo_nao_alfanumerico, "SIMBOLO_NAO_IDENTIFICADO"))
                        else:
                            tokens.append(Token(parte, "IDENT"))
                    else:
                        tokens.append(Token(parte, "IDENT"))
    return tokens

def analisar_token(token):
    if token in PALAVRAS_CHAVE:
        return [Token(token, token)]
    elif token in OP_ARITMETICOS or token in OP_RELACIONAIS or token in DELIMITADORES or token in OP_MEMORIA:
        return [Token(token, token)]
    elif PADRAO_CADEIA.match(token):
        return [Token(token, "CADEIA")]
    elif PADRAO_REAL.match(token):
        return [Token(token, "NUM_REAL")]
    elif PADRAO_INTEIRO.match(token):
        return [Token(token, "NUM_INT")]
    elif len(token) == 1 and token not in DELIMITADORES:
        return [Token(token, "SIMBOLO_NAO_IDENTIFICADO")]
    else:
        return [Token(token, "IDENT")]


def analisar_cadeia(cadeia):
    tokens = []
    match = PADRAO_CADEIA.search(cadeia)
    if match:

        texto = match.group(1)
        tokens.append(Token('"' + texto + '"', "CADEIA")) 
        
    return tokens

if __name__ == "__main__":
    import sys
    main(sys.argv)


