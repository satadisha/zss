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
reg=re.compile("[^a-zA-Z0-9]")

def index_2d(myList, v):
    result=[]
    for i, x in enumerate(myList):
        if v in x:
            result.append(i)
            result.append(x.index(v))
            return result

def insert_cost(A):
    #print("inserting "+A.my_label)
    #cost=3
    if(len(A.get_children())==0):
        cost=1
    else:
        cost=len(A.get_children())+1
    #print("inserting "+A.form+" "+str(cost))
    return cost
    
def remove_cost(A):
    #print("deleting "+A.form)
    #cost=3
    if(len(A.get_children())==0):
        cost=1
    else:
        cost=len(A.get_children())+1
    #print("deleting "+A.form+" "+str(cost))
    return cost

def postorder(Tree):
    if Tree != None:
        for child in Tree.children:
            postorder(child)
        print(Tree.form)

def height(Tree):

    if Tree.children is None:
        return 0
    else:
        return max([height(child) for child in Tree.children ]) + 1
                

def find_element(lst,id):
    for element in lst:
        if(id==element.wordID):
            return element

def shallow_match_parent(A,B):
    if((len(list1_to_compare)>0) & (len(list2_to_compare)>0)):
        index_A= index_2d(list1_to_compare, A)
        index_B= index_2d(list2_to_compare, B)
        parent_index_A_i=index_A[0]
        if((A.parentID!="0")&(A.parentID!="-0")&(A.parentID!="999")):
            parent_A=find_element(list1_to_compare[parent_index_A_i],A.parentID)
        else:
            parent_A=None
        parent_index_B_i=index_B[0]
        if((B.parentID!="0")&(B.parentID!="-0")&(B.parentID!="999")):
            parent_B=find_element(list2_to_compare[parent_index_B_i],B.parentID)
        else:
            parent_B=None
        if((parent_A==None)&(parent_B==None)):
            return True
        elif ((parent_A==None)&(parent_B!=None)):
            return False
        elif ((parent_A!=None)&(parent_B==None)):
            return False
        else:
            if((reg.sub("",parent_A.form))==(reg.sub("",parent_B.form))):
                #print(True)
                return True
            else:
                return False
    else:
           return False

def match_parent(A,B):
    #print(len(list1_to_compare))
    if((len(list1_to_compare)>0) & (len(list2_to_compare)>0)):
        #print("here")
        index_A= index_2d(list1_to_compare, A)
        index_B= index_2d(list2_to_compare, B)
        parent_index_A_i=index_A[0]
        if((A.parentID!="0")&(A.parentID!="-0")&(A.parentID!="999")):
            parent_A=find_element(list1_to_compare[parent_index_A_i],A.parentID)
        else:
            parent_A=None
        #print(B.parentID)
        parent_index_B_i=index_B[0]
        if((B.parentID!="0")&(B.parentID!="-0")&(B.parentID!="999")):
            parent_B=find_element(list2_to_compare[parent_index_B_i],B.parentID)
        else:
            parent_B=None
        #print("**"+B.parentID)
        #print("=>=> "+parent_A.form+" "+parent_B.form)
        if((parent_A==None)&(parent_B==None)):
            return True
        elif ((parent_A==None)&(parent_B!=None)):
            return False
        elif ((parent_A!=None)&(parent_B==None)):
            return False
        else:
            if((reg.sub("",parent_A.form))==(reg.sub("",parent_B.form))):
            #if(((reg.sub("",parent_A.form))==(reg.sub("",parent_B.form))) & shallow_match_parent(parent_A,parent_B)):
                #print(True)
                return True
            else:
                return False
    else:
        return False

def update_cost(A,B):
    cost=0
    incost=0
    temp=True
    #print(reg.sub("",A.form))
    #print(reg.sub("",B.form))
    '''if(A.upostag!=B.upostag):
        incost+=1
    #print(reg.sub("",A.form))'''
    if((reg.sub("",A.form))==(reg.sub("",B.form))):
        if(A.form!="Dummy"):
            if (match_parent(A,B)):
                #print("matching "+A.form+" and "+B.form)
                temp=False
                cost=0
                return cost
            else:
                temp=True
        else:
            temp=False
            cost=0
            return cost
    if(temp):
        #print("inserting "+A.form+" and deleting "+B.form)
        cost=remove_cost(A)+insert_cost(B)
        if((reg.sub("",A.form))!=(reg.sub("",B.form))):
            cost+=50
        #print (str(cost))
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
files_to_open=["regular_processed_input.txt","tweet_sample.predict"]
c=0
pos_holder={}
holder_pos_holder=[]

