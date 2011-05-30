from FlexFunction import *
import sys

from org.betterxml.xelement1.xelement import *
from org.betterxml.xelement1.xparser import *

class FlexPath:
    def __init__(self):
        self.functions = []
    
    def addFunction(self, funcClass, args=None):
        function = funcClass(args)
        self.functions.append(function)

    def evaluate(self, tree):
        for function in self.functions:
            tree = function.evaluate(tree)
        return tree
    

