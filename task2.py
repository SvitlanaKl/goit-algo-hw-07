# Завдання 2
# Напишіть алгоритм (функцію), який знаходить найменше значення у двійковому дереві пошуку або в AVL-дереві.

import networkx as nx
import matplotlib.pyplot as plt

class AVLNode:
    def __init__(self, key):
        self.key = key
        self.height = 1
        self.left = None
        self.right = None

def get_height(node):
    if not node:
        return 0
    return node.height

def get_balance(node):
    if not node:
        return 0
    return get_height(node.left) - get_height(node.right)

def left_rotate(z):
    y = z.right
    T2 = y.left

    y.left = z
    z.right = T2

    z.height = 1 + max(get_height(z.left), get_height(z.right))
    y.height = 1 + max(get_height(y.left), get_height(y.right))

    return y

def right_rotate(y):
    x = y.left
    T3 = x.right

    x.right = y
    y.left = T3

    y.height = 1 + max(get_height(y.left), get_height(y.right))
    x.height = 1 + max(get_height(x.left), get_height(x.right))

    return x

def insert(root, key):
    if not root:
        return AVLNode(key)

    if key < root.key:
        root.left = insert(root.left, key)
    else:
        root.right = insert(root.right, key)

    root.height = 1 + max(get_height(root.left), get_height(root.right))

    balance = get_balance(root)

    # Left Left Case
    if balance > 1 and key < root.left.key:
        return right_rotate(root)

    # Right Right Case
    if balance < -1 and key > root.right.key:
        return left_rotate(root)

    # Left Right Case
    if balance > 1 and key > root.left.key:
        root.left = left_rotate(root.left)
        return right_rotate(root)

    # Right Left Case
    if balance < -1 and key < root.right.key:
        root.right = right_rotate(root.right)
        return left_rotate(root)

    return root

def find_min_value(node):
    current = node
    while current.left is not None:
        current = current.left
    return current.key

# Вставка значень для створення збалансованого AVL-дерева
root = None
keys = [10, 20, 30, 25, 28, 27, 5, 15, 35, 40]

for key in keys:
    root = insert(root, key)

# Знаходження найменшого значення
min_value = find_min_value(root)
print("Найменше значення в AVL-дереві:", min_value)

# Функція для побудови графу дерева
def build_graph(graph, node, pos=None, x=0, y=0, layer=1):
    if pos is None:
        pos = {}
    pos[node.key] = (x, y)
    if node.left:
        graph.add_edge(node.key, node.left.key)
        l = x - 1 / layer
        build_graph(graph, node.left, pos=pos, x=l, y=y-1, layer=layer+1)
    if node.right:
        graph.add_edge(node.key, node.right.key)
        r = x + 1 / layer
        build_graph(graph, node.right, pos=pos, x=r, y=y-1, layer=layer+1)
    return graph, pos

# Побудова графу дерева
graph = nx.DiGraph()
graph, pos = build_graph(graph, root)

# Візуалізація дерева
plt.figure(figsize=(10, 7))
nx.draw(graph, pos, with_labels=True, node_size=5000, node_color="skyblue", font_size=16, font_weight="bold", arrows=False)
plt.title("AVL-Дерево")
plt.show()
