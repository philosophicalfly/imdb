#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import ast
import json
import time
import pickle

basePath = 'data/base/'
indexPath = 'data/indexes/'

DEPTH = 2  #  Profundidade da arvore quase trie de indices

#  def: an register is an tuple with the format:
#  [ string: "titulo" , string: "Id" ]

base_indice = {
	'registros' : [],
	'indice' : {}
}


# Funcao do Bardini
def getPryTitleList(value, base):
    idList = []
    with open(basePath+str(base), 'r') as baseFile:
        for line in baseFile:
            lineValue = ast.literal_eval(line)[0]
            if value.lower() in lineValue.lower():
                idList.append([lineValue, ast.literal_eval(line)[1]])
    return idList


def makeIndexTitle(listTitles):
	"""
	listTitles: list( ["titulo","Id"] )
	A partir de uma lista de ["titulo","Id"] cria e retorna um indice 
	usando 	uma arvore "try"(?) de profundidade definida globalmente,
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
	Adiciona um register(titulo, id) a arvore trie de indices existente
	"""
	length = len(register[0])
	#  loop pra percorrer todos os caracters do titulo
	for index in range(length):
		level = indice
		# loop para adicionar os caracters seguintes ao procurado
		i = 0
		#while(i < DEPTH):
		while(i<DEPTH and index+i<length):	# otimizacao, diminuiu de 23.8 minutos para 22.7 minutos
		#for i in range(DEPTH):
			#if index+i >= length:
			#	break
			letra = register[0][index+i].lower()
			"""
			try:
				letra.encode('utf8')
			except Exception as e:
				print e
				print register
			"""

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
	level['registros'] = []
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
	

def count_registers(soma, depth, indice):
	"""
	Conta o número de indices e de registros em cada um dos niveis da arvore, recursivamente
	"""
	if len(indice) != 0:
		soma[depth]['indices'] += len(indice)

	for key, value in indice.items():
		if 'indice' in value:
			count_registers(soma, depth+1, value['indice'])

		if 'registros' in value:
			soma[depth]['registros'] += len(value['registros'])
	

def quantidade_registros(indice):
	"""
	conta o numero de indices e registros em cada um dos niveis da arvore,
	retorna uma lista de dicionarios{'registros','indices'}
	"""

	contabilidade = []
	for i in range(DEPTH):
		contabilidade.append( {'registros':0, 'indices':0 } )
	count_registers(contabilidade, 0, indice)

	for level in range(len(contabilidade)):
		print('Numero de indices no level %s: %s' % (level, contabilidade[level]['indices']))
		print('Numero de registros no level %s: %s\n' % (level, contabilidade[level]['registros']))
	return contabilidade


def main():
	string_buscada = 'wa'
	inicio = time.time()
	#lista = getPryTitleList('', 'pryTitle')
	lista = []
	with open(basePath+str('pryTitle'), 'r') as baseFile:
		for line in baseFile:
			lista.append([ast.literal_eval(line)[0].decode('utf8'), ast.literal_eval(line)[1]])
	indice = makeIndexTitle(lista)

	print lista[0]
	#print(json.dumps(indice, sort_keys=True, indent=4))
	tempo_index = time.time()
	registro1 = searchIdFromTitle(indice, string_buscada)
	#print(json.dumps(registro1, indent=2))
	end1 = time.time()

	registro2 = getPryTitleList(string_buscada, 'pryTitle')
	#print(json.dumps(registro2, indent=2))
	end2 = time.time()

	print('Numero de registros: %s' % len(lista))
	print('Palavra procurada: "%s"' % string_buscada)
	print('Tempo de indexacao: \t\t\t    %f' % (tempo_index - inicio))
	print("trie   busca: resultados: %s, tempo: %f" % (len(registro1), end1 - tempo_index))
	print("linear busca: resultados: %s, tempo: %f" % (len(registro2), end2 - end1))

	#print(indice)	
	ind_json = json.dumps(indice)

	###  Salvando indice no disco para acesso posterior  ###
	with open(indexPath + 'indice', mode='wb') as arq:
		arq.write(json.dumps(indice))
		#arq.write( pickle.dumps(indice))

	print('save complete')

	###  recuperando do disco os indices para acesso posterior
	tempo1 = time.time()
	with open(indexPath + 'indice', 'rb') as arq:
		res = arq.readlines()[0]
		print('size: %s' % len(res))
		try:
			res = json.loads(res)
		except Exception as e:
			print 'error'
			print e
			print e.args	
	tempo2 = time.time()
	print('Tempo de carregar do\narquivo para a memoria: \t\t\t%f' % (tempo2 - tempo1))

	quantidade_registros(indice)


if __name__ == "__main__":
	main()