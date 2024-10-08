from BST import BST, Node, DIRECTION

def height(node):
    return node.height if node else -1

def update_height(node):
    node.height = max(height(node.left), height(node.right)) + 1
    return node.height

def update_height_above(node):
    while node:
        update_height(node)
        node = node.parent

def taller_child(node):
    if height(node.left) > height(node.right):
        return node.left
    elif height(node.left) < height(node.right):
        return node.right
    else:
        return node.left if node.is_left_child() else node.right

def connect34(
    a, b,c,
    T0, T1, T2, T3
):
    a.left = T0
    a.right = T1
    if T0:
        T0.parent = a
    if T1:
        T1.parent = a
    update_height(a)

    c.left = T2
    c.right = T3
    if T2:
        T2.parent = c
    if T3:
        T3.parent = c
    update_height(c)

    b.left = a
    b.right = c
    a.parent = b
    c.parent = b
    update_height(b)
    return b

def avl_balance(node):
    height_diff = height(node.left) - height(node.right)
    return height_diff in {-1, 0, 1}

class AVL_Node(Node):
    def __init__(self, key, left = None, right = None, parent = None) -> None:
        super().__init__(key, left, right, parent)
        self.height = 0

class AVL_TREE(BST):

    def check_at(self, node):
        super().check_at(node)
        assert isinstance(node, AVL_Node)
        assert height(node.left) - height(node.right) in {-1, 0, 1}
        assert avl_balance(node)

    def rotate_at(self, v: Node):
        p = v.parent
        g = p.parent
        if p.is_left_child():
            if v.is_left_child():
                self.set_parent(g.parent, p, None)
                return connect34(v, p, g, v.left, v.right, p.right, g.right)
            else:
                self.set_parent(g.parent, v, None)
                return connect34(p, v, g, p.left, v.left, v.right, g.right)
        else:
            if v.is_left_child():
                self.set_parent(g.parent, v, None)
                return connect34(g, v, p, g.left, v.left, v.right, p.right)
            else:
                self.set_parent(g.parent, p, None)
                return connect34(g, p, v, g.left, p.left, v.left, v.right)

    def insert(self, new_node: AVL_Node):
        super().insert(new_node)
        g = self._hot
        while g is not None:
            if not avl_balance(g):
                self.rotate_at(taller_child(taller_child(g)))
                break
            else:
                update_height(g)
            g = g.parent

        self.check_tree()
        return new_node

    def remove(self, key):
        result = super().remove(key)
        if not result:
            return False
        g = self._hot
        while g is not None:
            if not avl_balance(g):
                g = self.rotate_at(taller_child(taller_child(g)))
            update_height(g)
            g = g.parent

        self.check_tree()
        return True

if __name__ == '__main__':
    avl = AVL_TREE()
    avl.insert(AVL_Node('g'))
    avl.insert(AVL_Node('e'))
    avl.insert(AVL_Node('r'))
    avl.insert(AVL_Node('b'))
    avl.insert(AVL_Node('n'))
    avl.insert(AVL_Node('y'))
    avl.insert(AVL_Node('k'))

    avl.remove('y')
    avl.remove('g')
    print('Passed')