from typing import Callable

from logs.logger import Logger
'''
    Implementing the Node BaseClass. 
'''

class Node:
    '''
        Node class.
    '''
    def __init__(self, parent = None, siblingOrder : int = 0, children : list = [] ) -> None:
        self.parent = parent
        self.siblingOrder = siblingOrder
        self.children = children
        self.logger = Logger()
        self.tick = False

    def isRootNode(self) -> bool:
        return self.parent is None

    def isLeafNode(self) -> bool:
        return len(self.children) == 0
    
    def getParent(self):
        return self.parent
    
    def __str__(self) -> str:
        printableString = ""
        attributeList = [a for a in dir(self) if not a.startswith('__') and not callable(getattr(self, a))]
        for attribute in attributeList:
            printableString += f"{attribute} : {getattr(self, attribute)}\n"
        return printableString

class ActionNode(Node):
    '''
        ActionNode class.
    '''
    def __init__(self, actionFunction : Callable, parent = None, siblingOrder : int = 0, children : list = [] ) -> None:
        super().__init__(parent, siblingOrder, children)
        self.actionFunction = actionFunction

    def setAction(self, actionFunction : Callable) -> int:
        try :
            self.actionFunction = actionFunction
            return 0
        except Exception :
            self.logger.logException(message="Could not set action function.")
            return 1

    def performAction(self, *args) -> dict:
        try :
            if ( self.actionFunction is None ):
                self.logger.logError(message="Could not perform action. Action Function is None.")
                return {}
            result = self.actionFunction(*args)
            return {'result': result}
        except Exception :
            self.logger.logException(message="Could not perform action.")
            return {}

    def getAction(self) -> Callable:
        return self.actionFunction

class SelectorNode(Node):
    '''
        SelectorNode class.
        Iterates over all the children 
        model nodes and returns the first
        node that returns True.
    '''
    def __init__(self, parent = None, siblingOrder : int = 0, children : list = [] ) -> None:
        super().__init__(parent, siblingOrder, children)

    def  
