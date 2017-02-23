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

list1_to_compare=[]
list2_to_compare=[]


def index_2d(myList, v):
    result=[]
    for i, x in enumerate(myList):
        if v in x:
            result.append(i)
            result.append(x.index(v))
            return result

def insert_cost(A):
    #print("inserting "+A.my_label)
    cost=3
    return cost
    
def remove_cost(A):
    #print("deleting "+A.my_label)
    cost=3
    return cost

def shallow_match_parent(A,B):
    if(len(list1_to_compare)>0 & len(list2_to_compare)>0):
        index_A= index_2d(list1_to_compare, A)
        index_B= index_2d(list2_to_compare, B)
        parent_index_A_i=index_A[0]
        parent_index_A_j=int(A.parentID)
        parent_index_B_i=index_B[0]
        parent_index_B_j=int(B.parentID)
        parent_A=list1_to_compare[parent_index_A_i][parent_index_A_j]
        parent_B=list2_to_compare[parent_index_B_i][parent_index_B_j]
        if(parent_A.form==parent_B.form):
            return True
        else:
            return False
    else:
           return False
   
def match_parent(A,B):
    if(len(list1_to_compare)>0 & len(list2_to_compare)>0):
        index_A= index_2d(list1_to_compare, A)
        index_B= index_2d(list2_to_compare, B)
        parent_index_A_i=index_A[0]
        parent_index_A_j=int(A.parentID)
        parent_index_B_i=index_B[0]
        parent_index_B_j=int(B.parentID)
        parent_A=list1_to_compare[parent_index_A_i][parent_index_A_j]
        parent_B=list2_to_compare[parent_index_B_i][parent_index_B_j]
        if((parent_A.form==parent_B.form) & shallow_match_parent(parent_A,parent_B)):
            return True
        else:
            return False
    else:
        return False

def update_cost(A,B):
    incost=0
    if(A.upostag!=B.upostag):
        incost+=1
    if(match_parent(A,B)):
        incost+=1
    if(A.form==B.form):
        cost=incost
    else:
        cost=remove_cost(A)+insert_cost(B)
    return cost


extract_holder=[]

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
    


sentence_holder=[]
files_to_open=["stanford_processed_input.txt","test.predict"]
c=0
pos_holder={}
holder_pos_holder=[]

for file in files_to_open:
    line_holders=[]
    with open(file,encoding="utf-8") as f:
        hold=f.read()
        if(file=="stanford_processed_input.txt"):

            trees=hold.split("\n***********************************************************\n")
        else:
            trees=hold.split("\n\n")

        #print("+++"+str(len(trees)))
        for tree in trees:
            line_holders.append(tree.split("\n"))
            #print(tree)

        for tree in line_holders:

            for sentence_to_remove in list(tree):
                if(sentence_to_remove==""):
                    #print("hello")
                    tree.remove(sentence_to_remove)

           #print(tree)
        



        for tree in line_holders:
            pos_holder.clear()
            biggest_id="0"
            prev_id="0"
            offset_id=""
            #print(tree)

            # for sentence_to_remove in list(tree):
            #     print(sentence_to_remove)
            #     if(sentence_to_remove==""):
            #         print("hello")
            #         tree.remove(sentence_to_remove)
            for sentence in tree:
                b=sentence.split("\t")
                rplc=""
                #print(sentence)
                if(file=="test.predict"):
                    sentence_holder.append(Tree(b[0],b[1],b[2],b[3],b[4],b[5],b[6],b[7]))

                else:
                    if(int(b[0])>int(biggest_id)):
                        #print(str(pos_holder.get(b[0],None)))
                        #print(b[0]+" "+b[1])
                        rplc=lookup(b[3])
                        biggest_id=b[0]
                        offset_id=b[0]
                        sentence_holder.append(Tree(b[0],b[1],b[2],rplc,rplc,b[5],b[6],b[7]))
                    else:
                        #print(str(int(biggest_id)+1)+ " "+b[1])
                        if(b[6]!="0"):

                            rplc=lookup(b[3])
                            sentence_holder.append(Tree(str(int(biggest_id)+1),b[1],b[2],rplc,rplc,b[5],str(int(b[6])+int(offset_id)),b[7]))   
                            biggest_id=str(int(biggest_id)+1)
                        else:
                            b[6]="-0"
                            sentence_holder.append(Tree(str(int(biggest_id)+1),b[1],b[2],rplc,rplc,b[5],b[6],b[7]))
                            biggest_id=str(int(biggest_id)+1) 
                              
       

            holder_pos_holder.append(deepcopy(pos_holder))

            #print(sentence_holder)
            extract_holder.append(deepcopy(sentence_holder))                           
            sentence_holder.clear()

    if(c==0):
        list1_to_compare=deepcopy(extract_holder)
        extract_holder.clear()
        #print(len(list1_to_compare))
        #print(len(extract_holder))
       # print("-")

    if(c==1):
        list2_to_compare=deepcopy(extract_holder)
        extract_holder.clear()
        #print(len(list2_to_compare))
      #  print(len(extract_holder))
    #print(c)


    i_j_holder=["99"]
    if c==0:
        x=list1_to_compare
    if c==1:
        x=list2_to_compare
    for trees in x:
        #print(trees)
        for id1,word in enumerate(trees):
            for id2, word2 in enumerate(trees):
                
                if(str(id1)+str(id2) not in i_j_holder):
                    if(word.wordID==word2.parentID):
                        word.add_child(word2)
                        i_j_holder.append(str(id2)+str(id1))
                    
                    if(word2.wordID==word.parentID):
                        word2.add_child(word)
                        i_j_holder.append(str(id2)+str(id1))

        i_j_holder.clear()



    c+=1
## end of iterations.
for tree in list1_to_compare:
    for node in tree:
            print(node.form +" "+ node.wordID)
    print("\n")
    
root1=None
root2=None
dummy_form="Dummy"
dummy_parent="999"
dummy_id=0
file_to_write=open('tree_outputs.txt', 'w',encoding="utf-8")



for i in range(len(list1_to_compare)):
    dummy1=Tree(dummy_id,dummy_form,b[2],b[3],b[4],b[5],dummy_parent,b[7])
    dummy2=Tree(dummy_id,dummy_form,b[2],b[3],b[4],b[5],dummy_parent,b[7])
    
    for j in range(len(list1_to_compare[i])):
        if(list1_to_compare[i][j].parentID=="0"):
            root1=list1_to_compare[i][j]
            dummy1.add_child(root1)
        if(list1_to_compare[i][j].parentID=="-0"):
            dummy1.add_child(list1_to_compare[i][j])       
           # (RenderTree(dummy1))
    for j in range(len(list2_to_compare[i])):
        if(list2_to_compare[i][j].parentID=="0"):
            root2=list2_to_compare[i][j]
            dummy2.add_child(root2)
    print("Stanford Tree:")
    print(RenderTree(dummy1))

    print(RenderTree(dummy2))
    file_to_write.write("Tree for normal parser.\n")
    file_to_write.write(str(RenderTree(dummy1))+"\n")
    file_to_write.write("Tree for tweet parser.\n")
    file_to_write.write(str(RenderTree(dummy2))+"\n")

    if(root1 and root2):
        dist = zss.distance(dummy1, dummy2, Tree.get_children, insert_cost, remove_cost, update_cost)
        print(" Distance is "+str(dist))
        file_to_write.write("Distance is "+str(dist)+"\n")
        file_to_write.write("*****************************************************"+"\n")
        
    root1=None
    root2=None

file_to_write.close()