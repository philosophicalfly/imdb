# IMDB

# Trabalho de Classificação e Pesquisa de Dados

# RUNNING 
* Rodar um ./cleaner.sh apos o git clone.
* Testar com python3 tester.py

# DEFINIÇÃO

FUNCIONALIDADES PREVISTAS:
* 1. Processamento e armazenamento binário de dados da principal fonte de dados*
do IMDB.
a. O armazenamento incremental será feito da seguinte forma: Para cada
colina do TSV principal, serão criados arquivos contendo ([dado da
coluna] + [id do filme]), que serão posteriormente ordenados por [dado
da coluna]. Além disso, será mantida uma tabela com todos os dados
ordenada por ID.
b. Além da extração inicial, será possível adicionar filmes
incrementalmente ao armazenamento categorizado do sistema. A
especificação é que eles estejam em formato TSV (conforme os iniciais),
com a mesma disposição de linhas e colunas da fonte inicial.
c. * O banco completo do IMDB conta com 6 fontes de dados, encontrados
aqui. Será utilizada em primeira instância a fonte “title.basics.tsv.gz”. No
caso de haver tempo útil para aprimoração, deseja-se incluir tabelas
alternativas para complementar o trabalho.
* 2. Ordenação alfabética e inversamente alfabética de cada filme.
a. A ordenação será feita utilizando external-sorting. No caso do grupo,
será feito um “External Multi-Way Merge Sort”, em que o arquivo
inicial (com mais de 9M linhas) será dividido em pequenos arquivos, que
serão ordenados em memória e intercalados novamente em arquivos
maiores de forma recursiva.
b. * No caso de haver tempo útil para aprimoração, deseja-se ordenar todos
os arquivos de cada parâmetro.
* 3. Seleção de filmes por tipo ou gênero.
a. A seleção deve ser feita a partir da verificação do tipo ou gênero na
tabela que contém todos os dados do filme.
* 4. Busca de filme por título principal*. A busca de filmes é feita em 2 passos:
a. Primeiro, A busca deve ser feita utilizando uma variação de árvore TRIE,
onde os dados serão categorizados em listas contendo ([nome do filme] ,
[id do filme]) nas folhas da árvore. A árvore será construída com as
primeiras letras de cada filme. Dentro das pequenas listas, será utilizada
busca binária para chegar ao ID do filme pesquisado.
b. Uma vez encontrado o ID do filme, este será utilizado com busca binária
na tabela que contém todos os dados ordenados por ID.
c. * No caso de haver tempo útil para aprimoração, deseja-se incluir a
busca por outros parâmetros.
