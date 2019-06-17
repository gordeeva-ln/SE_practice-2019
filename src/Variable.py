class Variables:
    """
    Variables - class for collecting variables.
     Class have only one attribute - dict(key - name, value - value of variable).
     To add a new one use set, to get variable with same name use get(name).
    """

    def __init__(self):
        self.vars = {}

    def set(self, name, val):
        self.vars[name] = val

    def get(self, name):
        if name in self.vars.keys():
            return self.vars[name]
        else:
            raise ValueError("no such variable {}".format(name))