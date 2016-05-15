import numpy as n


class Plane:
    def __init__(self, points, normals):
        pass


class Node:
    def __init__(self, key, left=None, right=None, parent=None):
        self.key = key
        if left is not None:
            self.left = left
        else:
            self.left = None
        if right is not None:
            self.right = right
        else:
            self.right = None
        if parent is not None:
            parent = parent

    def setNewLeft(self, left):
        self.left = Node(left)

    def setNewRight(self, right):
        self.right = Node(right)

    def setLeft(self, left_node):
        self.left = left_node

    def setRight(self, right_node):
        self.right = right_node

    def setNewParent(self, parent):
        self.parent = Node(parent)

    def setParent(self, parent_node):
        self.parent = parent_node


class BSP:
    def __init__(self, *args):
        self.size = len(args)
        self.root = Node(args[0])
