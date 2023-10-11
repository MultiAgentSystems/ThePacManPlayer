from typing import Callable

from logs.logger import Logger

'''
    Implementing the Node BaseClass. 
'''

'''
    Each node must only carry out its functions
    when its tick has beeen set, furthermore, 
    when a node calls a child node, it must itself
    pass the tick to this child, and set its own 
    tick to False until the time the child returns 
    any response. 
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
        self.state = 'Initialized' # Can only be 'Initialized', 'Running', 'Success' or 'Failure'

    def isRootNode(self) -> bool:
        return self.parent is None

    def isLeafNode(self) -> bool:
        return len(self.children) == 0
    
    def getParent(self):
        return self.parent
    
    def setTick(self, tickVal) -> None:
        self.tick = tickVal

    def getTick(self) -> bool:
        return self.tick

    def setState(self, state) -> None:
        self.state = state

    def getState(self) -> str:
        return self.state

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
            self.logger.logInfo(message=f"Set action function. to {str(self.actionFunction)}")
            return 0
        except Exception :
            self.logger.logException(message="Could not set action function.")
            return 1

    def performAction(self, *args) -> dict:
        try :
            if ( self.getTick() is False ):
                self.logger.logWarning(message="Could not perform action. Tick is False.")

            if ( self.actionFunction is None ):
                self.logger.logError(message="Could not perform action. Action Function is None.")
                return {}

            result = self.actionFunction(*args)

            self.setTick(False)

            return {'result': result}
        except Exception :
            self.logger.logException(message="Could not perform action.")
            return {}

    def getAction(self) -> Callable:
        return self.actionFunction

class ConditionNode(Node):
    '''
        ConditionNode class.
    '''
    def __init__(self, conditionFunction : Callable, parent = None, siblingOrder : int = 0, children : list = [] ) -> None:
        super().__init__(parent, siblingOrder, children)
        self.conditionFunction = conditionFunction

    def setCondition(self, conditionFunction : Callable) -> int:
        try :
            self.conditionFunction = conditionFunction
            self.logger.logInfo(message=f"Set condition function. to {str(self.conditionFunction)}")
            return 0
        except Exception :
            self.logger.logException(message="Could not set condition function.")
            return 1
    
    def checkCondition(self, *args) -> dict:
        try :
            if ( self.getTick() is False ):
                self.logger.logWarning(message="Tick is FALSE whilst executing.")

            if ( self.conditionFunction is None ):
                self.logger.logError(message="Could not check condition. Condition Function is None.")
                return {}
            
            result = self.conditionFunction(*args)
            
            if ( result is True ):
                self.setState('Success')
            elif ( result is False ):
                self.setState('Failure')
            else :
                self.setState('Running')
            
            self.setTick(False)

            return {'result': result}
        except Exception :
            self.logger.logException(message="Could not check condition.")
            self.setTick(False)
            return {}

    def getCondition(self) -> Callable:
        return self.conditionFunction

class SelectorNode(Node): # '?'
    '''
        SelectorNode class.

        Iterates over all the children 
        nodes and returns the first
        node that returns True.

        Returns False only if all the 
        nodes return False
    '''
    def __init__(self, parent = None, siblingOrder : int = 0, children : list = [] ) -> None:
        super().__init__(parent, siblingOrder, children)

    def iterateOverChildren(self) -> str:
        self.logger.logInfo(message="Iterating over children.")

        for child in self.children:
            if child is ConditionNode:
                child.setTick(True)

                self.setTick(False)
                childResponse = child.checkCondition()
                self.setTick(True)

                if ( childResponse is 'Running' or childResponse is 'Success' ):
                    self.setState(child.getState())
                    self.setTick(False)
                    return self.getState() 
                   
            elif child is ActionNode:
                child.setTick(True)
                
                self.setTick(False)
                childResponse = child.performAction()
                self.setTick(True)

                if ( childResponse is 'Running' or childResponse is 'Success' ):
                    self.setState(child.getState())
                    self.setTick(False)
                    return self.getState()
            
            elif child is SequenceNode:
                child.setTick(True)
                
                self.setTick(False)
                childResponse = child.iterateOverChildren()
                self.setTick(True)

                if ( childResponse is 'Running' or childResponse is 'Success' ):
                    self.setState(child.getState())
                    self.setTick(False)
                    return self.getState()
        # Code reaching here means that all the children returned False.
        self.state = 'Failure'
        self.setTick(False)
        return 'Failure'


class SequenceNode(Node): # '+'
    '''
        SequenceNode class.

        Iterates over all the children 
        nodes and returns the first
        node that returns False.

        Returns False only if all the 
        nodes return True
    '''
    def __init__(self, parent = None, siblingOrder : int = 0, children : list = [] ) -> None:
        super().__init__(parent, siblingOrder, children)

    def iterateOverChildren(self) -> str:
        for child in self.children:
            
            if child is ConditionNode:
                child.setTick(True)

                self.setTick(False)
                childResponse = child.checkCondition()
                self.setTick(True)

                if ( childResponse is 'Running' or childResponse is 'Failure' ):
                    self.state = child.getState()
                    self.setTick(False)
                    return child.getState()

            elif child is ActionNode:
                child.setTick(True)
                
                self.setTick(False)
                childResponse = child.performAction()
                self.setTick(True)

                if ( childResponse['result'] is False ):
                    self.state = child.getState()
                    self.setTick(False)
                    return child.getState()

            elif child is SequenceNode:
                child.setTick(True)
                
                self.setTick(False)
                childResponse = child.iterateOverChildren()
                self.setTick(True)

                if ( childResponse is 'Running' or childResponse is 'Failure' ):
                    self.state = child.getState()
                    self.setTick(False)
                    return child.getState()
