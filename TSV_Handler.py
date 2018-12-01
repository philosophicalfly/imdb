import csv
import subprocess
from Media import Media
import Base_Handler
import Finders
import sys
import json
import time

from os import system

RAW_PATH = 'data/raw/'
BASE_PATH = 'data/base/'
TSV_PATH = 'data/tsv/'
TSV_FILE = 'data40.tsv'
TEMP_PATH = 'data/temp/'


#importTSV(mediaList)
# importa uma base do tipo 'title.basics.tsv' do imdb
# para arquivos distintos que representam cada coluna do TSV.
# esses arquivos ficam em /data/raw
# Ou seja, cada coluna da tabela: 
#   (id, type, pryTitle, oriTitle, isAdult, startYear, endYear, runtime, genres)
# vira um arquivo com esse mesmo nome em /data/raw
#   Ex: data/raw/type,  data/raw/pryTitle,  data/raw/isAdult
# Todos os arquivos gerados são organizados da seguinte forma:
#   Para cada linha, é feita uma lista "stringalizada" que contém ['dado', 'id']
#   Ex: ['The Arrival of a Train', 'tt0000012'], para o arquivo pryTitle
#       ['short', 'tt0000012'], para o arquivo type 
#   esses dados são salvos de forma binária nos arquivos.
#   essa "strring de lista" pode ser retransformada em lista com a biblioteca 'ast'
# 
# Há uma excessão para os arquivos, o arquivo 'id'. Esse arquivo contém todos os dados
# completos da mesma forma que o TSV original, porém na forma de lista.
#   Ex: ['tt0000012', 'short', 'The Arrival of a Train', "L'arrivée d'un train à La Ciotat", '0', '1896', '\\N', '1', 'Documentary,Short']
# TODO: verificar o que seria o parametro mediaList e se realmente precisamos dele
def importTSV(mediaList, tsv_filename):
    is_header = True

    raw_list = _get_list_of_raw_files('wb')

    with open(TSV_PATH+tsv_filename) as tsvFile:
        reader = csv.reader(tsvFile, delimiter='\t')
        for row in reader:
            if is_header:
                is_header = False
            else:
                media = _create_media_from_row(row)
                line_list = _get_list_of_filled_rows_to_insert(media)
                for raw_instance, line_instance in zip(raw_list, line_list):
                    raw_instance.write(line_instance)

    for raw_file in raw_list:
        raw_file.close()


#sortDataInMemory()
# ordena os dados de cada arquivo em data/raw 
# e coloca-os ordenados em data/base, com os mesmos nomes
#TODO: ordenar os dados utilizando o HD, pois
#      o ordenamento ainda está sendo feito em memória. 
def sortDataInMemory():
    rawId = open(str(RAW_PATH + 'id'), 'rb')
    rawType = open(str(RAW_PATH + 'type'), 'rb')
    rawPryTitle = open(str(RAW_PATH + 'pryTitle'), 'rb')
    rawOriTitle = open(str(RAW_PATH + 'oriTitle'), 'rb')
    rawIsAdult = open(str(RAW_PATH + 'isAdult'), 'rb')
    rawStartYear = open(str(RAW_PATH + 'startYear'), 'rb')
    rawEndYear = open(str(RAW_PATH + 'endYear'), 'rb')
    rawRuntime = open(str(RAW_PATH + 'runtime'), 'rb')
    rawGenres = open(str(RAW_PATH + 'genres'), 'rb')
    rawList = [rawId, rawType, rawPryTitle, rawOriTitle, rawIsAdult, rawStartYear, rawEndYear, rawRuntime, rawGenres]
    baseId = open(str(BASE_PATH + 'id'), 'wb')
    baseType = open(str(BASE_PATH + 'type'), 'wb')
    basePryTitle = open(str(BASE_PATH + 'pryTitle'), 'wb')
    baseOriTitle = open(str(BASE_PATH + 'oriTitle'), 'wb')
    baseIsAdult = open(str(BASE_PATH + 'isAdult'), 'wb')
    baseStartYear = open(str(BASE_PATH + 'startYear'), 'wb')
    baseEndYear = open(str(BASE_PATH + 'endYear'), 'wb')
    baseRuntime = open(str(BASE_PATH + 'runtime'), 'wb')
    baseGenres = open(str(BASE_PATH + 'genres'), 'wb')
    baseList = [baseId,baseType,basePryTitle,baseOriTitle,baseIsAdult,baseStartYear,baseEndYear,baseRuntime,baseGenres]
    
    for raw,base in zip(rawList,baseList):
        content = raw.readlines()
        raw.close()
        content.sort(key=lambda x:x[2:])
        for line in content:
            #print(line)
            base.write(line)
        base.close()


