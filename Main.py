import subprocess
import TSV_Handler
import Base_Handler
import Finders
from os import system
from pprint import pprint
import ast

TSV_PATH = 'data/tsv/'


def __init__():
    return 0

def printMenu():
    system("clear")
    print ("1 - Importar nova base de dados TSV")
    print ("2 - Busca Simples")
    print ("3 - Adicionar extensão de dados TSV")
    print ("4 - Busca Ordenada Completa")
    print ("0 - Sair")

def printFooter():
    print ("\nDigite qualquer coisa pra continuar.")
    input()

def getMenuOption():
    try:
        opcao = int(input("Selecione a opção desejada: "))
    except ValueError:
        print ("\nNão foi possível selecionar essa opção. Saindo do programa.")
        exit()
    return opcao

def show10in10(listOfIds):
    system('clear')
    print ('Resultados:\n')
    for i, ids in enumerate(listOfIds):
        if((i != 0 and i % 10 == 0)):
            print("\nENTER: Mais Resultados.")
            isOut = input('    S: Sair.')
            system('clear')
            print ('Resultados:\n')
            if(isOut == 'S'):
                return 0
        selected = Base_Handler.select(str(ids))
        print (ast.literal_eval(selected)[2])

def showOrdered(listOfIds):
    listaDeFilmes = []
    system('clear')
    for ids in listOfIds:
        listaDeFilmes.append(ast.literal_eval(Base_Handler.select(str(ids))))
    system("clear")
    print ("1 - Ordem Normal")
    print ("2 - Ordenar Inversa")
    if input("Digite a ordem escolhida: ") == '1':
        listaDeFilmes.sort(key=lambda x:x[2])
    else:
        listaDeFilmes.sort(key=lambda x:x[2], reverse=True)
    for filme in listaDeFilmes:
        system('clear')
        print ('Resultados:\n')
        print ("Titulo Principal: "+filme[2])
        print ("Titulo Original:  "+filme[3])
        print ("Tipo:             "+filme[1])
        print ("Ano:              "+filme[5])
        print("Pressione ENTER para continuar...")
        if input("\nS - Sair. ") == 'S':
            return
        
def get_tsv_file_choice():
    system("clear")
    print("\nLista de arquivos TSV para importação:\n")
    result = subprocess.run(['ls', str(TSV_PATH)], stdout=subprocess.PIPE).stdout.decode('utf-8')
    list_of_files = result[:-1].split('\n')
    for file in list_of_files:
        print(file)
    tsv_filename = input('\nDigite o TSV a ser importado: ')
    if tsv_filename not in list_of_files:
        print('\nNome de arquivo invalido.')
        return None
    return tsv_filename

def main():
    TSV_Handler.enforce_required_folder_structure()
    mediaList = []
    todo=-1
    #listOfFiles = ['id', 'type', 'pryTitle', 'oriTitle', 'isAdult', 'startYear', 'endYear', 'runtime', 'genres']
    while todo != 0:
        printMenu()
        todo = getMenuOption()
        if todo == 1:
            tsv_filename = get_tsv_file_choice()
            if tsv_filename != None:
                print("\nRealizando importação... Operação pode ser demorada.")
                TSV_Handler.importTSV(mediaList, tsv_filename)
                print("\nImportação finalizada.")
            # TODO (maybe?): ajustar ordenacao para considerar ordem numerica em vez de alfabetica quando relevante
            #               vide arquivo 'runtime', onde '45' estah vindo depois de '4' e antes de '5'
            print("\nRealizando ordenação... Operação pode ser demorada.")
            #TSV_Handler.sortDataInMemory()
            TSV_Handler.sortFiles()
            print("\nOrdenação finalizada.")
        elif todo == 2:
            value = input('Digite uma palavra do nome do filme: ')
            selectedIds = Finders.getIdFromTrie(value)
            #selectedIds = Base_Handler.getIdOf(value,base)
            show10in10(selectedIds)
        elif todo == 3:
            tsv_filename = get_tsv_file_choice()
            if tsv_filename != None:
                print("\nRealizando extensao dos dados com reordenacao... operacao pode ser bem demorada.")
                TSV_Handler.extendTSV(mediaList, tsv_filename)
                TSV_Handler.sortFiles()
                print("\nExtensao finalizada.")
        elif todo == 4:
            value = input('Digite uma palavra do nome do filme: ')
            selectedIds = Finders.getIdFromTrie(value)
            #selectedIds = Base_Handler.getIdOf(value,base)
            showOrdered(selectedIds)
            
        else:
            if todo == 0:
                system('clear')
                exit()
            else:
                print ("Inválido.")
        printFooter()
    exit()

if __name__ == "__main__":
    main()