import subprocess
import TSV_Handler
import Base_Handler
from os import system
from pprint import pprint
import ast

TSV_PATH = 'data/tsv/'


def __init__():
    return 0

def printMenu():
    system("clear")
    print ("1 - Importar nova base de dados CSV")
    print ("2 - Ordenar database")
    print ("3 - Selecionar")
    print ("4 - Adicionar extensão de dados CSV")
    print ("5 - Remover um registro")
    print ("0 - Sair")

def printFooter():
    print ("\nDigite qualuqer coisa pra continuar.")
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
    listOfFiles = ['id', 'type', 'pryTitle', 'oriTitle', 'isAdult', 'startYear', 'endYear', 'runtime', 'genres']
    while todo != 0:
        printMenu()
        todo = getMenuOption()
        if todo == 1:
            tsv_filename = get_tsv_file_choice()
            if tsv_filename != None:
                print("\nRealizando importação... Operação pode ser demorada.")
                TSV_Handler.importTSV(mediaList, tsv_filename)
                print("\nImportação finalizada.")
        elif todo == 2:
            # TODO (maybe?): ajustar ordenacao para considerar ordem numerica em vez de alfabetica quando relevante
            #               vide arquivo 'runtime', onde '45' estah vindo depois de '4' e antes de '5'
            print("\nRealizando ordenação... Operação pode ser demorada.")
            #TSV_Handler.sortDataInMemory()
            TSV_Handler.sortFiles()
            print("\nOrdenação finalizada.")
        elif todo == 3:
            print('Bases disponíveis:')
            for i in listOfFiles:
                print(i)
            base = input('\nDigite a base na qual deseja pesquisar: ')
            if str(base) in listOfFiles:
                value = input('Digite o Valor: ')
                selectedIds = Base_Handler.getIdOf(value,base)
                show10in10(selectedIds)
            else:
                print("Base de dados inexistente.")
        elif todo == 4:
            tsv_filename = get_tsv_file_choice()
            if tsv_filename != None:
                print("\nRealizando extensao dos dados com reordenacao... operacao pode ser bem demorada.")
                TSV_Handler.extendTSV(mediaList, tsv_filename)
                print("\nExtensao finalizada.")
        elif todo == 5:
            id = input('Digite o id do registro: ')
            # Sanitização
            i=0
            while i < len(id):
                if id[i] == 't':
                    id = id[1:]
                    i = 0
                elif '0' <= id[i] and id[i] <= '9':
                    i += 1
                else:
                    id = input('ID não é válido. Digite um novo ID:')
                    i = 0
            
            # completing the ID
            id = 'tt' + '0' * (7 - len(id)) + id
                        
            print('id correto: %r' % id)
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