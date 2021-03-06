#!/usr/bin/env python
# coding: utf-8

# In[3]:


import string


# In[53]:


def dynamic_var(X):
    if X in globals():
        return globals()[X]
    else:
        globals()[X] = Symbol(X)
        return globals()[X]
# globals().__getitem__ = dynamic_var


# In[217]:


class Expression:
#     def __init__(self, terms=None, *extra_terms):
    def __init__(self, *terms):
        if terms is None:
            terms = []
#         terms.extend(extra_terms)
        self.terms = terms
        self.group = True
    def stringify(self, level=0):
        result = ' '.join([(T.stringify(level+1) if isinstance(T, Expression) else str(T)) for T in self.terms])
        if all([self.group, level!=0, self.terms]):
            result = f'({result})'
        return result
    def __str__(self):
#         return ' '.join(map(str, self.terms))
        return self.stringify()
    def __repr__(self):
        return str(self)


# In[218]:


class Operator(Expression):
    def __init__(self, symbol, *inputs, **kwargs):
        super().__init__(*inputs, **kwargs)
        self.symbol = symbol
        self.inputs = self.terms
    def stringify(self, level=0):
        if len(self.terms) == 2:
            return ' '.join([(T.stringify(level+1) if isinstance(T, Expression) else str(T)) for T in [self.terms[0], self.symbol, self.terms[1]]])
        else:
            return super().__str__(self)
    def __str__(self):
        return self.stringify()


# In[246]:


class Symbol(Expression):
    def __init__(self, name):
        super().__init__()
        self.name = name
#     def __add__(self, B):
#         return Expression(Operator('+', self, B))
    def stringify(self, *args, **kwargs):
        return str(self.name)
    def __str__(self):
        return str(self.name)


# In[247]:


def magic_factory(W):
    return lambda Self, Other: Expression(Operator(W, Self, Other))
def magic_factory_reverse(W):
    return lambda Self, Other: Expression(Operator(W, Other, Self))

for J, K in [('add', '+'), ('sub', '-'), ('mul', '*'), ('truediv', '/'), ('xor', '^')]:
#     for F in [magic_factory, magic_factory_reverse]:
    setattr(
        Expression,
        f'__{J}__',
        magic_factory(K)
    )
    setattr(Expression, f'__r{J}__', magic_factory(K))


# In[248]:


class Session:
    pass
qq = Session


# In[249]:


Expression.__mul__==Expression.__add__


# In[250]:


varnames = list(string.ascii_lowercase)
for C in varnames:
    globals()[C] = Symbol(C)


# In[251]:


((x+5)-10)^2


# In[252]:


# locals()


# In[253]:


# |y|


# In[254]:


# qq<root>
# 3<root>x
# xy


# In[255]:


class Infix:
    def __init__(self, function):
        self.function = function
    def __ror__(self, other):
        return Infix(lambda x, self=self, other=other: self.function(other, x))
    def __or__(self, other):
        return self.function(other)
    def __rlshift__(self, other):
        return Infix(lambda x, self=self, other=other: self.function(other, x))
    def __rshift__(self, other):
        return self.function(other)
    def __call__(self, value1, value2):
        return self.function(value1, value2)


# In[256]:


root = Infix(lambda A, B: B ^ (Symbol(1) / A))
# handling int literals?
# define/apply op?


# In[257]:


3<<root>>x


# In[ ]:




