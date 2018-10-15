import subprocess
import TSV_Handler
import Base_Handler
from os import system

def __init__():
    return 0

def printMenu():
    system("clear")
    print ("1 - Importar nova base de dados CSV")
    print ("2 - Ordenar database")
    print ("3 - Selecionar")
    print ("4 - Adicionar extensão de dados CSV")
    print ("0 - Sair")

def printFooter():
    print("\nDigite qualuqer coisa para continuar")
    input()

def getMenuOption():
    try:
        opcao = int(input("Selecione a opção desejada: "))
    except ValueError:
        print ("Não foi possível selecionar essa opção. Saindo do programa.")
        exit()
    return opcao

def main():
    mediaList = []
    todo=-1
    while todo != 0:
        printMenu()
        todo = getMenuOption()
        if todo == 1:
            TSV_Handler.importTSV(mediaList)
        elif todo == 2:
            TSV_Handler.sortData()
        elif todo == 3:
            base = input('Digite a Base: ')
            value = input('Digite o Valor: ')
            selectedIds = Base_Handler.getIdOf(value,base)
            for ids in selectedIds:
                selected = Base_Handler.select(str(ids))
                print (selected[:-1])
        elif todo == 4:
            addCSV()
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