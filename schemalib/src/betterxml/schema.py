#
# Beginnings of the PySchema prototype
#

class Schema(object):
    def __init__(self, namespace):
        self.namespace = namespace
        self.start = None
        self.elements = {}

    def Element(self, name):
        e = Element(name, self)
        self.elements[name] = e
        return e

def spaces(n):
    return n * " "

class Expr(object):
    def __or__(self, other):
        oneOf = OneOf()
        oneOf.add(self)
        oneOf.add(other)
        return oneOf

    def __and__(self, other):
        seq = Seq()
        seq.add(self)
        seq.add(other)
        return seq

    def add(self, term):
        raise "This Expr has no terms."

    def pprint(self, indent):
        pass

class Seq(Expr):
    def __init__(self, existing=None):
        if not existing:
            self.terms = []
        elif existing is Seq:
            self.terms = existing.terms[:]
        else:
            self.terms = [terms]

    def __and__(self, other):
        self.add(other)
        return self

    def pprint(self, indent):
        print spaces(indent) + "&"
        for term in self.terms:
            term.pprint(indent+1)

    def add(self, term):
        self.terms.append(term)

class OneOf(Expr):
    def __init__(self, existing=None):
        if not existing:
            self.terms = []
        elif existing is OneOf:
            self.terms = existing.terms[:]
        else:
            self.terms = [existing]

    def __or__(self, other):
        self.add(other)
        return self

    def pprint(self, indent):
        print spaces(indent) + "|"
        for term in self.terms:
            term.pprint(indent+1)

    def add(self, term):
        self.terms.append(term)



class Occurs(Expr):
    def __init__(self, expr, minimum=0, maximum=None):
        self.term = expr
        self.minimum = minimum
        self.maximum = maximum

    def pprint(self, indent):
        if self.maximum:
            print spaces(indent) + str((self.minimum, self.maximum))
        else:
            print spaces(indent) + str((self.minimum,))
        self.term.pprint(indent+1)


def closure(expr):
    return Occurs(expr, 0, None)

def pclosure(expr):
    return Occurs(expr, 1, None)

class Element(Expr):
    def __init__(self, name, schema):
        self.name = name
        self.schema = schema
        self.grammar = None

    def pprint(self, indent):
        print spaces(indent) + "E(" + self.name +")"

    def Attribute(self, name, type):
        a = Attribute(name, type)
        self.attributes[name] = Attribute(name, type, self.schema)
        return a

class Attribute(object):
    def __init__(self, name, type, is_required=True):
        self.name = name
        self.type = type
        self.is_required = is_required
