import bisect

class B_Node:
    def __init__(self, key = None):
        if key is not None:
            self.keys = [key]
            self.parent = None
            self.children = [None, None]
        else:
            self.keys = []
            self.parent = None
            self.children = [None]

    def __repr__(self):
        return "".join(str(self.keys))

class B_Tree:
    def __init__(self, m = 3):
        self._root = B_Node()
        self.max_degree = m
        self.min_degree = (m + 1) // 2

    def trav_pre(self, fn):
        def trav_pre_at(node):
            if node is None:
                return
            fn(node)
            for child in node.children:
                trav_pre_at(child)

        trav_pre_at(self._root)

    def check_tree(self):
        self.trav_pre(self.check_at)

    def check_at(self, node):
        if not self._root.keys:
            return
        assert len(node.keys) + 1 == len(node.children)
        assert len(node.children) >= self.min_degree
        assert len(node.children) <= self.max_degree
        if node.parent:
            assert node in node.parent.children
        if node.children[0]:
            for child in node.children:
                assert child.parent == node

    def search(self, key):
        v = self._root
        self._hot = None
        while v:
            r = bisect.bisect_right(v.keys, key)
            if r > 0 and key == v.keys[r - 1]:
                return v
            self._hot = v
            v = v.children[r]

        return None


    def insert(self, key):
        v = self.search(key)
        if v:
            return False
        r = bisect.bisect_right(self._hot.keys, key)
        self._hot.keys.insert(r, key)
        self._hot.children.insert(r + 1, None)
        self.solve_overflow(self._hot)
        self.check_tree()
        return True

    def solve_overflow(self, v):
        if len(v.children) <= self.max_degree:
            return
        s = self.max_degree // 2
        u = B_Node()
        left_keys, mid_key, right_keys = v.keys[:s], v.keys[s], v.keys[s+1:]
        left_children, right_children = v.children[:s+1], v.children[s+1:]

        u.keys = right_keys
        u.children = right_children
        v.keys = left_keys
        v.children = left_children
        if u.children[0]:
            for child in u.children:
                child.parent = u

        p = v.parent
        if p is None:
            p = self._root = B_Node()
            p.children[0] = v
            v.parent = p

        r = bisect.bisect_right(p.keys, v.keys[0])
        p.keys.insert(r, mid_key)
        p.children.insert(r+1, u)
        u.parent = p

        self.solve_overflow(p)

    def remove(self, key: B_Node):
        v = self.search(key)
        if v is None:
            return False
        r = bisect.bisect_right(v.keys, key) - 1
        if v.children[0]:
            u = v.children[r+1] # right child
            while u.children[0]:
                u = u.children[0]
            v.keys[r] = u.keys[0]
            v = u
            r = 0

        del v.keys[r]
        del v.children[r+1]
        self.solve_underflow(v)
        self.check_tree()


    def solve_underflow(self, v: B_Node):
        if (len(v.children) >= self.min_degree):
            return
        p = v.parent

        if p is None:
            if len(v.keys) == 0 and v.children[0]:
                self._root = v.children[0]
                self._root.parent = None
            return

        r = p.children.index(v)

        # Case 1: Borrow from left
        if r > 0:
            ls = p.children[r - 1]
            if len(ls.children) > self.min_degree:
                v.keys.insert(0, p.keys[r - 1])
                p.keys[r - 1] = ls.keys.pop(-1)
                v.children.insert(0, ls.children.pop(-1))
                if v.children[0]:
                    v.children[0].parent = v
                return
        # Case 2: Borrow from right
        if r < len(p.children) - 1:
            rs = p.children[r + 1]
            if len(rs.children) > self.min_degree:
                v.keys.append(p.keys[r])
                p.keys[r] = rs.keys.pop(0)
                v.children.append(rs.children.pop(0))
                if v.children[-1]:
                    v.children[-1].parent = v
                return
        # Case 3: Borrow from parent
        if r > 0: # Combine with left
            ls = p.children[r - 1]
            ls.keys.append(p.keys.pop(r - 1))
            p.children.pop(r)
            ls.keys.extend(v.keys)
            if v.children[0]:
                for child in v.children:
                    child.parent = ls
            ls.children.extend(v.children)
        else: # Combine with right
            rs = p.children[r + 1]
            v.keys.insert(0, p.keys.pop(r))
            p.children.pop(r + 1)
            v.keys.extend(rs.keys)
            if rs.children[0]:
                for child in rs.children:
                    child.parent = v
            v.children.extend(rs.children)

        self.solve_underflow(p)

if __name__ == '__main__':
    import random
    bt = B_Tree()
    for i in range(10000):
        random_int = random.randint(1, 60)
        if i % 2 == 0:
            bt.insert(random_int)
        else:
            bt.remove(random_int)