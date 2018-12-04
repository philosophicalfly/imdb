import csv
import subprocess
import shutil
import os
from Media import Media
import Base_Handler
import Finders
import sys
import json
import time
import ast
from os import system


RAW_PATH = 'data/raw/'
BASE_PATH = 'data/base/'
TSV_PATH = 'data/tsv/'
TSV_FILE = 'data40.tsv'
TEMP_PATH = 'data/temp/'
UPDATE_RAW_PATH = 'data/updateTemp/raw/'
UPDATE_BASE_PATH = 'data/updateTemp/base/'
MERGED_BASE_PATH = 'data/updateTemp/merged/'
REQUIRED_FOLDERS = [
    RAW_PATH,
    BASE_PATH,
    TSV_PATH,
    TEMP_PATH,
    UPDATE_RAW_PATH,
    UPDATE_BASE_PATH,
    MERGED_BASE_PATH
]


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

    raw_list = _get_list_of_raw_files(RAW_PATH, 'wb')

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
            print(line)
            base.write(line)
        base.close()
    return


def sortFiles(raw_path=RAW_PATH, base_path=BASE_PATH):
    listOfFiles = ['id', 'type', 'pryTitle', 'oriTitle', 'isAdult', 'startYear', 'endYear', 'runtime', 'genres']
    for instance in listOfFiles:
        if instance == 'pryTitle':
            createAndSaveTrie(raw_path, base_path, instance)
        else:
            sortFile(raw_path, base_path, instance)


def createAndSaveTrie(raw_path, base_path, fileName):
    trie = None
    try:
        trie = Finders.loadTrie(str(base_path+fileName))
    except:
        trie = dict()

    with open(str(raw_path+fileName), 'rb') as unsorted:
        for str_line in unsorted:
            str_decoded = str_line.decode(encoding='utf8')
            lista = ast.literal_eval(str_decoded)
            Finders.addInfoToTrie(chave=lista[0], info=lista[1], trie=trie)
    Finders.saveTrie(str(base_path+fileName), trie=trie)

#sortFile()
# ordena os dados de um único arquivo em data/temp utilizando
# um merge sort no disco rígido
def sortFile(raw_path, base_path, fileName):
    #PEGA TAMANHO DO ARQUIVO INTEIRO
    #TODO: Substituir para um indice de tamanhos
    unsorted = open(str(raw_path + fileName), 'rb')
    for size, instance in enumerate(unsorted):
        pass
    unsorted.close()

    #Chama o criador do 8 primeiros chunks
    createFiles(raw_path, base_path, fileName, size//7, 8)


#createFiles(qtdLines, qtdFiles):
# cria o primeiro pack de chunks do arquivo principal
# aqui estou separando tudo em 8 chunks
# ao criar um chunk, ordena ele em memória
# ao final da função, tem-se 8 chunks ordenados separadamente
# e chama-se a função unifyFiles 
def createFiles(raw_path, base_path, fileName, qtdLines, qtdFiles):
    content = []
    with open(str(raw_path+fileName), 'rb') as unsorted:
        for i in range(0,qtdFiles):
            with open(str(TEMP_PATH+ 'temp-'+str(qtdFiles)+ '-'+str(i)), 'wb') as base8:
                for qtd in range(0,qtdLines):
                    content.append(unsorted.readline())
                content.sort(key=lambda x:x[2:])
                for line in content:
                    base8.write(line)
            content = []
    unifyFiles(base_path, fileName, 8)


#unifyFiles(numFiles):
# pega os 8 chunks anteriormente feitos e
# recursivamente juntando os arquivos pequenos, linha a linha, 
# em arquivos maiores, até que só haja um arquivo novamente
def unifyFiles(base_path, fileName, numFiles):
    toWrite = []
    i = 0
    if numFiles == 1:
        result = subprocess.run(['mv', str(TEMP_PATH) + 'temp-1-0', str(base_path) + str(fileName)], stdout=subprocess.PIPE).stdout.decode('utf-8')
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
    unifyFiles(base_path, fileName, numFiles//2)


# TODO: extender os arquivos importados e reordenar
def extendTSV(mediaList, tsv_filename):
    is_header = True

    raw_list = _get_list_of_raw_files(UPDATE_RAW_PATH, 'ab')
    existing_raw_list = _get_list_of_raw_files(RAW_PATH, 'ab')

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
                    for raw_instance, existing_raw_instance, line_instance \
                            in zip(raw_list, existing_raw_list, line_list):
                        raw_instance.write(line_instance)
                        existing_raw_instance.write(line_instance)

    for raw_file in raw_list:
        raw_file.close()

    sortFiles(UPDATE_RAW_PATH, UPDATE_BASE_PATH)
    index_files = _get_list_of_index_file_names()
    for index_file in index_files:
        _merge_base_file(BASE_PATH + index_file, UPDATE_BASE_PATH + index_file,
                         MERGED_BASE_PATH + index_file)
    # doing two for loops so it will only move the files when we already have everything updated
    for index_file in index_files:
        shutil.move(MERGED_BASE_PATH + index_file, BASE_PATH + index_file)
        os.remove(UPDATE_RAW_PATH + index_file)
        os.remove(UPDATE_BASE_PATH + index_file)
    return 0


def _create_media_from_row(row):
    if len(row) < 9:
        media = Media(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], 'Null')
    else:
        media = Media(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8])
    return media


