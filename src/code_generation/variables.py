class Variables:
    
    def __init__(self):
        self.stack = {}
        self.vars = []

    def add_var(self, name):
        self.stack[name] = len(self.stack) + 1
        self.vars.append(name)

    def id(self, name):
        return len(self.stack) - self.stack[name] + 1

    def pop_var(self):
        self.stack.pop(self.vars[-1])
        self.vars.pop()

    def add_temp(self):
        name = len(self.stack) + 1
        self.add_var('tmp_' + str(name))

    def peek_last(self):
        return self.vars[-1]

    def get_stack(self):
        stack = '|'
        for v in self.stack:
            stack += 'id: ' + str(self.id(v) ) + 'name :' + v + '|'
        return stack

    def get_copy(self):
        vars_copy = Variables()
        vars_copy.stack = self.stack.copy()
        vars_copy.vars = self.vars.copy()
        return vars_copy
