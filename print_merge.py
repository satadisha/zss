from tree2 import Tree
from anytree import Node, RenderTree
import sys
if sys.version[0] == '2':
    reload(sys)
    sys.setdefaultencoding("utf-8")
import site
from copy import deepcopy
import re
import string
import zss

line_holders=[]
tree_holders=[]
pos_holder={}
holder_pos_holder=[]
with open("regular_parser.txt",encoding="utf-8") as f:
    hold=f.read()
    trees=hold.split("\n++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n")
    for tree in trees:
        print(len(tree.split("\n\n")))
        tree_holders.append(tree.split("\n\n"))
        

    i=0
    
    for trees in tree_holders:
        for tree in trees:
            b_holder=[]
            i=0
            sentences=tree.split("\n")
            for sentence in sentences:
                b=sentence.split("\t")
                b_holder.append(b)
                #print(sentence)
                try:            
                    if("'" in b[1] ):
                        if(b[3]!="NNP"):
                            new_form=b_holder[i-1][1]+b[1]
                            b_holder[i-1][1]=new_form
                            del b_holder[i] 			
                except Exception as e:
                    pass

                i=i+1

            for line in b_holder:
                print(line)

        

        
                
