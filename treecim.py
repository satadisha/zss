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

def insert_cost(A):
    #print("inserting "+A.my_label)
    cost=3
    return cost
    
def remove_cost(A):
    #print("deleting "+A.my_label)
    cost=3
    return cost

def update_cost(A,B):
    incost=0
    if(A.upostag!=B.upostag):
        incost+=1
    if(A.depRel!=B.depRel):
        incost+=1
    if(A.lemma==B.lemma):
        cost=incost
    else:
        cost=remove_cost(A)+insert_cost(B)
    return cost

class Extractor():
    
    def __init__(self, id2, form, lemma, upostag, xpostag, feats,head,deprel,deps,misc):
        self.id = id2
        self.form = form
        self.lemma = lemma
        self.upostag = upostag
        self.xpostag = xpostag
        self.feats = feats
        self.head=head
        self.deprel=deprel
        self.deps=deps
        self.misc=misc
    
    def get_children():
        return node.my_children
    
    def get_nodeID():
        return node.nodeID
    
    def get_depRel():
        return node.depRel
    
    def get_parentID():
        return node.parentID
    
    def get_posTag():
        return node.posTag
    
    def get_lemma():
        return node.my_lemma
extract_holder=[]

c=0

def lookup(postag):
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
    
##with open("test.predict",encoding="utf-8") as f:
##    for line in f:
##        c=c+1
##        a=line.replace("\n","")
##        b=a.split("\t")
##        #print (a.split("\t"))
##        form=bytes(str(b[1]).encode("utf-8"))
##        form=form.decode("utf-8")
##        print(form)
##        extract_holder.append(Tree(b[0], 
##form,
##b[2],
##b[3],
##b[4],
##b[5],
##b[6],
##b[7],
##b[8],
##b[9]))

line_holders=[]
sentence_holder=[]
files_to_open=["output3.txt","test.predict"]
c=0
for file in files_to_open:
    with open(file,encoding="utf-8") as f:
        hold=f.read()
        trees=hold.split("\n\n")
        #print("+++"+str(len(trees)))
        for tree in trees:
            line_holders.append(tree.split("\n"))


        for tree in line_holders:
            
            for sentence in tree:
                b=sentence.split("\t")
                rplc=""
                if(file=="test.predict"):
                    sentence_holder.append(Tree(b[0],b[1],b[2],b[3],b[4],b[5],b[6],b[7]))
                else:
                    rplc=lookup(b[3])
                    sentence_holder.append(Tree(b[0],b[1],b[2],rplc,rplc,b[5],b[6],b[7]))

            #print(sentence_holder)
            extract_holder.append(deepcopy(sentence_holder))                           
            sentence_holder.clear()
            line_holders.clear()

    if(c==0):
        list1_to_compare=deepcopy(extract_holder)
        extract_holder.clear()
       # print(len(list1_to_compare))
      #  print(len(extract_holder))
       # print("-")

    if(c==1):
        list2_to_compare=deepcopy(extract_holder)
        extract_holder.clear()
      ##  print(len(list2_to_compare))
      #  print(len(extract_holder))
    c=c+1
    #print(c)
    extract_holder.clear()


i_j_holder=["99"]
c=0
while c<2:
    if c==0:
        x=list1_to_compare
    if c==1:
        x=list2_to_compare
    for trees in x:
        #print(trees)
        for id1,word in enumerate(trees):
            for id2, word2 in enumerate(trees):
                #print(word2)
                            
                #print(word2.id)
                if(str(id1)+str(id2) not in i_j_holder):
                    if(word.wordID==word2.parentID):
                        word.add_child(word2)
                        i_j_holder.append(str(id2)+str(id1))
                    
                    if(word2.wordID==word.parentID):
                        word2.add_child(word)
                        i_j_holder.append(str(id2)+str(id1))

        i_j_holder.clear()


    for trees in x:
        for word in trees:
            if(word.parentID=="0"):
                #print("mert")
                root=word

    c+=1
root1=None
root2=None
for i in range(len(list1_to_compare)):
    for j in range(len(list1_to_compare[i])):
        if(list1_to_compare[i][j].parentID=="0"):
            root1=list1_to_compare[i][j]
    for j in range(len(list2_to_compare[i])):
        if(list2_to_compare[i][j].parentID=="0"):
            root2=list2_to_compare[i][j]
    if(root1 and root2):
        dist = zss.distance(root1, root2, Tree.get_children, insert_cost, remove_cost, update_cost)
        print("Distance is"+str(dist))
        
    root1=None
    root2=None
##
##for trees in extract_holder:
##    for word in trees:
##        if(len(word.upostag)>1):
##            #print(word.upostag)

    #print(RenderTree(root))
    #print("\n*************")
#root.show_child()
