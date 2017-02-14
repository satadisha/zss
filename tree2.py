class Tree():
    def __init__(self, wordID, form, lemma, upostag, xpostag, feats,parentID,depRel):
        self.form = form
        self.lemma = lemma
        self.upostag = upostag
        self.xpostag = xpostag
        self.feats = feats
        self.parentID=parentID
        self.wordID = wordID
        self.depRel = depRel
        self.children = list()


        
    def add_child(self, obj):
        self.children.append(obj)


    def show_child(self):
        for i in self.children:
            print(i.form)
        return
    
    def get_children(self):
        return self.children

    def printNode(self, node):
        print(str(node.wordID)+'\t'+node.lemma+'\t'+ node.upostag+'\t'+str(node.parentID)+'\t'+node.depRel)
        return
  
    def printTree(self, node, level):
        print("\t"*level,end="")
        self.printNode(node)
        if len(node.children)>0:
            for child in node.childen:
                node.printTree(child, level+1)
        return
