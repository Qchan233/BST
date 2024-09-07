from AVL import AVL_TREE, AVL_Node
import random

# use letter as key randomly insert and delete for a 1000 times
avl = AVL_TREE()

for i in range(10000):
    random_letter = chr(random.randint(97, 122))
    if i % 2 == 0:
        avl.insert(AVL_Node(random_letter))
    else:
        avl.remove(random_letter)
