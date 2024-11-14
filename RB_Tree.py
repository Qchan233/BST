from BST import BST, Node
from enum import Enum

class Color(Enum):
    BLACK = 0
    RED = 1

def height(node):
    return node.height if node else -1

def is_black(node):
    return not node or node.color == Color.BLACK

def is_red(node):
    return not is_black(node)

def update_height(node):
    node.height = max(height(node.left), height(node.right))
    if is_black(node):
        node.height += 1

    return node.height

def height_updated(node):
    return height(node.left) == height(node.right) and (node.height == (height(node.left) if is_red(node) else height(node.left) + 1))

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

class RB_Node(Node):
    def __init__(self, key, left = None, right = None, parent = None, color = Color.RED, height = -1) -> None:
        super().__init__(key, left, right, parent)
        self.color = color
        self.height = height

    def __repr__(self) -> str:
        color_str = '🔴' if self.color == Color.RED else '⚫'
        return color_str + str(self.key)

    def __str__(self) -> str:
        return 'R' if self.color == Color.RED else 'B'

class RB_Tree(BST):
    def check_at(self, node):
        super().check_at(node)
        assert isinstance(node, RB_Node)
        if is_red(node):
            assert is_black(node.left)
            assert is_black(node.right)
        assert height_updated(node)

    def solve_double_red(self, x: RB_Node):
        if x is self._root:
            self._root.color = Color.BLACK
            self._root.height += 1
            return
        p = x.parent
        if p.color == Color.BLACK:
            return
        g = p.parent
        u = g.left if g.left != p else g.right

        if is_black(u):
            if x.is_left_child() == p.is_left_child():
                p.color = Color.BLACK
            else:
                x.color = Color.BLACK
            g.color = Color.RED
            self.rotate_at(x)
        else:
            p.color = Color.BLACK
            p.height += 1
            u.color = Color.BLACK
            u.height += 1
            g.color = Color.RED
            self.solve_double_red(g)

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

    def insert(self, e):
        x = self.search(e)
        if x:
            return x
        x = RB_Node(e)
        self.set_parent(self._hot, x)
        self.solve_double_red(x)
        assert x
        self.check_tree()
        return x

    def solve_double_black(self, r: RB_Node):
        p = r.parent if r else self._hot # In case r is None, and considers recursion
        if p is None:
            return
        s = p.right if r == p.left else p.left
        if is_black(s):
            t = None
            if is_red(s.right):
                t = s.right
            if is_red(s.left):
                t = s.left
            if t: # BB-1
                old_color = p.color
                b = self.rotate_at(t)
                if b.left:
                    b.left.color = Color.BLACK
                    update_height(b.left)
                if b.right:
                    b.right.color = Color.BLACK
                    update_height(b.right)

                b.color = old_color
                update_height(b)
            else: # BB-2
                s.color = Color.RED
                s.height -= 1
                if is_red(p): #
                    p.color = Color.BLACK
                else:
                    p.height -= 1
                    self.solve_double_black(p)
        else: # BB-3
            s.color = Color.BLACK
            p.color = Color.RED
            # s is red, because on the othersider x is not None, s must have non-empty child
            t = s.left if s.is_left_child() else s.right
            # self._hot = p
            self.rotate_at(t)
            self.solve_double_black(r)


    def remove(self, e):
        x = self.search(e)
        if x is None:
            return False
        r = self.remove_at(x)
        if self._root is None:
            return

        if self._hot is None:
            self._root.color = Color.BLACK
            update_height(self._root)
            return True

        if  height_updated(self._hot):
            return True

        if is_red(r):
            r.color = Color.BLACK
            r.height += 1
            return True

        self.solve_double_black(r)
        self.check_tree()
        return True


if __name__ == '__main__':
    import random
    rbt = RB_Tree()
    for i in range(20):
        random_int = random.randint(1, 200)
        if i % 2 == 0:
            rbt.insert(random_int)
        else:
            rbt.remove(random_int)
    
    rbt.visualize()