def _get_list_of_raw_files(path, mode):
    raw_id = open(str(path + 'id'), mode)
    raw_type = open(str(path + 'type'), mode)
    raw_pry_title = open(str(path + 'pryTitle'), mode)
    raw_ori_title = open(str(path + 'oriTitle'), mode)
    raw_is_adult = open(str(path + 'isAdult'), mode)
    raw_start_year = open(str(path + 'startYear'), mode)
    raw_end_year = open(str(path + 'endYear'), mode)
    raw_runtime = open(str(path + 'runtime'), mode)
    raw_genres = open(str(path + 'genres'), mode)

    raw_list = [raw_id, raw_type, raw_pry_title, raw_ori_title, raw_is_adult, raw_start_year, raw_end_year,
                raw_runtime, raw_genres]

    return raw_list


def _get_list_of_filled_rows_to_insert(media):
    line_id = bytes(media.toCsvRow().encode('utf-8'))
    line_type = bytes((str([media.type, media.tconst]) + '\n').encode('utf8'))
    line_pry_title = bytes((str([media.priTitle, media.tconst]) + '\n').encode('utf8'))
    line_ori_title = bytes((str([media.oriTitle, media.tconst]) + '\n').encode('utf8'))
    line_is_adult = bytes((str([media.isAdult, media.tconst]) + '\n').encode('utf8'))
    line_start_year = bytes((str([media.startYear, media.tconst]) + '\n').encode('utf8'))
    line_end_year = bytes((str([media.endYear, media.tconst]) + '\n').encode('utf8'))
    line_runtime = bytes((str([media.runtime, media.tconst]) + '\n').encode('utf8'))
    line_genres = bytes((str([media.genres, media.tconst]) + '\n').encode('utf-8'))

    line_list = [line_id, line_type, line_pry_title, line_ori_title, line_is_adult, line_start_year, line_end_year,
                 line_runtime, line_genres]

    return line_list


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


def _merge_base_file(file_path_one, file_path_two, destiny):
    file_one = open(file_path_one, 'rb')
    file_two = open(file_path_two, 'rb')
    line_one = file_one.readline()
    line_two = file_two.readline()
    with open(destiny, 'wb') as file_destiny:
        while line_one and line_two:
            if (line_one[2:] <= line_two[2:]):
                file_destiny.write(line_one)
                line_one = file_one.readline()
                if not line_one:
                    line_one = file_two.readline()
            elif (line_one[2:] >= line_two[2:]):
                file_destiny.write(line_two)
                line_two = file_two.readline()
                if not line_two:
                    line_two = file_one.readline()
        file_destiny.write(line_one)
        file_destiny.write(line_two)
    file_one.close()
    file_two.close()
    return


def _get_list_of_index_file_names():
    return ['id', 'type', 'pryTitle', 'oriTitle', 'isAdult', 'startYear', 'endYear', 'runtime', 'genres']


# TODO: move this to a more appropriate place
def enforce_required_folder_structure():
    for folder in REQUIRED_FOLDERS:
        if not os.path.exists(folder):
            os.makedirs(folder, exist_ok=True)

def main():
    print("Testing")
    enforce_required_folder_structure()
    sortFiles()
    exit()


if __name__ == "__main__":
    main()

