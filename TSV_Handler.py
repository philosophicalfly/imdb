import csv
import subprocess
import Media
import sys
import json

from os import system

rawPath = 'data/raw/'
basePath = 'data/base/'
tsvPath = 'data/tsv/'
tsvFile = 'data40.tsv'



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
def importTSV(mediaList):
    isHeader = True
    system("clear")

    print ("CSV files to chose: ")
    result = subprocess.run(['ls', str(tsvPath)], stdout=subprocess.PIPE).stdout.decode('utf-8')
    listOfFiles = result[:-1].split('\n')
    for file in listOfFiles:
        print (file)
    tsvFile = input('Digite o TSV a ser importado: ')

    rawId = open(str(rawPath+'id'),'wb')
    rawType = open(str(rawPath+'type'),'wb')
    rawPryTitle = open(str(rawPath+'pryTitle'),'wb')
    rawOriTitle = open(str(rawPath+'oriTitle'),'wb')
    rawIsAdult = open(str(rawPath+'isAdult'),'wb')
    rawStartYear = open(str(rawPath+'startYear'),'wb')
    rawEndYear = open(str(rawPath+'endYear'),'wb')
    rawRuntime = open(str(rawPath+'runtime'),'wb')
    rawGenres = open(str(rawPath+'genres'),'wb')

    rawList = [rawId, rawType, rawPryTitle, rawOriTitle, rawIsAdult, rawStartYear, rawEndYear, rawRuntime, rawGenres]
    
    with open(tsvPath+tsvFile) as tsvfile:
        reader = csv.reader(tsvfile, delimiter='\t')
        for row in reader:
            if isHeader:
                isHeader = False
            else:
                if len(row) < 9:
                    lineId = bytes(str(str([row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],'Null'])+'\n').encode('utf8'))
                    lineGenres = bytes((str(['Null',row[0]])+'\n').encode('utf8'))
                else:
                    lineId = bytes(str(str([row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8]])+'\n').encode('utf8'))
                    lineGenres = bytes((str([row[8],row[0]])+'\n').encode('utf8'))
                lineType = bytes((str([row[1],row[0]])+'\n').encode('utf8'))
                linePryTitle = bytes((str([row[2],row[0]])+'\n').encode('utf8'))
                lineOriTitle = bytes((str([row[3],row[0]])+'\n').encode('utf8'))
                lineIsAdult = bytes((str([row[4],row[0]])+'\n').encode('utf8'))
                lineStartYear = bytes((str([row[5],row[0]])+'\n').encode('utf8'))
                lineEndYear = bytes((str([row[6],row[0]])+'\n').encode('utf8'))
                lineRuntime = bytes((str([row[7],row[0]])+'\n').encode('utf8'))
                
                lineList = [lineId,lineType,linePryTitle,lineOriTitle,lineIsAdult,lineStartYear,lineEndYear,lineRuntime,lineGenres]

                for rawInstance, lineInstance in zip(rawList, lineList):
                    rawInstance.write(lineInstance)

    rawId.close()
    rawType.close()
    rawPryTitle.close()
    rawOriTitle.close()
    rawIsAdult.close()
    rawStartYear.close()
    rawEndYear.close()
    rawRuntime.close()
    rawGenres.close()

#sortData()
# ordena os dados de cada arquivo em data/raw 
# e coloca-os ordenados em data/base, com os mesmos nomes
#TODO: ordenar os dados utilizando o HD, pois
#      o ordenamento ainda está sendo feito em memória. 
def sortData():
    rawId = open(str(rawPath+'id'),'rb')
    rawType = open(str(rawPath+'type'),'rb')
    rawPryTitle = open(str(rawPath+'pryTitle'),'rb')
    rawOriTitle = open(str(rawPath+'oriTitle'),'rb')
    rawIsAdult = open(str(rawPath+'isAdult'),'rb')
    rawStartYear = open(str(rawPath+'startYear'),'rb')
    rawEndYear = open(str(rawPath+'endYear'),'rb')
    rawRuntime = open(str(rawPath+'runtime'),'rb')
    rawGenres = open(str(rawPath+'genres'),'rb')
    rawList = [rawId, rawType, rawPryTitle, rawOriTitle, rawIsAdult, rawStartYear, rawEndYear, rawRuntime, rawGenres]
    baseId = open(str(basePath+'id'),'wb')
    baseType = open(str(basePath+'type'),'wb')
    basePryTitle = open(str(basePath+'pryTitle'),'wb')
    baseOriTitle = open(str(basePath+'oriTitle'),'wb')
    baseIsAdult = open(str(basePath+'isAdult'),'wb')
    baseStartYear = open(str(basePath+'startYear'),'wb')
    baseEndYear = open(str(basePath+'endYear'),'wb')
    baseRuntime = open(str(basePath+'runtime'),'wb')
    baseGenres = open(str(basePath+'genres'),'wb')
    baseList = [baseId,baseType,basePryTitle,baseOriTitle,baseIsAdult,baseStartYear,baseEndYear,baseRuntime,baseGenres]
    
    for raw,base in zip(rawList,baseList):
        content = raw.readlines()
        raw.close()
        content.sort(key=lambda x:x[2:])
        for line in content:
            #print(line)
            base.write(line)
        base.close()

#TODO: extender os arquivos importados e reordenar
def extendTSV(mediaList):
    return 0

def main():
    print("Call gui.py")
    importTSV()
    exit()

if __name__ == "__main__":
    main()