for file in files_to_open:
    line_holders=[]
    with open(file,encoding="utf-8") as f:
        hold=f.read()
        if(file=="regular_processed_input.txt"):

            trees=list(filter(None,hold.split("\n*****************************************************\n")))
        else:
            trees=list(filter(None,hold.split("\n\n")))

        #print("+++"+str(len(trees)))
        for tree in trees:
            line_holders.append(list(filter(None,tree.split("\n"))))
            #print(tree)

        for tree in line_holders:
            for sentence_to_remove in list(tree):
                if(sentence_to_remove==""):
                    #print("hello")
                    tree.remove(sentence_to_remove)

        



        for tree in line_holders:
            pos_holder.clear()
            biggest_id=0
            prev_id=0
            offset_id=0
            #print(tree)
            for sentence in tree:
                b=sentence.split("\t")
                if(file=="tweet_sample.predict"):
                    sentence_holder.append(Tree(b[0],b[1],b[2],b[3],b[4],b[5],b[6],b[7]))

                else:
                    '''if(int(b[0])>int(biggest_id)):
                        print("++++"+b[1])
                        #print(b[0]+" "+b[1])
                        #rplc=lookup(b[3])
                        biggest_id=b[0]
                        offset_id=b[0]
                        sentence_holder.append(Tree(b[0],b[1],b[2],b[3],b[4],b[5],b[6],b[7]))
                        
                    else:
                        #print(str(int(biggest_id)+1)+ " "+b[1])
                        if(b[6]!="0"):
                            print("-----")
                            sentence_holder.append(Tree(str(int(biggest_id)+int(b[0])),b[1],b[2],b[3],b[4],b[5],str(int(b[6])+int(offset_id)),b[7]))   
                            biggest_id=str(int(biggest_id)+1)
                        else:
                            print("====")
                            b[6]="-0"
                            sentence_holder.append(Tree(str(int(biggest_id)+1),b[1],b[2],b[3],b[4],b[5],b[6],b[7]))
                            biggest_id=str(int(biggest_id)+1) '''
                    temp=int(b[0])
                    if(int(b[0])>prev_id):
                        if(int(b[0])>biggest_id):
                            biggest_id=int(b[0])
                            sentence_holder.append(Tree(b[0],b[1],b[2],b[3],b[4],b[5],b[6],b[7]))
                            prev_id=temp
                        else:
                            b[0]=str(offset_id+int(b[0]))
                            if(b[6]!="0"):
                                b[6]=str(offset_id+int(b[6]))
                            else:
                                b[6]="-0"
                            biggest_id=int(b[0])
                            sentence_holder.append(Tree(b[0],b[1],b[2],b[3],b[4],b[5],b[6],b[7]))
                            prev_id=temp
                    else:
                        offset_id+=biggest_id
                        b[0]=str(offset_id+int(b[0]))
                        if(b[6]!="0"):
                            b[6]=str(offset_id+int(b[6]))
                        else:
                            b[6]="-0"
                        biggest_id=int(b[0])
                        sentence_holder.append(Tree(b[0],b[1],b[2],b[3],b[4],b[5],b[6],b[7]))
                        prev_id=temp
                        
                              
       

            holder_pos_holder.append(deepcopy(pos_holder))

            #print(sentence_holder)
            extract_holder.append(deepcopy(sentence_holder))                           
            sentence_holder.clear()

    if(c==0):
        list1_to_compare=deepcopy(extract_holder)
        extract_holder.clear()


    if(c==1):
        list2_to_compare=deepcopy(extract_holder)
        extract_holder.clear()


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

    
root1=None
root2=None
dummy_form="Dummy"
dummy_parent="999"
dummy_id=0
file_to_write=open('tree_outputs.txt', 'w',encoding="utf-8")

print(len(list1_to_compare))
print(len(list2_to_compare))
for i in range(90,91):
#for i in range(len(list1_to_compare)):
    dummy1=Tree(dummy_id,dummy_form,b[2],b[3],b[4],b[5],dummy_parent,b[7])
    dummy2=Tree(dummy_id,dummy_form,b[2],b[3],b[4],b[5],dummy_parent,b[7])
    
    for j in range(len(list1_to_compare[i])):
        if(list1_to_compare[i][j].parentID=="0"):
            root1=list1_to_compare[i][j]
            dummy1.add_child(root1)
        if(list1_to_compare[i][j].parentID=="-0"):
            dummy1.add_child(list1_to_compare[i][j]) 
            
    for j in range(len(list2_to_compare[i])):
        if(list2_to_compare[i][j].parentID=="0"):
            root2=list2_to_compare[i][j]
            dummy2.add_child(root2)
    '''print(str(i)+". Regular Parser Tree:")
    print(RenderTree(dummy1))
    print("Tweet Parser Tree:")
    print(RenderTree(dummy2))'''
    file_to_write.write(str(i)+". Tree for normal parser.\n")
    file_to_write.write(str(RenderTree(dummy1))+"\n")
    file_to_write.write("Tree for tweet parser.\n")
    file_to_write.write(str(RenderTree(dummy2))+"\n")

    if(root1 and root2):
        dist = zss.distance(dummy1, dummy2, Tree.get_children, insert_cost, remove_cost, update_cost)
        #print(str(i+1)+". Distance is "+str(dist))
        print(str(dist))
        file_to_write.write("Distance is "+str(dist)+"\n")
        file_to_write.write("*****************************************************"+"\n")
        
    root1=None
    root2=None

file_to_write.close()