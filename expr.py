"""
This module contains functions for expression operations.
"""


import collections
import re


_Op = collections.namedtuple('Op', [
    'precedence',
    'associativity'])


_RIGHT, _LEFT = 0,1


_OPS = {
    '^': _Op(precedence=4, associativity=_RIGHT),
    '*': _Op(precedence=3, associativity=_LEFT),
    '/': _Op(precedence=3, associativity=_LEFT),
    '+': _Op(precedence=2, associativity=_LEFT),
    '-': _Op(precedence=2, associativity=_LEFT)}


basic_opeartors_mapper = {
    "+": lambda x,y : x+y,
    "-": lambda x,y : x-y,
    "*": lambda x,y : x*y,
    "/": lambda x,y : x/y,
    "^": lambda x,y : x**y
}


function_mapper = {
    "max": lambda x,y : max(x, y),
    "min": lambda x,y : min(x, y),
    "sin": None
}


class token():
    def __init__(self, sym, is_num=False, is_func=False,
                    is_dummy=False, is_oper=False,
                    is_leftb=False, is_rightb=False):
        self.sym = sym
        self.is_num = is_num
        self.is_func = is_func
        self.is_dummy = is_dummy
        self.is_oper = is_oper
        self.is_leftb = is_leftb
        self.is_rightb = is_rightb
    
    def __str__(self):
        return "token(sym=" + str(self.sym) +\
                    ", is_func=" + str(self.is_func) +\
                    ", is_num=" + str(self.is_num) +\
                    ", is_dummy=" + str(self.is_dummy) +\
                    ", is_oper=" + str(self.is_oper) +\
                    ", is_leftb=" + str(self.is_leftb) +\
                    ", is_rightb=" + str(self.is_rightb) +\
                    ")"
    
    def __repr__(self):
        return self.__str__()


def has_precedence(a, b):
    """Compare two opeartors a and b.
    1. If b is right associativity and has lower precedence than a, return True
    2. If b is left associativity and has lower or same precedence with a, return True
    3. Otherwise, return False
    """
    return ((_OPS[b].associativity == _RIGHT and
             _OPS[a].precedence > _OPS[b].precedence) or
            (_OPS[b].associativity == _LEFT and
             _OPS[a].precedence >= _OPS[b].precedence))


def postfix(e):
    """Convert infix expression to postfix expression and return
    a list that contains all the tokens in postfix order.
    """
    tokens = tokenize(e)
    q = []
    op = []
    index = 0
    while index < len(tokens):
        token = tokens[index]
        if token.is_num or token.is_dummy:
            q.append(token.sym)
        if token.is_leftb:
            op.append(token.sym)
        elif token.is_oper:
            if len(op) > 0:
                while len(op) > 0 and op[-1] != "(" and has_precedence(op[-1], token.sym):
                    q.append(op.pop())
                op.append(token.sym)
            else:
                op.append(token.sym)
        elif token.is_rightb:
            while len(op) > 0 and op[-1] != "(":
                q.append(op.pop())
            op.pop()
        index += 1
    while len(op) > 0:
        q.append(op.pop())
    return q


def is_symbol(s):
    """Return True if given str is a symbol, which means
    it is in '+,-,*,/,^', False otherwise.
    """
    return s in basic_opeartors_mapper


def is_func(s):
    """Return True if its
    """
    pass


def is_digit(s):
    """Return True if given str is a digit, which means it
    is in '0,1,2,3,4,5,6,7,8,9', False otherwise.
    """
    return s in "1234567890"


def is_letter(s):
    """Return True if the given str is a alphabet, which
    means it is in 'a-z,A-Z', False otherwise.
    """
    return s.isalpha()


def tokenize(e):
    """Tokenize the expression and return a list that contains
    all the tokens from start to end. Please notice that ','
    will be ignored. And also, tokenizer will not recongize
    any wrong patterns or errors in the expression.
    """
    index = 0
    eindex = 0
    result = []
    starts, ends = _match_regex(_func_regex(), e)
    while index < len(e):
        if index in starts:
            result.append(token(e[index: ends[eindex]], is_func=True))
            index = ends[eindex]
            eindex += 1
            continue
        t = e[index]
        if is_digit(t):
            d = ""
            while index < len(e) and is_digit(e[index]):
                d += e[index]
                index += 1
            result.append(token(d, is_num=True))
            index -= 1
        elif is_letter(t):
            d = ""
            while index < len(e) and is_letter(e[index]):
                d += e[index]
                index += 1
            result.append(token(d, is_dummy=True))
            index -= 1
        elif t == "(":
            result.append(token(t, is_leftb=True))
        elif t == ")":
            result.append(token(t, is_rightb=True))
        elif is_symbol(t):
            result.append(token(t, is_oper=True))
        index += 1
    return result


def _func_regex():
    "Construct regex for special math functions"
    regex = "("
    for f in function_mapper:
        if "(" in f:
            index = f.find("(")
            regex += f[:index] + "\\" + f[index:] + "|"
        else:
            regex += f + "|"
    return regex[:-1] + ")"


def _match_regex(r, e):
    "Match the functions regex and return a list of start indices and a list of end indices"
    reg = re.compile(r)
    starts, ends = [], []
    for m in reg.finditer(e):
        starts.append(m.start())
        ends.append(m.end())
    return starts, ends
