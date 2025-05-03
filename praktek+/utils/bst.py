# utils/bst.py
class Node:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.left = None
        self.right = None

class BST:
    def __init__(self):
        self.root = None

    def insert(self, key, value):
        def _insert(current, key, value):
            if not current:
                return Node(key, value)
            if key < current.key:
                current.left = _insert(current.left, key, value)
            else:
                current.right = _insert(current.right, key, value)
            return current
        self.root = _insert(self.root, key, value)

    def search(self, key):
        def _search(current, key):
            if not current:
                return None
            if key == current.key:
                return current.value
            elif key < current.key:
                return _search(current.left, key)
            else:
                return _search(current.right, key)
        return _search(self.root, key)