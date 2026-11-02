from ohma.core import Tree,Node
def test_tree(tmp_path):
 t=Tree(tmp_path/"x"); t.add(Node("a",None,"root","active")); assert t.all()
