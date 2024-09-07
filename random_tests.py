from AVL import AVL_TREE, AVL_Node
from SPLAY_TREE import SPLAY_TREE
import random

# use letter as key randomly insert and delete for a 1000 times
avl = AVL_TREE()

for i in range(10000):
    random_int = random.randint(1, 60)
    if i % 2 == 0:
        avl.insert(AVL_Node(random_int))
    else:
        avl.remove(random_int)

# use letter as key randomly insert and delete for a 1000 times
splay = SPLAY_TREE()

for i in range(10000):
    random_int = random.randint(1, 60)
    if i % 2 == 0:
        splay.insert(AVL_Node(random_int))
    else:
        splay.remove(random_int)