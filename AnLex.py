# Programa feito para a disciplina de Compiladores, do 6º semestre, UTFPR Pato Branco
# O programa usa a bibliteca re, mais especificamente a função match, para comparar expressões regulares

from re import match
from os import system

def lerArquivo(codename):
    """
    :param codename nome do arquivo que será lido
    :return string com os caracteres do arquivo se encontrar, 0 se não encontrar o arquivo
    """
    # facilita a abertura do código com o nome padrão para entrar no arquivo codigoFonte.txt
    if codename == 'padrão':
        codename = 'codigoFonte.txt'
    # coloca  a extensão txt no final do nome do arquivo
    elif not(',txt' in codename):
        codename += '.txt'
    # tenta abrir o arquivo
    try:
        # abre de maneira segura o arquivo txt e retorna uma string com os carcteres do arquivo
        with open(codename, 'r') as code:
            code = code.read()
            system('clear')
            return code
    # se não encontrar o arquivo, retorna 0
    except FileNotFoundError:
        print('Arquivo não encontrado')
        return 0


def percorrerPalavras(codelinhas):
    """
    :param string do arquivo spearadas por linhas
    :return lista de tokens separados por espaço, desconsiderando comentários
    """
    # inicia o programa sem comentários abertos
    comentario_aberto = False
    # percorre as linhas da string com arquivo
    for linha in codelinhas:
        # separa a string nos espaços
        palavras= linha.split()
        for item in palavras:
            # se encontrar uma chave aberta, abre os comentário e desconsidera todos os strings até fechar
            if item[0] == '{':
                comentario_aberto = True
            # fecha o comentário
            if comentario_aberto and item.find('}') != -1:
                pos = item.find('}')
                if pos < len(item):
                    item = item[pos+1: len(item)]
                    comentario_aberto = False
                elif pos == len(item):
                    comentario_aberto = False
                    item = ''
            # se o item não estiver em um comentário, adiciona ele na lista global
            if len(item) > 0:
                if item[0] != '{' and not comentario_aberto:
                    codels.append(item)
        
        # adiciona o marcador de nova linha no final
        codels.append('###ENTER###')
    return codels

def analisarInteiro(word):
    '''
    :param: palavra para ser analisada
    :return: 0 se não corresponder a um número inteiro, 1 se corresponder
    '''
    # valida inteiros negativos
    if word[0] == '-':
        word = word[1:len(word)]
    # verifica se a palavra é um número
    if word.isnumeric():
        return True
    return False

def analisarFloat(word):
    '''
    :param: palavra para ser analisada
    :return: 0 se não corresponder a um número real, 1 se corresponder
    '''
    # valida se reais são negativos
    if word[0] == '-':
        word = word[1:len(word)]
    # verifica se está no formato para um float
    if '.' in word:
        real = word.split('.')
        if real[0].isnumeric() and real[1].isnumeric() and len(real) == 2:
            return True
    return False
        
def analisarIdentificador(word):
    '''
    :param: palavra para ser analisada
    :return: 0 se não corresponder a umidentificador, 1 se corresponder
    '''
    #  verifica se começa com caracter
    if not(match('[a-zA-Z]', word[0])):
        return 0
    # verifica se está no formato para um identificador
    for i in word:
        if not(match('\w', i)):
            return 0
    return 1

def analisadorLexico (code):
    """
    :param lista de tokens
    :return lista de tuplas no formato (tipo do token, linha do token, token)
    """
    linhaAtual = 1
    tokenls = list()
    erros = list()
    for word in codels:
            if word == '###ENTER###':
                linhaAtual += 1
            elif not(word == "###ENTER###"):
                if word == 'inteiro' :
                    tokenls.append('INTEIRO')
                elif word =='real':
                    tokenls.append('REAL')
                elif word =='booleano':
                    tokenls.append('BOOLEANO')
                elif word == 'programa':
                    tokenls.append('PROGRAMA')
                elif word == 'var':
                    tokenls.append('BLOCO')
                elif word == ':':
                    tokenls.append('DELCARACAO')
                elif word == 'inicio':
                    tokenls.append('COMANDO_INI')
                elif word == 'fim':
                    tokenls.append('COMANDO_FIM')
                elif word == ':=':
                    tokenls.append('ATRIBUICAO')
                elif word == 'se':
                    tokenls.append('CONDICIONAL_INI')
                elif word == 'entao':
                    tokenls.append('CONDICIONAL_INSTRUCT')
                elif word == 'senao':
                    tokenls.append('CONDICIONAL_ELSE')
                elif word == 'enquanto':
                    tokenls.append('LOOP_INI')
                elif word == 'faca':
                    tokenls.append('LOOP_COMANDO')
                elif word == 'leia':
                    tokenls.append('LEITURA')
                elif word == 'escreva':
                    tokenls.append('ESCRITA')
                elif word == '<>':
                    tokenls.append('DIFERENTE')
                elif word == '<=':
                    tokenls.append('MENOR_IGUAL')
                elif word =='>=':
                    tokenls.append('MAIOR_IGUAL')
                elif word =='>':
                    tokenls.append('MAIOR')
                elif word =='>=':
                    tokenls.append('MENOR_IGUAL')
                elif word == '+':
                    tokenls.append('MAIS')
                elif word =='-':
                    tokenls.append('MENOS')
                elif word =='ou':
                    tokenls.append('OU')
                elif word == '*':
                    tokenls.append('MULTIPLICACAO')
                elif word =='/':
                    tokenls.append('DIVISAO')
                elif word =='e':
                    tokenls.append('E_LOGICO')
                elif word =='(':
                    tokenls.append('ABRE_PARENTESES')
                elif word ==')':
                    tokenls.append('FECHA_PARENTESES')
                elif word ==';':
                    tokenls.append('PONTO_VIRGULA')
                elif word ==',':
                    tokenls.append('VIRGULA')
                elif analisarInteiro(word):
                    tokenls.append('INTEIRO')
                elif analisarFloat(word):
                    tokenls.append('REAL')
                elif analisarIdentificador(word):
                    tokenls.append('IDENTIFICADOR')
                else:
                    tokenls.append('ERROR')
                    erros.append(('ERROR', linhaAtual, word))
    return tokenls, erros

def anLex():
    """
    inicia o analisador léxico
    usa as variáveis globais codels, tokens e erros
    :param none
    :return none
    """
    global codels
    global tokens
    codels = list()
    codename = input('Informe o nome do arquivo de texto com: ')
    code = lerArquivo(codename)
    if code:
        codelinhas = code.split('\n')
        percorrerPalavras(codelinhas)
        tokenls = analisadorLexico(code)
        tokens = tokenls[0]
        erros = tokenls[1]
        print(tokens)
        print(erros)


anLex()
