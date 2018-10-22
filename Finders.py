#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import ast
import logging
import time

DEPTH = 2  #  Profundidade da arvore trie

#linearIdFind(id):
# id = string
# faz busca LINEAR e
# retorna uma liste com todos os dados de um filme da base
# a partiur do ID dado como parametro
def linearIdFind(filename, matchvalue, key=lambda val: val):
    with open('data/base/id', 'rb') as fptr:
        while fptr:
            line = fptr.readline().decode('utf8')
            if matchvalue == key(line):
                return(line)
            if matchvalue < key(line):
                return([])

#linearIdFind(id):
# id = string
# faz busca SEMI-BINÁRIA e
# retorna uma lista com todos os dados de um filme da base
# a partiur do ID dado como parametro
# obs: o código é uma adaptação minha de outro código das interwebs (que não funcionava)
def binaryIdFind(filename, matchvalue, key=lambda val: val):
    """
    Binary search a file for matching lines.
    Returns a list of matching lines.
    filename - path to file, passed to 'open'
    matchvalue - value to match
    key - function to extract comparison value from line
 
    >>> parser = lambda val: int(val.split('\t')[0].strip())
    >>> line_binary_search('sd-arc', 63889187, parser)
    ['63889187\t3592559\n', ...]
    """
    logging.propagate = False
    # Must be greater than the maximum length of any line.
    logging.debug(' Serching for '+str(matchvalue))
    logging.debug('          in  '+str(filename))
    logging.debug('w/ parameter  '+str(matchvalue[-3:]))

    max_line_len = 2 ** 12
    logging.debug(' Max lenght of Line: '+str(max_line_len))
    start = pos = 0
    end = os.path.getsize(filename)
    logging.debug(' End of File = ' + str(end)+' bytes')
    counter = 0
    lastMin = 0
    with open(filename, 'rb') as fptr:
        
        #verifica os dois primeiros
        line = fptr.readline().decode('utf8')
        linevalue = key(line)
        if linevalue == matchvalue:
            return([line])
        line = fptr.readline().decode('utf8')
        linevalue = key(line)
        if linevalue == matchvalue:
            return([line])
        fptr.seek(0)

        # Limit the number of times we binary search.
        for rpt in range(50):
            logging.debug('lastmin = '+ str(lastMin))
            logging.debug(' Start: |  '+ str(start))
            logging.debug(' End  : |  '+ str(end))
            last = pos
            pos = start + ((end - start) // 2)
            fptr.seek(pos)
            
            # Move the cursor to a newline boundary.
            fptr.readline()
            line = fptr.readline().decode('utf8')
            linevalue = key(line)
            logging.debug(' Line == Match | '+ str(linevalue) + ' = '+ str(matchvalue))
            logging.debug(' Pos  == Last  | '+ str(pos) + ' = '+ str(last))
            if linevalue == matchvalue or pos == last:
                #return(line)
                #print(line)
 
                # Seek back until we no longer have a match.
                while True:
                    fptr.seek(lastMin)
                    fptr.readline().decode('utf8')
                    if matchvalue != key(fptr.readline().decode('utf8')):
                        break
               # Seek forward to the first match.
                while fptr.tell() < end:
                    logging.debug('End  = '+str(end))
                    logging.debug('Fptr = '+str(fptr.tell()))
                    logging.debug(counter)
                    counter += 1  
                    line = fptr.readline().decode('utf8')
                    linevalue = key(line)     
                    if matchvalue == linevalue:
                        logging.debug('Repeats = '+str(counter))
                        break
                else:
                    # No match was found.
                    return []
                results = []
                while linevalue == matchvalue:
                    results.append(line)
                    line = fptr.readline().decode('utf8')
                    linevalue = key(line)
 
                return results
            elif linevalue < matchvalue:
                counter += 1
                lastMin = start
                start = fptr.tell()
            else:
                assert linevalue > matchvalue
                counter += 1                
                end = fptr.tell()
        else:
            raise RuntimeError('Binary Search Failed')


#   register
#   def: an register is an tuple with the format:
#   [ string: "titulo" , string: "Id" ]


def makeIndexTitle(listTitles):
    """
    listTitles: list( ["titulo","Id"] )
    A partir de uma lista de ["titulo","Id"] cria e retorna um indice 
    usando  uma arvore "try"(?) de profundidade definida globalmente,
    em que os indices sao as letras contidas no nome do filme, para
    facilitar a busca.
    a arvore de indices contem o seguinte formato:
    indice = 
    {
    dict( caracter ):
        "registros": list()
        "indice": dict(caracter)
    }
    """
    indice = {}
    for registro in listTitles:
        indice = addTitleToIndex(registro, indice)
    return indice

def addTitleToIndex(register, indice):
    """
    Adiciona um register(titulo, id) a arvore quase trie de indices existente
    """
    length = len(register[0])
    #  loop pra percorrer todos os caracters do titulo
    for index in range(length):
        level = indice
        # loop para adicionar os caracters seguintes ao procurado
        i = 0
        #while(i < DEPTH):
        while(i<DEPTH and index+i<length):  # otimizacao, diminuiu de 23.8 minutos para 22.7 minutos
        #for i in range(DEPTH):
            #if index+i >= length:
            #   break
            letra = register[0][index+i].lower()
            #  if the level not yet have the index with the actual letter, create the index
            if letra not in level:
                level[letra] = {"registros": [], "indice": {},}

            #  Verifies to have no repeat registers in the list
            if not level[letra]["registros"]:
                # list of registers empty
                level[letra]["registros"].append( register )

            elif level[letra]["registros"][-1] != register:
                # last register different from actual register
                level[letra]["registros"].append( register )
            level = level[letra]["indice"]
            i = i+1
    return indice
    

def searchIdFromTitle(index, string):
    """
    Procura por uma string na arvore quase 'trie' de indices, 
    retorna uma lista de registros do formato[titulo, id]
    """
    level = index
    string = string.lower()
    for letter in string:
        if letter in level:
            level = level[letter]
        else:
            break

    registros = []
    for registro in level['registros']:
        if string in registro[0].lower():
            registros.append(registro)
    return registros


#Utilidade unica para testes
def main():
    """
    ehSubs = lambda val: ast.literal_eval(val)[0]
    for i in range(1,10):
        print(binaryIdFind('data/base/id', 'tt000000'+str(i), ehSubs))
    for i in range(10,100):
        print(binaryIdFind('data/base/id', 'tt00000'+str(i), ehSubs))
    for i in range(100,167):
        print(binaryIdFind('data/base/id', 'tt0000'+str(i), ehSubs))
    for i in range(168,1000):
        print(binaryIdFind('data/base/id', 'tt0000'+str(i), ehSubs))
    #print(lineFind('id', 'tt0000020', ehSubs))
"""
    # Teste da arvore quase trie de indices
    string_buscada = 'wa'
    inicio = time.time()
    #lista = getPryTitleList('', 'pryTitle')
    lista = []
    with open('data/base/pryTitle', 'r') as baseFile:
        for line in baseFile:
            lista.append([ast.literal_eval(line)[0], ast.literal_eval(line)[1]])
    indice = makeIndexTitle(lista)
    #print(json.dumps(indice, sort_keys=True, indent=4))
    tempo_index = time.time()
    registro1 = searchIdFromTitle(indice, string_buscada)
    #print(json.dumps(registro1, indent=2))
    end = time.time()

    print('Numero de registros: %s' % len(lista))
    print('Palavra procurada: "%s"' % string_buscada)
    print('Tempo de indexacao: \t\t\t    %f' % (tempo_index - inicio))
    print("trie busca: resultados: %s, tempo: %f" % (len(registro1), end - tempo_index))
    

if __name__ == "__main__":
    main()
