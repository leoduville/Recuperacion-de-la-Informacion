import sys
from os import listdir
from os.path import join, isdir

def main():
    filein = "../CISI/CISI.REL"
    fileout= open("qrels_CISI", "x",encoding='utf-8')
    with open(filein,'r',encoding='utf-8') as f:  
        for line in f.readlines():
            query_id, document_id, _, _ = line.split()
            fileout.write("{} {} {} {}\n".format(query_id, 0, document_id, 1))
    fileout.close()

if __name__ == '__main__':
    main()
    