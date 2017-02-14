class parseTree():
    def __init__(self, wordID, form, lemma, upostag, xpostag, feats,parentID,depRel):
        self.form = form
        self.lemma = lemma
        self.upostag = upostag
        self.xpostag = xpostag
        self.feats = feats
        self.parentID=parentID
        self.wordID = wordID
        self.depRel = depRel
        self.my_children = list()


        
    def add_child(self, obj):
        self.my_children.append(obj)


    def show_child(self):
        for i in self.children:
            print(i.form)
        return
    
    def get_children(self):
        return self.my_children

    def printNode(self, node):
        print(str(node.wordID)+'\t'+node.form+'\t'+ node.upostag+'\t'+str(node.parentID)+'\t'+node.depRel)
        return
  
    def printTree(self, node, level):
        print("\t"*level,end="")
        self.printNode(node)
        if len(node.my_children)>0:
            for child in node.my_children:
                node.printTree(child, level+1)
        return
