from BST import BST, Node
from enum import Enum

class Color(Enum):
    BLACK = 0
    RED = 1


class RB_Node(Node):
    def __init__(self, color, *args) -> None:
        super().__init__(*args)
        self.color = color

class RB_Tree(BST):
    def check_at(node):
        super().check_at()
        assert isinstance(node, RB_Node)
        