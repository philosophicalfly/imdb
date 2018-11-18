import ast
import Finders

rawPath = 'data/raw/'
basePath = 'data/base/'
tsvPath = 'data/tsv/'
tsvFile = 'data.tsv'

baseDict = {
    'id': 0,
    'type': 1,
    'prytitle': 2,
    'oriTitle': 3,
    'isAdult': 4,
    'startYear': 5,
    'endYear': 6,
    'runtime': 7,
    'genres': 8,
}


#linearIdFind(id):
# id = string
# retorna uma lisa com todos os dados de um filme da base
# a partiur do ID dado como parametro

def select(id):
    substring = lambda val: ast.literal_eval(val)[0]
    #está usando agora busca semi-binária
    return (Finders.binaryIdFind('data/base/id', str(id), substring)[0][:-1])

#selectId(id):
# id = string
# retorna uma lisa com todos os dados de um filme da base
# a partiur do ID dado como parametro
#TODO: temos que usar uma estrutura de dados específica no arquivo
#      eu acho legal usar uma arvore TRIE, o professor também citou ela,
#      provavelmente gostaria que usássemos
#      http://www.grantjenks.com/wiki/random/python_binary_search_file_by_line
def selectList(idList):
    listOfMedia = []
    with open(basePath+'id', 'r') as baseFile:
        for line in baseFile:
            lineId = str(ast.literal_eval(line)[0])
            if lineId in idList:
                listOfMedia.append(line)
    return listOfMedia


#getIdOf(value, base):
# valeu = string
# base  = string
# Retorna a lista de IDs relacionados ao valor passado de acordo com a base.
# Na relação, é verificado se o valor de parametro é substring de cada valor da base
# Ex:
# getIdOf('short', 'type') 
#   -> 'short' é o valor a ser procurado na tabela 'type'
#   -> retorna: ['tt0000001', 'tt0000002', ...... , 'tt0000099', 'tt0000100']
# getIdOf('Dessinateur', 'pryTitle')  
#   -> 'Dessinateur' é o valor a ser procurado na tabela 'pryTitle'
#   -> retorna ['tt0000063', 'tt0000064', 'tt0000065', 'tt0000066']
# esses ids podem ser depois utilizados na função selectId
# para pegar todos os dados de cada filme
#TODO: tornar a busca binária
#      http://www.grantjenks.com/wiki/random/python_binary_search_file_by_line
def getIdOf(value, base):
    idList = []
    with open(basePath+str(base), 'r') as baseFile:
        for line in baseFile:
            lineValue = ast.literal_eval(line)[0]
            if value.lower() in lineValue.lower():
                idList.append(ast.literal_eval(line)[1])
    #print (idList)
    return idList

#Utilidade única para testes
def main():
    selected = select(input('Digite o ID: '))
    print (selected)
    base = input('Digite a Base: ')
    value = input('Digite o Valor: ')
    selectedId = getIdOf(value,base)
    print (selected)

if __name__ == "__main__":
    main()
