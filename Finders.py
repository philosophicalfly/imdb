#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import ast
import logging as log
import time
import subprocess
import json

import collections
DEPTH = 2  #  Profundidade da arvore trie


# Antes de usar qualquer coisa daqui,
# Execute o script tester.py
# insira a base de dados & ordene ela


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
    log.propagate = False
    # Must be greater than the maximum length of any line.
    log.debug(' Serching for '+str(matchvalue))
    log.debug('          in  '+str(filename))
    log.debug('w/ parameter  '+str(matchvalue[-3:]))

    max_line_len = 2 ** 12
    log.debug(' Max lenght of Line: '+str(max_line_len))
    start = pos = 0
    end = os.path.getsize(filename)
    log.debug(' End of File = ' + str(end)+' bytes')
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
            log.debug('lastmin = '+ str(lastMin))
            log.debug(' Start: |  '+ str(start))
            log.debug(' End  : |  '+ str(end))
            last = pos
            pos = start + ((end - start) // 2)
            fptr.seek(pos)
            
            # Move the cursor to a newline boundary.
            fptr.readline()
            line = fptr.readline().decode('utf8')
            linevalue = key(line)
            log.debug(' Line == Match | '+ str(linevalue) + ' = '+ str(matchvalue))
            log.debug(' Pos  == Last  | '+ str(pos) + ' = '+ str(last))
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
                    log.debug('End  = '+str(end))
                    log.debug('Fptr = '+str(fptr.tell()))
                    log.debug(counter)
                    counter += 1  
                    line = fptr.readline().decode('utf8')
                    linevalue = key(line)     
                    if matchvalue == linevalue:
                        log.debug('Repeats = '+str(counter))
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
    

def searchIdinTrie(index, string):
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


# New Struct Data, the classic Trie, using dicts instead of struct with pointers
def addInfoToTrie(chave, id, trie):
    """
    Adiciona uma chave apontando para um id na árvore trie dada.
    a chave é quebrada em várias chaves separadas pelos espaços.
    """
    key_list = chave.split(" ")

    for key in key_list:
        lenght = len(key)
        if lenght < 3:
            continue

        key = key.lower()
        level = trie
        i = 0

        while i < lenght:
            if key[i] not in level:
                level[ key[i] ] = dict()
            level = level[ key[i] ]
            i = i + 1

        if 'info' not in level:
            level['info'] = [id]
        else:
            level['info'].append(id)
    return trie


def searchInfoInTrie(chave, trie):
    """
    Retorna uma lista com os resultados que contenham todas as palavras da
    chave recebida, menos as palavras com até 2 letras.
    """
    search_result = []

    key_list = chave.lower().split(" ")    
    for key in key_list:
        i = 0
        lenght = len(key)
        #  possivelmente stopword ( ex. 'do', 'da', 'at', 'in')
        level = trie
        find = True

        while i < lenght and find:
            if key[i] in level:
                level = level[ key[i] ]
                i = i+1
            else:
                find = False
        
        if key[-1] == '*':
            #  TODO: selecionar todos os resultados a partir desse nodo
            log.debug('Union in the search for Prefix:')
            search_result.append( unionAllTrie( level ))
        elif find:
            if 'info' in level:
                search_result.append( level['info'] )      

    #  TODO: intersection between the results
    print('\nresults:\n%s' % search_result)
    return search_result


def unionAllTrie(trie):
    """
    Une todos os registros guardados na TRIE recebida em uma única lista
    return: lista,
    """
    results = []
    if 'info' in trie:
        results = trie['info']

    for key in trie:
        if key != 'info':
            results.extend( unionAllTrie( trie[key] ))
    return results


def saveFirstTrie(address, trie):
    """
    Salva a trie como ela está no local especificado
    Não se preocupa se há outra trie ĺá ou não
    """
    with open(address, mode='wb') as arq:
	   # Transform the struct Trie ( that use Dicts ) in JSON format,
	   # encode the string in Bytes of format 'utf-8' 
	   # and save in byte file
        json_string = json.dumps(trie)
        encode_string = json_string.encode( encoding='utf-8' )
        arq.write( encode_string )
    log.info('Save Trie in disk complete')


def loadTrie(address):
    """
    Carrega toda a trie na memória
    """
    with open(address, mode='rb') as arq:
        encode_string = arq.read()
        json_string = encode_string.decode( encoding='utf-8' )
        trie = json.loads(json_string)
    return trie


def test_prefix_tree():
    log.basicConfig(level='DEBUG', format='%(funcName)10s[%(lineno)d]: %(msg)s')
    log.debug('DEBUG')
    log.info('INFO')
    log.warn('WARN')
    log.error('ERROR')
    print('LOGS /\\')

    # Loading raw data after the slicing by fields of the TSV files 
    raw_pryTitle = []
    with open('data/raw/pryTitle', 'r') as baseFile:
        for line in baseFile:
            raw_pryTitle.append([ast.literal_eval(line)[0], ast.literal_eval(line)[1]])
    
    # Creating and adding data in the trie
    trie = dict()
    for reg in raw_pryTitle:
        addInfoToTrie(reg[0], reg[1], trie)
    
    saveFirstTrie('data/indice_pryTitle', trie)

    # Testando a trie, buscando por um prefixo e usando wildcard
    search_results = searchInfoInTrie('r*', trie)
    lista_resumida = []
    for lista_results in search_results:
        for result in lista_results:
            if result not in lista_resumida:
                lista_resumida.append(result)

    log.info('Resultados: ')
    for titulo_id in raw_pryTitle:
        if titulo_id[1] in lista_resumida:
            log.info('[%s]-> %s' % (titulo_id[1], titulo_id[0]))
    

    # testando o carregamento do disco para memória da trie
    log.info('Loading trie')
    loadedTrie = loadTrie('data/indice_pryTitle')
    log.info('\n')

    


def test_almost_trie():
    """
    Teste da arvore quase trie de indices
    """

    string_buscada = 'wa'
    inicio = time.time()
    
    #lista = getPryTitleList('', 'pryTitle')
    lista = []
    with open('data/raw/pryTitle', 'r') as baseFile:
        for line in baseFile:
            lista.append([ast.literal_eval(line)[0], ast.literal_eval(line)[1]])
    indice = makeIndexTitle(lista)
    
    index_time = time.time()
    registro1 = searchIdinTrie(indice, string_buscada)
    
    end_time = time.time()

    print('Numero de registros: %s' % len(lista))
    print('Palavra procurada: "%s"' % string_buscada)
    print('Tempo de indexacao: \t\t\t    %f' % (index_time - inicio))
    print("trie busca: resultados: %s, tempo: %f" % (len(registro1), end_time - tempo_index))


def test_binaryFind():
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


#Utilidade unica para testes
def main():
    # arvore com apenas o inicio das palavras
    test_prefix_tree()

    # arvore com todas as partes das palavras.
    #test_almost_trie()

    # busca binária em um arquivo
    #test_binaryFind()
    

if __name__ == "__main__":
    main()
