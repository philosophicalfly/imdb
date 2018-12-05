# IMDB

# Trabalho de Classificação e Pesquisa de Dados

# RUNNING 

Para executar o programa, o usuário deve entrar na pasta imdb e executar o script imdb.sh (se necessário, alterar as permissões da pasta inteira para permitir execução). O script chama inicialmente um cleaner, que limpa bases de dados anteriores existentes e, logo após isso, executado programa principal, em python3. (Pode ser necessária a instalação do python3 antes de executar o programa).
Ao ser executado o programa principal, o usuário se depara com 4 opções no menu principal, e números para navegação. Na primeira execução, o usuário DEVE selecionar o número 1 e importar uma base de dados. Junto com o programa, foram fornecidas 2 bases de dados, dados.tsv, e extensao.tsv; seleciona-se então a base de dados desejada (para fins de teste, usar dados.tsv.) O processo de importação e ordenação de dados, juntamente com o de criação da árvore de prefixos inicia-se, e o usuário deve esperar até o final do processo.
Após terminados os processos de importação, o usuário volta à tela inicial. Nesse momento, há possibilidade de importar uma extensão de dados, pesquisar rapidamente por um filme, ou pesquisar detalhadamente por um filme. 
No caso de o usuário fazer uma pesquisa simples, deve selecionar o item 2 e, logo após isso, digitar uma palavra existente no título de seu filme. O sistema então devolve uma lista de filmes e o usuário pode apertar Enter para paginar, ou S seguido de Enter para sair da visualização e voltar ao menu principal.
No caso de o usuário estender sua base de dados, deve selecionar o item 3, e realizar um processo semelhante ao de importação, escolhendo uma base de dados para ser adicionada ao banco de dados (para fim de testes, usar extensao.tsv).
No caso de o usuário fazer uma pesquisa detalhada, deve selecionar o item 4 e, logo após isso, digitar uma palavra existente no título de seu filme. O sistema então devolve os formatos de ordenação possíveis para as pesquisas, que são 1: ordem alfabética normal e 2: ordem alfabética inversa. Então o usuário digita o número de seu desejo e o sistema retorna dados detalhados de cada filme na ordem que o usuário desejou. Para paginar entre os filmes o usuário deve apertar Enter, para sair e voltar ao menu principal, o usuário deve apertar S seguido de Enter.
No caso de o usuário querer sair do sistema, deve selecionar o ítem 0.


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
