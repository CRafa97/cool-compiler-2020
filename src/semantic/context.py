"""Contains Context Structures"""

import itertools as itt
from .types import *
from .error import SemanticError

class Context:
    def __init__(self):
        self.types = {}

    def create_type(self, name:str):
        if name in self.types:
            raise SemanticError(f'Type with the same name ({name}) already in context.')
        typex = self.types[name] = Type(name)
        return typex

    def get_type(self, name:str):
        try:
            return self.types[name]
        except KeyError:
            raise SemanticError(f'Type "{name}" is not defined.')

    def __str__(self):
        return '{\n\t' + '\n\t'.join(y for x in self.types.values() for y in str(x).split('\n')) + '\n}'

    def __repr__(self):
        return str(self)

class VariableInfo:
    def __init__(self, name, vtype):
        self.name = name
        self.type = vtype

    def __str__(self):
        return f'{self.name} : {self.type.name}'

    def __repr__(self):
        return str(self)

class Scope:
    def __init__(self, parent=None):
        #self.context = context
        self.locals = []
        self.parent = parent
        self.children = []
        self.expr_dict = { }
        self.functions = { }
        self.index = 0 if parent is None else len(parent)

    def __len__(self):
        return len(self.locals)

    def __str__(self):
        res = ''
        for scope in self.children:
            try:
                classx = scope.locals[0]
                name = classx.type.name
            except:
                name = 'miss'
            res += name + scope.tab_level(1, '', 1) #'\n\t' +  ('\n' + '\t').join(str(local) for local in scope.locals) + '\n'
        return res

    def tab_level(self, tabs, name, num):
        res = ('\t' * tabs) +  ('\n' + ('\t' * tabs)).join(str(local) for local in self.locals)
        if self.functions:
            children = '\n'.join(v.tab_level(tabs + 1, '[method] ' + k, num) for k, v in self.functions.items())
        else:
            children = '\n'.join(child.tab_level(tabs + 1, num, num + 1) for child in self.children)
        return "\t" * (tabs-1) + f'{name}' + "\t" * tabs + f'\n{res}\n{children}'

    def __repr__(self):
        return str(self)

    def create_child(self):
        child = Scope(self)
        self.children.append(child)
        return child

    def define_variable(self, vname, vtype):
        info = VariableInfo(vname, vtype)
        self.locals.append(info)
        return info

    def define_attribute(self, attr):
        self.locals.append(attr)

    def find_variable(self, vname, index=None):
        locals = self.locals if index is None else itt.islice(self.locals, index)
        try:
            return next(x for x in locals if x.name == vname)
        except StopIteration:
            return self.parent.find_variable(vname, self.index) if self.parent else None

    def get_class_scope(self):
        if self.parent == None or self.parent.parent == None:
            return self
        return self.parent.get_class_scope()

    def is_defined(self, vname):
        return self.find_variable(vname) is not None

    def is_local(self, vname):
        return any(True for x in self.locals if x.name == vname)