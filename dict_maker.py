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
pos_holder={}
holder_pos_holder=[]
with open("test.predict",encoding="utf-8") as f:
    hold=f.read()
    trees=hold.split("\n\n")
    for tree in trees:
        line_holders.append(tree.split("\n"))
        


    for tree in line_holders:
        pos_holder.clear()            
        for sentence in tree:
            b=sentence.split("\t")
            rplc=""
            if(b[6]!="-1"):
                key=b[1]
                pos_holder.setdefault(key, [])
                pos_holder[key].append(b[0])

        holder_pos_holder.append(deepcopy(pos_holder))


    for tree in holder_pos_holder:
        for key, value in tree.items():
            print(key,value)

        

        
                
