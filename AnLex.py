# Programa feito para a disciplina de Compiladores, do 6º semestre, UTFPR Pato Branco
# O programa usa a bibliteca re, mais especificamente a função match, para comparar expressões regulares

from re import match
from os import system

def lerArquivo(codename):
    """
    :param codename nome do arquivo que será lido
    :return string com os caracteres do arquivo se encontrar, 0 se não encontrar o arquivo
    """
    if codename == 'padrão':
        codename = 'codigoFonte.txt'
    elif not(',txt' in codename):
        codename += '.txt'
    try:
        with open(codename, 'r') as code:
            code = code.read()
            system('clear')
            return code
    except FileNotFoundError:
        print('Arquivo não encontrado')
        return 0


def percorrerPalavras(codelinhas):
    """
    :param string do arquivo spearadas por linhas
    :return lista de tokens separados por espaço, desconsiderando comentários
    """
    comentario_aberto = False
    for linha in codelinhas:
        aux= linha.split()
        for item in aux:
            #print(item)
            if item[0] == '{':
                comentario_aberto = True
            if comentario_aberto and item.find('}') != -1:
                pos = item.find('}')
                if pos < len(item):
                    item = item[pos+1: len(item)]
                    comentario_aberto = False
                elif pos == len(item):
                    comentario_aberto = False
                    item = ''
            if len(item) > 0:
                if item[0] != '{' and not comentario_aberto:
                    codels.append(item)
        codels.append('###ENTER###')
    return codels

def analisarInteiro(word):
    '''
    :param: palavra para ser analisada
    :return: 0 se não corresponder a um número inteiro, 1 se corresponder
    '''
    if word[0] == '-':
        word = word[1:len(word)]
    if word.isnumeric():
        return True
    return False

def analisarFloat(word):
    '''
    :param: palavra para ser analisada
    :return: 0 se não corresponder a um número real, 1 se corresponder
    '''
    if word[0] == '-':
        word = word[1:len(word)]
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
    if not(match('[a-zA-Z]', word[0])):
        return 0
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
                    tokenls.append(('INTEIRO', linhaAtual, word))
                elif word =='real':
                    tokenls.append(('REAL', linhaAtual, word))
                elif word =='booleano':
                    tokenls.append(('BOOLEANO', linhaAtual, word))
                elif word == 'programa':
                    tokenls.append(('PROGRAMA', linhaAtual, word))
                elif word == 'var':
                    tokenls.append(('BLOCO', linhaAtual, word))
                elif word == ':':
                    tokenls.append(('DELCARACAO', linhaAtual, word))
                elif word == 'inicio':
                    tokenls.append(('COMANDO_INI', linhaAtual, word))
                elif word == 'fim':
                    tokenls.append(('COMANDO_FIM', linhaAtual, word))
                elif word == ':=':
                    tokenls.append(('ATRIBUICAO', linhaAtual, word))
                elif word == 'se':
                    tokenls.append(('CONDICIONAL_INI', linhaAtual, word))
                elif word == 'entao':
                    tokenls.append(('CONDICIONAL_INSTRUCT', linhaAtual, word))
                elif word == 'senao':
                    tokenls.append(('CONDICIONAL_ELSE', linhaAtual, word))
                elif word == 'enquanto':
                    tokenls.append(('LOOP_INI', linhaAtual, word))
                elif word == 'faca':
                    tokenls.append(('LOOP_COMANDO', linhaAtual, word))
                elif word == 'leia':
                    tokenls.append(('LEITURA', linhaAtual, word))
                elif word == 'escreva':
                    tokenls.append(('ESCRITA', linhaAtual, word))
                elif word == '<>':
                    tokenls.append(('DIFERENTE', linhaAtual, word))
                elif word == '<=':
                    tokenls.append(('MENOR_IGUAL', linhaAtual, word))
                elif word =='>=':
                    tokenls.append(('MAIOR_IGUAL', linhaAtual, word))
                elif word =='>':
                    tokenls.append(('MAIOR', linhaAtual, word))
                elif word =='>=':
                    tokenls.append(('MENOR_IGUAL', linhaAtual, word))
                elif word == '+':
                    tokenls.append(('MAIS', linhaAtual, word))
                elif word =='-':
                    tokenls.append(('MENOS', linhaAtual, word))
                elif word =='ou':
                    tokenls.append(('OU', linhaAtual, word))
                elif word == '*':
                    tokenls.append(('MULTIPLICACAO', linhaAtual, word))
                elif word =='/':
                    tokenls.append(('DIVISAO', linhaAtual, word))
                elif word =='e':
                    tokenls.append(('E_LOGICO', linhaAtual, word))
                elif word =='(':
                    tokenls.append(('ABRE_PARENTESES', linhaAtual, word))
                elif word ==')':
                    tokenls.append(('FECHA_PARENTESES', linhaAtual, word))
                elif word ==';':
                    tokenls.append(('PONTO_VIRGULA', linhaAtual, word))
                elif word ==',':
                    tokenls.append(('VIRGULA', linhaAtual, word))
                elif analisarInteiro(word):
                    tokenls.append(('INTEIRO', linhaAtual, word))
                elif analisarFloat(word):
                    tokenls.append(('REAL', linhaAtual, word))
                elif analisarIdentificador(word):
                    tokenls.append(('IDENTIFICADOR', linhaAtual, word))
                else:
                    tokenls.append(('ERROR', linhaAtual, word))
                    erros.append((('ERROR', linhaAtual, word)))
    return tokenls, erros


def printTokens(tokenls, wordPrint=False):
    """
    imprime a lista de tokens com a posição deles, depois imprime separadamente os erros, caso não haja erros, imprime que não há erros léxicos
    :param lista de tuplas de tokens
    :param controlador para imprimir ou não a palavra passada
    :return none
    """
    linha = 1
    for token in tokenls[0]:
        if linha != token[1]:
            print()
            linha = token[1]
        print(f'<{token[0]},{token[1]}', end = '')
        if wordPrint:
            print(f', {token[2]}>', end =' ')
        else:
            print('>', end=' ')

    if len(tokenls[1]) > 0:
        print(f'\n{tokenls[1]}')
    else:
        print('\nNão há erros léxicos')


def anLex():
    """
    inicia o analisador léxico
    usa as variáveis globais codels, tokens e erros
    :param none
    :return none
    """
    global codels
    global tokens
    global erros
    codels = list()
    codename = input('Informe o nome do arquivo de texto com: ')
    code = lerArquivo(codename)
    if code:
        codelinhas = code.split('\n')
        percorrerPalavras(codelinhas)
        tokenls = analisadorLexico(code)
        printTokens(tokenls)   
        tokens = tokenls[0]
        erros = tokenls[1]


anLex()
