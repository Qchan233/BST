from enum import Enum
from typing import Optional


class DIRECTION(Enum):
    LEFT = 0
    RIGHT = 1


class Node:
    def __init__(self, key, left = None, right = None, parent = None) -> None:
        self.key = key
        self.left = left
        self.right = right
        self.parent = parent
    
    @property
    def successor(self):
        if self.right:
            node = self.right
            while node.left:
                node = node.left
            return node
        else:
            return None


class BST:
    def __init__(self, node: Node = None) -> None:
        self._root = node
        self._hot = None
    
    def trav_pre(self, fn):
        stack = []
        if self._root:
            stack.append(self._root)

        while stack:
            x = stack.pop() 
            fn(x)
            if x.right:
                stack.append(x.right)
            if x.left:
                stack.append(x.left)

    def trav_mid(self, fn):
        stack = []
        x = self._root
        def go_left(x):
            while x:
                stack.append(x)
                x = x.left
        while True:
            go_left(x)
            if not stack:
                break
            x = stack.pop()
            fn(x)
            x = x.right

    def trav_post(self, fn):
        pass

    def search(self, key):
        def search_at(node, key):
            if node is None or node.key == key:
                return node
            self._hot = node

            return search_at(node.left if key < node.key else node.right, key)

        self._hot = None 
        return search_at(self._root, key)

    def set_parent(self, parent: Node, child: Node, direction: Optional[DIRECTION] = None):
        if child: 
            child.parent = parent
        if parent is None:
            self._root = child
            return

        if direction is None:
            direction = DIRECTION.LEFT if child.key < parent.key else DIRECTION.RIGHT

        if direction == DIRECTION.LEFT:
            parent.left = child
        else:
            parent.right = child

    def insert(self, new_node: Node):
        self.check_tree()
        node = self.search(new_node.key)
        if node:
            return node
        self.set_parent(self._hot, new_node)
        self.check_tree()
        return new_node
    
    def remove(self, key):
        def remove_at(node: Node):
            self.check_tree()
            succ = None 

            direction = None if node.parent is None else DIRECTION.LEFT \
                if node.parent.left == node else DIRECTION.RIGHT
            
            if node.left is None:
                self.set_parent(node.parent, node.right, direction)
            elif node.right is None:
                self.set_parent(node.parent, node.left, direction)
            else:
                succ = node.successor
                node.key, succ.key = succ.key, node.key
                remove_at(succ)
            self.check_tree()

        node = self.search(key)
        if not node:
            return
        remove_at(node)

    def check_at(self, node):
        if node is None:
            return
        key = node.key

        if node.left:
            assert node.left.key < key
            assert node.left.parent == node
        if node.right:
            assert node.right.key > key
            assert node.right.parent == node
        if node.parent:
            assert node.parent.left == node or node.parent.right == node

    def check_tree(self): 
        self.trav_pre(self.check_at)