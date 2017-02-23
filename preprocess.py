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

def setPosTag(postag):
    if(postag=="^+G"):
        return "Z"
    if(postag=="N+G"):
        return "S"
    if(postag=="^+V"):
        return "M"
    if(postag=="N+V"):
        return "L"
    if(postag=="O+V"):
        return "L"
    if(postag=="V+R"):
        return "V"
    if(postag=="V+V"):
        return "V"
    if(postag=="X+R"):
        return "Y"

def lookup(postag):
    rplc=""
    if(postag=="NN" or postag=="NNS"):
        rplc="N"
    if(postag=="PRP" or postag=="WP"):
        rplc="O"
    if(postag=="NNP" or postag=="NNPS"):
        rplc="^"
    if(postag[0]=="V" or postag=="MD"):
        rplc="V"
    if(postag[0]=="J"):
        rplc="A"
    if(postag[0]=="R" or postag=="WRB"):
        rplc="R"
    if(postag=="UH" or postag=="UH"):
        rplc="!"
    answer=re.match(r'WP$',postag)
    answer2=re.match(r'PRP$',postag)
    if(answer!=None or answer2!=None or postag=="DT" or postag=="WDT" or postag=="PRP$"):
        rplc="D"
    if(postag=="IN" or postag=="TO"):
        rplc="P"
    if(postag=="CC" or postag=="CC"):
        rplc="&"
    if(postag=="RP"):
        rplc="T"
    if(postag=="EX" or postag=="PDT"):
        rplc="X"
    if(postag=="CD"):
        rplc="$"
    if(postag=="FW" or postag=="POS" or postag=="SYM" or postag=="LS"):
        rplc="G"
    if(postag in string.punctuation or postag=="''" or postag=="``" or postag=="-LRB-" or postag=="-RRB-"):
        rplc=","
    if(postag=="HT"):
        rplc="#"
    if(rplc==""):
        rplc=postag
    return rplc

def set_parentID(mergee,merger):
    wordIDlist=[mergee[0],merger[0]]
    parentID=-999
    #print(str(mergee[0])+" "+str(merger[0]))
    #print(str(mergee[6])+" "+str(merger[6]))
    if (mergee[6]==merger[6]):
        parentID= merger[6]
    else:
        if (mergee[6] not in wordIDlist):
            parentID= mergee[6]
        elif (merger[6] not in wordIDlist):
            parentID= merger[6]
    #print("The parentID is "+str(parentID))
    return parentID
            
line_holders=[]
tree_holders=[]
pos_holder={}
holder_pos_holder=[]
with open("regular_parser.txt",encoding="utf-8") as f1:
    hold=f1.read()
    trees=hold.split("\n++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n")
    for tree in trees:
        #print(len(tree.split("\n\n")))
        tree_holders.append(tree.split("\n\n"))
print  (len(tree_holders))      

i=0
tweet_tree_holder=[]   
for trees in tree_holders:
    tree_b_holder=[]    #tweet level container
    for tree in trees:
        b_holder=[]    #tree level container
        i=0
        sentences=tree.split("\n")
        for sentence in sentences:
            b=sentence.split("\t")
            print(b)
            b[3]= lookup(b[3])
            b[4]=b[3]
            b_holder.append(b) 
            if(("'" in b[1])& (b[3]!="NNP")):
                    new_form=b_holder[i-1][1]+b[1]
                    new_upostag=b_holder[i-1][3]+'+'+b[3]
                    b_holder[i-1][1]=new_form
                    b_holder[i-1][3]=setPosTag(new_upostag)
                    #merge_position.append(i)
                    #b[6]=str(int(b[6])-merge_count)
                    b_holder[i-1][6]=set_parentID(b_holder[i-1],b)
                    del(b_holder[i])
                    i=i-1
            i=i+1
        #print("===>"+str(merge_position))
        tree_b_holder.append(b_holder)
    tweet_tree_holder.append(tree_b_holder)

file_to_write=open("stanford_processed_input2.txt","w",encoding="utf-8")



for tree_b_holder in tweet_tree_holder:
    file_to_write.write("\n***********************************************************\n")
    for b_holder in tree_b_holder:
        #print(b_holder)
        for line in b_holder:
            str1 = '\t'.join(line)
            file_to_write.write(str1)
            file_to_write.write("\n")
        

file_to_write.close()