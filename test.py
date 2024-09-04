from BST import BST
from BST import Node

# Tests for BST
bst = BST()
bst.check_tree()

# Testing Insert
bst.insert(Node('i'))
bst.insert(Node('d'))
bst.insert(Node('l'))
bst.insert(Node('c'))
bst.insert(Node('h'))
bst.insert(Node('k'))
bst.insert(Node('n'))
bst.insert(Node('a'))
bst.insert(Node('f'))
bst.insert(Node('j'))
bst.insert(Node('m'))
bst.insert(Node('p'))
bst.insert(Node('b'))
bst.insert(Node('e'))
bst.insert(Node('g'))
bst.insert(Node('o'))

accumulator = ''
def accumulate(x):
    global accumulator
    accumulator += str(x.key)
bst.trav_pre(accumulate)
assert accumulator == 'idcabhfeglkjnmpo'

accumulator = ''
def accumulate(x):
    global accumulator
    accumulator += str(x.key)
bst.trav_mid(accumulate)
assert accumulator == 'abcdefghijklmnop'

for c in accumulator:
    bst.remove(c)

accumulator = ''
def accumulate(x):
    global accumulator
    accumulator += str(x.key)
bst.trav_mid(accumulate)
assert accumulator == ''