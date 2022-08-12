from sympy.combinatorics.free_groups import free_group
import numpy as np
from itertools import permutations

F,a,b = free_group("a, b")
a_symb = tuple(a)[0][0]
b_symb = tuple(b)[0][0]
identity = F.identity

def invert(x):
    if x == identity:
        return x
    else:
        return x**(-1)

class F2xF2Algebra:
    def __init__(self, element = dict()):
        # An element is a dict where entries are of the form (x,y) : c
        # where c is a complex number, and x, y are group elements.
        self.element = element

    def __sub__(self, other):
        return self + F2xF2Algebra({x : -other.element[x] for x in other.element})
                

    def simplify(self):
        deleted = 0
        x = self.element.copy()
        for term in x:
            if self.element[term] == 0:
                del self.element[term]

    def transpose(self):
        return F2xF2Algebra({(x[0]**-1, x[1]**-1) : self.element[x] for x in self.element})

    def __add__(self, other):
        element = dict()
        mysupp = set(self.element.keys())
        othersupp = set(other.element.keys())
        for term in mysupp.union(othersupp):
            if term in mysupp and term in othersupp:
                element[term] = self.element[term] + other.element[term]
                continue
            if term in mysupp:
                element[term] = self.element[term]
            if term in othersupp:
                element[term] = other.element[term]
        x = F2xF2Algebra(element)
        x.simplify()
        return x

    def __mul__(self, other):
        element = dict()
        for myterm in self.element:
            for otherterm in other.element:
                newterm = (myterm[0] * otherterm[0], myterm[1] * otherterm[1])
                if newterm not in element:
                    element[newterm] = 0
                element[newterm] += self.element[myterm] * other.element[otherterm]
        x = F2xF2Algebra(element)
        x.simplify()
        return x


    def __str__(self):
        if not self.element:
            return "0"
        return " + ".join(["{} * ({}, {})".format(c, term[0], term[1]) if c != 1 else "({}, {})".format(term[0], term[1]) for term, c in self.element.items()])

    def is_sos(self, S):
        equalities = dict()
        for i in range(len(S)):
            for j in range(len(S)):
                product = ((S[i][0]**(-1))*S[j][0], (S[i][1]**(-1))*S[j][1])
                if product not in equalities:
                    equalities[product] = []
                equalities[product].append((i,j))
        print(equalities)

    def evaluate(self, U, V, W, X):
        val = np.zeros(U.shape)
        for term in self.element:
            x1 = substitute(term[0], U, V)
            x2 = substitute(term[1], W, X)
            val += self.element[term] * x1 @ x2
        return val

    def maximizeEigen(self, k):
        maxEig = -100
        best = None
        iden = np.eye(k)
        for s1 in permutations(range(k), k):
            U = np.kron(matrixify(s1), iden)
            for s2 in permutations(range(k), k):
                V = np.kron(matrixify(s2), iden)
                for s3 in permutations(range(k), k):
                    W = np.kron(iden, matrixify(s3))
                    for s4 in permutations(range(k), k):
                        X = np.kron(iden, matrixify(s4))
                        subbed = self.evaluate(U, V, W, X)
                        val = max(np.linalg.eigvalsh(subbed))
                        if val > maxEig:
                            maxEig = val
                            best = (s1, s2, s3, s4)
                            print("Found better", best)
                            print(maxEig)
                            print(subbed)
        return maxEig, best

def substitute(g, U, V): 
    val = np.eye(*U.shape)
    for let in g.array_form:
        k = let[1]
        if let[0] == a_symb:
            X = U
        elif let[0] == b_symb:
            X = V
        else:
            print("AHHH")
        if k >= 0:
            val = val @ np.linalg.matrix_power(X, k)
        else:
            val = val @ np.linalg.matrix_power(np.transpose(X), -k)
    return val


def matrixify(perm):
    n = len(perm)
    return np.array([[1 if j == perm[i] else 0 for j in range(n)] for i in range(n)])

t = F2xF2Algebra({(a**2*b*a**-1, a*b**3*a) : -2, (a**2*b, b**3*a) : -2, (a**2, (a**-1)*b**3) : -1, (a, b) : 3})
t = t + t.transpose()
print(t.maximizeEigen(5))
