from BST import BST, Node, DIRECTION

class SPLAY_TREE(BST):
    def splay(self, v):
        self.check_tree()
        if v is None:
            return None
            
        def get_pg(v):
            p = v.parent
            if p is None:
                return None, None
            g = p.parent
            return p, g

        p, g = get_pg(v)
        while p and g:
            gg = g.parent
            if v.is_left_child():
                if p.is_left_child():
                    self.set_parent(g, p.right, DIRECTION.LEFT)
                    self.set_parent(p, v.right, DIRECTION.LEFT)
                    self.set_parent(p, g, DIRECTION.RIGHT)
                    self.set_parent(v, p, DIRECTION.RIGHT)
                else:
                    self.set_parent(p, v.right, DIRECTION.LEFT)
                    self.set_parent(g, v.left, DIRECTION.RIGHT)
                    self.set_parent(v, g, DIRECTION.LEFT)
                    self.set_parent(v, p, DIRECTION.RIGHT)
            else:
                if p.is_right_child():
                    self.set_parent(g, p.left, DIRECTION.RIGHT)
                    self.set_parent(p, v.left, DIRECTION.RIGHT)
                    self.set_parent(p, g, DIRECTION.LEFT)
                    self.set_parent(v, p, DIRECTION.LEFT)
                else:
                    self.set_parent(p, v.left, DIRECTION.RIGHT)
                    self.set_parent(g, v.right, DIRECTION.LEFT)
                    self.set_parent(v, g, DIRECTION.RIGHT)
                    self.set_parent(v, p, DIRECTION.LEFT)
            self.set_parent(gg, v)
            p, g = get_pg(v)
        
        if p:
            if v.is_left_child():
                self.set_parent(p, v.right, DIRECTION.LEFT)
                self.set_parent(v, p, DIRECTION.RIGHT)
            else:
                self.set_parent(p, v.left, DIRECTION.RIGHT)
                self.set_parent(v, p, DIRECTION.LEFT)

        self.set_parent(None, v) 
        self.check_tree()
        return v
    
    def search(self, key):
        node = super().search(key)
        self._root = self.splay(node if node else self._hot)
        return self._root

    def insert(self, new_node: Node):
        if self._root is None:
            self._root = new_node
            return self._root

        if (new_node.key == self.search(new_node.key).key):
            assert self._root.key == new_node.key
            return self._root
        
        if self._root.key < new_node.key:
            self.set_parent(new_node, self._root, DIRECTION.LEFT)
            self.set_parent(new_node, self._root.right, DIRECTION.RIGHT)
            # If the child already exists in the tree, we need to remove its reference
            self._root.right = None
        else:
            self.set_parent(new_node, self._root, DIRECTION.RIGHT)
            self.set_parent(new_node, self._root.left, DIRECTION.LEFT)
            # If the child already exists in the tree, we need to remove its reference
            self._root.left = None

        self.set_parent(None, new_node)
        self.check_tree()
        return self._root
    
    def remove(self, key):
        if self._root is None or key != self.search(key).key:
            return False
        
        if self._root.left is None:
            self.set_parent(None, self._root.left)
        elif self._root.right is None:
            self.set_parent(None, self._root.left)
        else:
            left = self._root.left
            self.set_parent(None, self._root.right)
            self.search(key)
            assert self._root.left is None

            self.set_parent(self._root, left)
            
        self.check_tree()
        return True