def sortFiles():
    listOfFiles = ['id', 'type', 'pryTitle', 'oriTitle', 'isAdult', 'startYear', 'endYear', 'runtime', 'genres']
    for instance in listOfFiles:
        sortFile(instance)
#sortFile()
# ordena os dados de um único arquivo em data/temp utilizando
# um merge sort no disco rígido
def sortFile(fileName):
    #PEGA TAMANHO DO ARQUIVO INTEIRO
    #TODO: Substituir para um indice de tamanhos
    unsorted = open(str(RAW_PATH + fileName), 'rb')
    for size, instance in enumerate(unsorted):
        pass
    unsorted.close()

    #Chama o criador do 8 primeiros chunks
    createFiles(fileName, size//7, 8)


#createFiles(qtdLines, qtdFiles):
# cria o primeiro pack de chunks do arquivo principal
# aqui estou separando tudo em 8 chunks
# ao criar um chunk, ordena ele em meória
# ao final da função, tem-se 8 chunks ordenados separadamente
# e chama-se a função unifyFiles 
def createFiles(fileName, qtdLines, qtdFiles):
    content = []
    with open(str(RAW_PATH+fileName), 'rb') as unsorted:
        for i in range(0,qtdFiles):
            with open(str(TEMP_PATH+ 'temp-'+str(qtdFiles)+ '-'+str(i)), 'wb') as base8:
                for qtd in range(0,qtdLines):
                    content.append(unsorted.readline())
                content.sort(key=lambda x:x[2:])
                for line in content:
                    base8.write(line)
            content = []
    unifyFiles(fileName, 8)


#unifyFiles(numFiles):
# pega os 8 chunks anteriormente feitos e
# recursivamente juntando os arquivos pequenos, linha a linha, 
# em arquivos maiores, até que só haja um arquivo novamente
def unifyFiles(fileName, numFiles):
    toWrite = []
    i = 0
    if numFiles == 1:
        result = subprocess.run(['mv', str(TEMP_PATH) + 'temp-1-0', str(BASE_PATH) + str(fileName)], stdout=subprocess.PIPE).stdout.decode('utf-8')
        result = subprocess.run(['rm', '-r', str(TEMP_PATH)], stdout=subprocess.PIPE).stdout.decode('utf-8')
        result = subprocess.run(['mkdir', str(TEMP_PATH)], stdout=subprocess.PIPE).stdout.decode('utf-8')
        return
    while i < numFiles:
        file0 = open(str(TEMP_PATH + 'temp-' + str(numFiles) + '-' + str(i)), 'rb')
        file1 = open(str(TEMP_PATH + 'temp-' + str(numFiles) + '-' + str(i + 1)), 'rb')
        line0 = file0.readline()
        line1 = file1.readline()
        with open(str(TEMP_PATH+ 'temp-'+str(numFiles//2)+ '-'+str((i+1)//2)), 'wb') as base8:
            while line0 and line1:
                if (line0[2:] <= line1[2:]):
                    base8.write(line0)
                    #print ('Escreveu 0' + str(line0))
                    #time.sleep(0.2)
                    line0 = file0.readline()
                    if not line0:
                        line0 = file1.readline()
                elif (line0[2:] >= line1[2:]):
                    base8.write(line1)
                    #print ('Escreveu 1' + str(line1))
                    #time.sleep(0.2)
                    line1 = file1.readline()
                    if not line1:
                        line1 = file0.readline()
            base8.write(line0)
            base8.write(line1)
        i += 2        
    unifyFiles(fileName, numFiles//2)


# TODO: extender os arquivos importados e reordenar
def extendTSV(mediaList, tsv_filename):
    is_header = True

    raw_list = _get_list_of_raw_files('ab')

    with open(TSV_PATH+tsv_filename) as tsv_file:
        reader = csv.reader(tsv_file, delimiter='\t')
        for row in reader:
            if is_header:
                is_header = False
            else:
                media = _create_media_from_row(row)
                already_exists = _media_already_exists(media)
                if not already_exists:
                    line_list = _get_list_of_filled_rows_to_insert(media)
                    for raw_instance, line_instance in zip(raw_list, line_list):
                        raw_instance.write(line_instance)

    for raw_file in raw_list:
        raw_file.close()

    sortFiles()
    return 0


def _create_media_from_row(row):
    if len(row) < 9:
        media = Media(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], 'Null')
    else:
        media = Media(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8])
    return media


def _get_list_of_raw_files(mode):
    rawId = open(str(RAW_PATH + 'id'), mode)
    rawType = open(str(RAW_PATH + 'type'), mode)
    rawPryTitle = open(str(RAW_PATH + 'pryTitle'), mode)
    rawOriTitle = open(str(RAW_PATH + 'oriTitle'), mode)
    rawIsAdult = open(str(RAW_PATH + 'isAdult'), mode)
    rawStartYear = open(str(RAW_PATH + 'startYear'), mode)
    rawEndYear = open(str(RAW_PATH + 'endYear'), mode)
    rawRuntime = open(str(RAW_PATH + 'runtime'), mode)
    rawGenres = open(str(RAW_PATH + 'genres'), mode)

    rawList = [rawId, rawType, rawPryTitle, rawOriTitle, rawIsAdult, rawStartYear, rawEndYear, rawRuntime, rawGenres]

    return rawList


def _get_list_of_filled_rows_to_insert(media):
    lineId = bytes(media.toCsvRow().encode('utf-8'))
    lineType = bytes((str([media.type, media.tconst]) + '\n').encode('utf8'))
    linePryTitle = bytes((str([media.priTitle, media.tconst]) + '\n').encode('utf8'))
    lineOriTitle = bytes((str([media.oriTitle, media.tconst]) + '\n').encode('utf8'))
    lineIsAdult = bytes((str([media.isAdult, media.tconst]) + '\n').encode('utf8'))
    lineStartYear = bytes((str([media.startYear, media.tconst]) + '\n').encode('utf8'))
    lineEndYear = bytes((str([media.endYear, media.tconst]) + '\n').encode('utf8'))
    lineRuntime = bytes((str([media.runtime, media.tconst]) + '\n').encode('utf8'))
    lineGenres = bytes((str([media.genres, media.tconst]) + '\n').encode('utf-8'))

    lineList = [lineId, lineType, linePryTitle, lineOriTitle, lineIsAdult, lineStartYear, lineEndYear, lineRuntime,
                lineGenres]

    return lineList


# TODO: Testar jeitos de melhorar isso
#       ex.: rever metodo de busca binaria em Finders.py
#       ex.: manter um arquivo de tconst's presentes e ordenados e fazer pesquisa binaria nele
#               (no caso de uma pesquisa binaria no arquivo id ficar muito ruim pelo excesso de informacoes nele)
def _media_already_exists(media):
    already_exists = False
    try:
        entry = Base_Handler.select(media.tconst)
        if entry != []:
            already_exists = True
    except:
        pass
    return already_exists


def main():
    print("Testing")
    listOfFiles = ['id', 'type', 'pryTitle', 'oriTitle', 'isAdult', 'startYear', 'endYear', 'runtime', 'genres']
    for instance in listOfFiles:
        sortFile(instance)
    exit()


if __name__ == "__main__":
    main()

