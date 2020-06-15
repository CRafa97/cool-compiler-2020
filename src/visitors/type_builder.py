from semantic import *

import visitors.visitor as visitor
from pipeline import State
from cl_ast import *
from tools.cmp_errors import *

class TypeBuilder(State):
    def __init__(self, name):
        super().__init__(name)

    def run(self, inputx):
        ast, context = inputx
        self.context = context
        self.visit(ast)
        return ast, self.context

    @visitor.on('node')
    def visit(self, node):
        pass

    @visitor.when(ProgramNode)
    def visit(self, node):
        pass

    class Builder:
        def __init__(self):
            self.context = None
            self.current_type = None

        @visitor.on('node')
        def visit(self, node):
            pass

        @visitor.when(ProgramNode)
        def visit(self, node):
            for dec in node.declarations:
                self.visit(dec)   

        @visitor.when(ClassDeclarationNode)
        def visit(self, node):
            # set current type for this class declaration
            self.current_type = self.context.get_type(node.id)

            # visit func declarations and attr declarations for this class
            for feature in node.features:
                self.visit(feature)

            # compute parent
            if node.parent:
                try:
                    parent = self.context.get_type(node.parent)
                    current = parent
                    while current:
                        if current.name == self.current_type.name:
                            raise SemanticError('<CIRCULAR DEPENDENCY>')
                        current = current.parent
                except SemanticError as e:
                    parent = ErrorType()
                    self.errors.append(e.text) # parent type missing
                
                self.current_type.set_parent(parent)

        @visitor.when(FuncDeclarationNode)
        def visit(self, node):
            args_ids = []
            args_types = []

            for n, t in node.params:
                args_ids.append(n)
                try:
                    args_types.append(self.context.get_type(t))
                except SemanticError as e:
                    args_types.append(ErrorType())
                    self.errors.append(e.text)

            try:
                ret_type = self.context.get_type(node.type)
            except SemanticError as e:
                ret_type = ErrorType()
                self.errors.append(e.text)

            try:
                self.current_type.define_method(node.id, args_ids, args_types, ret_type)
            except:
                self.errors.append(e.text)

        @visitor.when(AttrDeclarationNode)
        def visit(self, node):
            try:
                attr_type = self.context.get_type(node.type)
            except SemanticError as e:
                attr_type = ErrorType()
                self.errors.append(e.text)

            try:
                self.current_type.define_attribute(node.id, attr_type)
            except SemanticError as e:
                self.errors.append(e.text)

    class InheritBuilder:
        def __init__(self):
            self.context = None
            self.current_type = None

        @visitor.when('node')
        def visit(self, node):
            pass

        @visitor.when(ProgramNode)
        def visit(self, node):
            for dec in node.declarations:
                self.visit(dec)   

        @visitor.when(ClassDeclarationNode)
        def visit(self, node):
            # set current type for this class declaration
            self.current_type = self.context.get_type(node.id)
            parent = self.current_type.parent

            # visit func declarations and attr declarations for this class
            if node.parent and parent is not ErrorType():
                for feature in node.features:
                    self.visit(feature)

        @visitor.when(FuncDeclarationNode)
        def visit(self, node):
            # check correct override 
            parent = self.current_type.parent
            

        @visitor.when(AttrDeclarationNode)
        def visit(self, node):
            pass