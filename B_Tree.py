import bisect

class B_Node:
    def __init__(self, key):
        self.keys = [key]
        self.parent = None
        self.children = [None, None]

class B_Tree:
    def __init__(self, m):
        self._root = None
        self.max_degree = m
        self.min_degree = m // 2
    
    def search(self, key):
        v = self._root
        self._hot = None 
        while v:
            r = bisect.bisect_right(self.keys, key)
            if r < len(v.keys) and key == v.keys[r]: 
                return v
            self._hot = v
            v = v.children[r]
        
        return None
    
    def insert(self, node):
        key = node.key
        v = self.search(key)
        if v:
            return False
        r = bisect.bisect_right(self._hot.keys, key)
        self._hot.keys.insert(r, key)
        self._hot.children.insert(r + 1, None)
        self.solve_overflow(self._hot)
        return True
    
    def solve_overflow(self, v):
        if len(v.keys) < self.max_degree:
            return
        s = self.max_degree // 2


        p = v.parent


        self.solve_overflow(p)

    

