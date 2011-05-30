from Exceptions import *

class FlexFunction:
    '''
    Root class for all flex functions.
    '''
    def __init__(self, args):
        self.args = args
        self.validateArgs()
        
    def validateArgs(self):
        pass
    
    def evaluate(self, currentData):
        pass 

class Child(FlexFunction):
    '''
     The Child FlexFunction gets all children Elements from the data set given 
     to the evaluate function.This accepts the 0 or 1 items in the passed in 
     array of arguments.  0 items means that all children elements of each 
     element in the current data set will be returned.  If 1 item is in args 
     then that item is the name of the desired children. Then, evaluate will 
     return all children of the elements in the current data set that match the 
     name.
     
     author nabicht
    '''
    def validateArgs(self):
        if(self.args and len(self.args) > 1):
            raise InvalidFunctionArguments("Invalid Arguments! Child only takes 0 or 1 argument.")
    
    def evaluate(self, currentData):
        results = list()
        if(not currentData):
            return None
        elif(not self.args or len(self.args) == 0):
            for node in currentData:
                #add type check?
                results.extend(node.getChildren()[:])
        elif(self.args and len(self.args) == 1):
            for node in currentData:
                results.extend(node.getChildrenByName(self.args[0]))
        return results

class First(FlexFunction):
    def validateArgs(self):
        #arguments are passed in then can't evaluate
        if(self.args):
            raise InvalidFunctionArguments("Invalid Arguments! First takes no arguments.")
    
    def evaluate(self, currentData):
        if(currentData == None):
            return None
    
        results = list()
        if (len(currentData) > 0):
            results.append(currentData[0])
        return results

class HasAttribute(FlexFunction):
    def validateArgs(self):
        #arguments are passed in then can't evaluate
        if(not self.args or len(self.args) != 1):
            raise InvalidFunctionArguments("Invalid Arguments! HasAttribute takes exactly 1 argument.")
    
    def evaluate(self, currentData):
        if(currentData == None):
            return None
        
        return [node for node in currentData if node.hasAttributes(self.args)]

class HasAttributeWithValueContains(FlexFunction):
    def validateArgs(self):
        #arguments are passed in then can't evaluate
        if(self.args == None or len(self.args) != 2): 
            raise InvalidFunctionArguments("Invalid Arguments! HasAttributeWithValueContains takes exactly 2 arguments.")
    
    def evaluate(self, currentData):
        if(currentData == None):
            return None

        return [node for node in currentData
                if node.getAttribute(self.args[0]).__contains__(self.args[1])]

class HasAttributeWithValue(FlexFunction):
    def validateArgs(self):
        if (not args or len(args) != 2):
            raise InvalidFunctionArguments("Invalid Arguments! HasAttributeWithValue takes exactly 2 arguments.", args)
    
    def evaluate(self, currentData):
        if (currentData == None):
            return None
		
        return [node for node in currentData if node.getAttribute(self.args[0]) == self.args[1]]
                
class HasPCDataContains(FlexFunction):
    def validateArgs(self):
        if (self.args == None or len(self.args) != 1):
            raise InvalidFunctionArguments("Invalid Arguments! HasPCDataContains takes exactly one argument.")
    
    def evaluate(self, currentData):
        if(currentData == None):
            return null
        
        return [node for node in currentData if node.getText().__contains__(self.args[0])]
        

class HasPCData(FlexFunction):
    def validateArgs(self):
        if(not (self.args == None or len(self.args) == 0)):
            raise InvalidFunctionArguments("Invalid Arguments! HasPCData takes no arguments.")
    
    def evaluate(self, currentData):
        if(currentData == None):
            return None
		
        return [node for node in currentData if (node.getText() != None) and (len(node.getText())>0)]

class Last(FlexFunction):
    def validateArgs(self):
        if(not (self.args == None or len(self.args) == 0)):
            raise InvalidFunctionArguments("Invalid Arguments! Last takes no arguments.")
    
    def evaluate(self, currentData):
        if(currentData == None):
            return None

        results = list()
		
        size = len(currentData)
        if(size != 0):
            results.append(currentData[size - 1])
		
        return results

class PCDataContains(FlexFunction):
    def validateArgs(self):
        if(self.args == None or len(self.args) != 1):
          raise InvalidFunctionArguments("Invalid Arguments! PCDataContains takes exactly one argument.")
    
    def evaluate(self, currentData):
        if(currentData == None):
            return None

        return [node.getText() for node in currentData if node.getText().__contains__(self.args[0])]

class PCData(FlexFunction):
    def validateArgs(self):
        if(not (self.args == None or len(self.args) == 0)):
            raise InvalidFunctionArguments("Invalid Arguments! Last takes no arguments.")
    
    def evaluate(self, currentData):
        if(currentData == None):
            return None

        return [node.getText() for node in currentData]

class Pos(FlexFunction):
    def validateArgs(self):
        #if too many arguments are passed in, then you can't evaluate
        #if no argument is passed in then you can't evaluate
        if (not self.args or len(self.args) != 1):
            raise InvalidFunctionArguments("Invalid Arguments! Pos takes exactly one argument.")
        
        try:
            self.requestedPos = int(self.args[0])
        except ValueError:
            raiseInvalidFunctionArguments("Invalid Arguments! The argument for Pos must be an integer >= 0.")
        
        if (self.requestedPos < 0):
            raise InvalidFunctionArguments("Invalid Arguments! The argument for Pos must be an integer >= 0.")

    def evaluate(self, currentData):
        '''Gets the the item from the given position of the current data set.  The array of argument
        strings should contain 1 item. This item should be the position you want to retrieve, which by
        definition must be greater than or equal to 0.  The number must be in numeric form, which means 
        "one" is invalid but "1" is valid.  The first item in the current data set has the position "0".'''
        if (currentData == None):
            return None
        results = list()
        
        if (self.requestedPos < len(currentData)):
            results.append(currentData[self.requestedPos])
        
        return results


class Range(FlexFunction):
    def validateArgs(self):
        if (not self.args or len(self.args) != 2):
            raise InvalidFunctionArguments("Invalid Arguments! Range takes exactly two arguments.")
		
        try:
            self.requestedStart = int(self.args[0])
            self.requestedStop  = int(self.args[1])
        except ValueError:
            raise InvalidFunctionArguments("Invalid Arguments! The arguments for Range must be integers >= 0.")	
        
        if(self.requestedStart < 0 or self.requestedStop < 0):
            raise InvalidFunctionArguments("Invalid Arguments! The arguments for Range must be integers >= 0.")
		
        if(self.requestedStart >= self.requestedStop):
            raise InvalidFunctionArguments("Invalid Arguments! The second argument of Range must be greater than the first argument.")

    def evaluate(self, currentData):
        if (currentData == None):
            return None

        if (self.requestedStart < len(currentData)):
            stop = min(self.requestedStop, len(currentData))
            return currentData[self.requestedStart:stop]

        return []

