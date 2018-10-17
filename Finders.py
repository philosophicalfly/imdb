import os
import ast
import logging

#linearIdFind(id):
# id = string
# faz busca LINEAR e
# retorna uma liste com todos os dados de um filme da base
# a partiur do ID dado como parametro
def linearIdFind(filename, matchvalue, key=lambda val: val):
    with open('data/base/id', 'rb') as fptr:
        while fptr:
            line = fptr.readline().decode('utf8')
            if matchvalue == key(line):
                return(line)
            if matchvalue < key(line):
                return([])

#linearIdFind(id):
# id = string
# faz busca SEMI-BINÁRIA e
# retorna uma lista com todos os dados de um filme da base
# a partiur do ID dado como parametro
# obs: o código é uma adaptação minha de outro código das interwebs (que não funcionava)
def binaryIdFind(filename, matchvalue, key=lambda val: val):
    """
    Binary search a file for matching lines.
    Returns a list of matching lines.
    filename - path to file, passed to 'open'
    matchvalue - value to match
    key - function to extract comparison value from line
 
    >>> parser = lambda val: int(val.split('\t')[0].strip())
    >>> line_binary_search('sd-arc', 63889187, parser)
    ['63889187\t3592559\n', ...]
    """
    logging.propagate = False
    # Must be greater than the maximum length of any line.
    logging.debug(' Serching for '+str(matchvalue))
    logging.debug('          in  '+str(filename))
    logging.debug('w/ parameter  '+str(matchvalue[-3:]))

    max_line_len = 2 ** 12
    logging.debug(' Max lenght of Line: '+str(max_line_len))
    start = pos = 0
    end = os.path.getsize(filename)
    logging.debug(' End of File = ' + str(end)+' bytes')
    counter = 0
    lastMin = 0
    with open(filename, 'rb') as fptr:
        
        #verifica os dois primeiros
        line = fptr.readline().decode('utf8')
        linevalue = key(line)
        if linevalue == matchvalue:
            return([line])
        line = fptr.readline().decode('utf8')
        linevalue = key(line)
        if linevalue == matchvalue:
            return([line])
        fptr.seek(0)

        # Limit the number of times we binary search.
        for rpt in range(50):
            logging.debug('lastmin = '+ str(lastMin))
            logging.debug(' Start: |  '+ str(start))
            logging.debug(' End  : |  '+ str(end))
            last = pos
            pos = start + ((end - start) // 2)
            fptr.seek(pos)
            
            # Move the cursor to a newline boundary.
            fptr.readline()
            line = fptr.readline().decode('utf8')
            linevalue = key(line)
            logging.debug(' Line == Match | '+ str(linevalue) + ' = '+ str(matchvalue))
            logging.debug(' Pos  == Last  | '+ str(pos) + ' = '+ str(last))
            if linevalue == matchvalue or pos == last:
                #return(line)
                #print(line)
 
                # Seek back until we no longer have a match.
                while True:
                    fptr.seek(lastMin)
                    fptr.readline().decode('utf8')
                    if matchvalue != key(fptr.readline().decode('utf8')):
                        break
               # Seek forward to the first match.
                while fptr.tell() < end:
                    logging.debug('End  = '+str(end))
                    logging.debug('Fptr = '+str(fptr.tell()))
                    logging.debug(counter)
                    counter += 1  
                    line = fptr.readline().decode('utf8')
                    linevalue = key(line)     
                    if matchvalue == linevalue:
                        logging.debug('Repeats = '+str(counter))
                        break
                else:
                    # No match was found.
                    return []
                results = []
                while linevalue == matchvalue:
                    results.append(line)
                    line = fptr.readline().decode('utf8')
                    linevalue = key(line)
 
                return results
            elif linevalue < matchvalue:
                counter += 1
                lastMin = start
                start = fptr.tell()
            else:
                assert linevalue > matchvalue
                counter += 1                
                end = fptr.tell()
        else:
            raise RuntimeError('Binary Search Failed')

#Utilidade unica para testes
def main():
    ehSubs = lambda val: ast.literal_eval(val)[0]
    for i in range(1,10):
        print(binaryIdFind('data/base/id', 'tt000000'+str(i), ehSubs))
    for i in range(10,100):
        print(binaryIdFind('data/base/id', 'tt00000'+str(i), ehSubs))
    for i in range(100,167):
        print(binaryIdFind('data/base/id', 'tt0000'+str(i), ehSubs))
    for i in range(168,1000):
        print(binaryIdFind('data/base/id', 'tt0000'+str(i), ehSubs))
    #print(lineFind('id', 'tt0000020', ehSubs))

if __name__ == "__main__":
    main()
