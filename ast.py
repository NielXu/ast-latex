"""
This module contains `astree` which can add node onto. Abstract Syntax Tree
only supports basic operators. Use `build` to generate a correct AST by a
math expression.
"""


from queue import Queue
import expr
import binarytree
import sys


class node():
    "A node in the AST"
    def __init__(self, sym, parent=None, left=None, right=None):
        self.sym = sym
        self.left = left
        self.parent = parent
        self.right = right
    
    def copy(self):
        return node(self.sym, self.parent, self.left, self.right)


class astree():
    """
    Abstract Syntax Tree is a tree representation of an expression.
    Please notice that this tree only accpets basic operators +,-,*,/
    and the nodes will be inserted in POSTFIX order.

    If one wants to construct AST with infix expression, please convert
    it using `postfix` method first, and then pop elements from the stack
    in order to add them into the tree. Or use `build` directly, which
    supports more functions such as parathensis and so on.
    
    After constructing the tree completely, one can use `preorder`, `inorder`
    and `postorder` to convert the expression to prefix, infix and postfix format.
    """
    def __init__(self):
        self.root = None
        self.cur = None
    
    def add(self, sym):
        if self.root is None:
            self.root = node(sym, None)
            self.cur = self.root
        else:
            if expr.is_symbol(sym) or expr.is_func(sym):
                if self.cur.right is None:
                    self.cur.right = node(sym, self.cur)
                    self.cur = self.cur.right
                elif self.cur.left is None and not expr.is_unary(self.cur.sym):
                    self.cur.left = node(sym, self.cur)
                    self.cur = self.cur.left
                else:
                    while self.cur.left is not None or expr.is_unary(self.cur.sym):
                        self.cur = self.cur.parent
                    self.cur.left = node(sym, self.cur)
                    self.cur = self.cur.left
            else:
                if self.cur.right is None:
                    self.cur.right = node(sym, self.cur)
                elif self.cur.left is None and not expr.is_unary(self.cur.sym):
                    self.cur.left = node(sym, self.cur)
                else:
                    while self.cur.left is not None or expr.is_unary(self.cur.sym):
                        self.cur = self.cur.parent
                    self.cur.left = node(sym, self.cur)

    def evaluate(self):
        "Evaluate the result of the AST, and return the value as `float`."
        return evaluate(self.root)
    
    def bfs(self):
        """
        Travel the tree in `breadth first search` way, which is from left to
        right and level by level. And return a list that contains the symbols.
        """
        q = Queue()
        q.put(self.root)
        s = []
        while q.qsize() > 0:
            node = q.get()
            s.append(node.sym)
            if node.left is not None:
                q.put(node.left)
            if node.right is not None:
                q.put(node.right)
        return s
    
    def inorder(self):
        """
        Travel the tree by `in-order` way, and return a list that contains
        the symbols.
        """
        li = []
        def travel(node):
            if node is not None:
                travel(node.left)
                li.append(node.sym)
                print(node.sym, end=" ")
                travel(node.right)
        print()
        travel(self.root)
        return li
    
    def preorder(self):
        """
        Travel the tree by `pre-order` way, and return a list that contains
        the symbols.
        """
        li = []
        def travel(node):
            if node is not None:
                print(node.sym, end=" ")
                li.append(node.sym)
                travel(node.left)
                travel(node.right)
        print()
        travel(self.root)
        return li
    
    def postorder(self):
        """
        Travel the tree by `post-order` way, and return a list that contains
        the symbols.
        """
        li = []
        def travel(node):
            if node is not None:
                travel(node.left)
                travel(node.right)
                print(node.sym, end=" ")
                li.append(node.sym)
        print()
        travel(self.root)
        return li
    
    def copy(self):
        a = astree()
        a.root = _clone(self.root)
        return a


def evaluate(node):
    """
    Evaluate the result of a AST by a given node. Please
    notice that not all AST can be evaluated. Only the
    tree that contains valid numbers or symbols can be
    evaluated.
    """
    if node is None:
        return 0
    if expr.is_unary(node.sym):
        return expr.function_mapper[node.sym](evaluate(node.right))
    if expr.is_number(node.sym):
        return float(node.sym)
    if expr.is_special_number(node.sym):
        return expr.special_number[node.sym]
    left = evaluate(node.left)
    right = evaluate(node.right)
    return expr.symbols[node.sym](left, right)


def build(e):
    """
    Build and return a `astree` by given INFIX expression. Infix
    expression means expressions that placed operators between
    numbers, such as `1+1`.

    This function not only support math expressions, but
    also support expressions in general, for example `a+b`.
    However, only math expressions can be evaluated.

    Support operators:
    ------
    Basic:
        + - * / ^ ( )
    Functions:
        sin, cos, tan, ln, log, abs
    Special numbers:
        pi, e
    """
    e = e.replace(" ", "")
    p = expr.postfix(e)
    ast = astree()
    while len(p) > 0:
        ast.add(p.pop())
    return ast


def level_order(ast):
    """Travel the given AST level by level and return a list
    that contains list of nodes at each level, start from
    root to the most bottom.
    """
    levels = []
    _level_traversal(ast.root, 0, levels)
    return levels


def max_depth(ast):
    "Get the max depth of a given AST"
    return _max_depth(ast.root)


def view(ast):
    "View the AST on console"
    a = ast.copy()
    _extend_tree(a, a.root, max_depth(a))
    print(binarytree.build(a.bfs()))


def _level_traversal(root, level, tlist):
    "Travel the tree level by level and save each level in list"
    if root is None:
        return

    if level >= len(tlist):
        l = []
        tlist.append(l)
    tlist[level].append(root.sym)
    _level_traversal(root.left, level+1, tlist)
    _level_traversal(root.right, level+1, tlist)


def _max_depth(n):
    if n is None:
        return 0
    left = _max_depth(n.left)
    right = _max_depth(n.right)
    return max(left, right) + 1


def _level_traversal_node(root, level, tlist):
    if root is None:
        return

    if level >= len(tlist):
        l = []
        tlist.append(l)
    tlist[level].append(root)
    _level_traversal_node(root.left, level+1, tlist)
    _level_traversal_node(root.right, level+1, tlist)


def _clone(n):
    if n is None:
        return  
    node = n.copy()
    node.left = _clone(n.left)
    node.right = _clone(n.right)
    return node


def _extend_tree(a, n, md):
    if n is None:
        return
    if n.left is None and _at_level(n, a) != md:
        n.left = node(None)
    if n.right is None and _at_level(n, a) != md:
        n.right = node(None)
    _extend_tree(a, n.left, md)
    _extend_tree(a, n.right, md)


def _at_level(n, tree):
    levels = []
    _level_traversal_node(tree.root, 0, levels)
    for index in range(len(levels)):
        if n in levels[index]:
            return index+1
    return -1


def main():
    import argparse
    parser = argparse.ArgumentParser(prog="AST",
        description="Generate and view Abstract-Syntax-Tree")
    parser.add_argument("eval",
        help="Evaluate the given expression and display the result if possible",
        metavar="expr",
        nargs=1)
    parser.add_argument("-v", "--view",
        help="View the abstract-syntax-tree that generated by the given expression",
        required=False,
        action="store_true")
    args = parser.parse_args()
    exp = args.eval[0]
    a = build(exp)
    print(a.evaluate())
    if args.view:
        view(a)


def test():
    a = build("1^(2*2)/3")
    view(a)


if __name__ == "__main__":
    main()
