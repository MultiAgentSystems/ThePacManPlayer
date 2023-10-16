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
    def __init__(self, parent = None, siblingOrder : int = -1, children : list = [] ) -> None:
        self.parent = parent
        self.siblingOrder = siblingOrder
        self.children = children
        self.tick = False
        self.state = 'Initialized' # Can only be 'Initialized', 'Error', 'Running', 'Success' or 'Failure'
        self._name = 'Node'

    def isRootNode(self) -> bool:
        return self.parent is None

    def isLeafNode(self) -> bool:
        return len(self.children) == 0
    
    def setParent(self, parent) -> None:
        self.parent = parent

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
    
    def addChild(self, child, position = None) -> int:
        if ( position is None or position >= len(self.children) ):
            self.children.append(child)
        elif ( position < len(self.children) ):
            self.children.insert(position, child)
        self.children.append(child)
        return len(self.children)

    def getChildren(self) -> list:
        return self.children

    def removeChild(self, child) -> int:
        if ( child in self.children ):
            self.children.remove(child)
        else :
            return -1
        return len(self.children)
    
    def setSiblingOrder(self, siblingOrder : int) -> None:
        self.siblingOrder = siblingOrder

    def getSiblingOrder(self) -> int:
        return self.siblingOrder
    
    def getYoungestChild(self):
        if ( len(self.getChildren()) == 0 ):
            return None
        else :
            return self.getChildren()[-1]

    def __str__(self) -> str:

        printableString = ""
        attributeList = [a for a in dir(self) if not a.startswith('__') and not callable(getattr(self, a))]
        for attribute in attributeList:
            printableString += f"{attribute} : {getattr(self, attribute)}\n"
        return "*"*20 + "\n" + printableString + "*"*20

class ActionNode(Node):
    '''
        ActionNode class.
    '''
    def __init__(self, actionFunction : Callable , parent = None, siblingOrder : int = 0, children : list = [], description = "" , logger = None) -> None:
        super().__init__(parent, siblingOrder, children)
        self._name = 'ActionNode'
        self.actionFunction = actionFunction
        if ( logger is None ):
            logger = Logger()
        self.logger = logger
        if description == "" :
            description = str(actionFunction)
        self.actionDescription = description

    def setAction(self, actionFunction : Callable, description = "") -> int:
        try :
            self.actionFunction = actionFunction
            if description == "" :
                description = str(actionFunction)
            self.actionDescription = description
            self.logger.logInfo(message=f"Set action function. to {str(self.actionFunction)}")
            return 0
        except Exception :
            self.logger.logException(message="Could not set action function.")
            return 1

    def performAction(self, *args) -> dict:
        try :
            if ( self.getTick() is False ):
                self.logger.logWarning(message="Tick is FALSE whilst executing.")

            if ( self.actionFunction is None ):
                self.logger.logError(message="Could not perform action. Action Function is None.")
                return {}

            result = self.actionFunction(*args)
            
            self.logger.logInfo(message=f"Action function description : {str(self.actionDescription)}")
            self.logger.logInfo(message=f"Action function returned {str(result)}")
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
    def __init__(self, conditionFunction : Callable, parent = None, siblingOrder : int = 0, children : list = [], description = "", logger = None ) -> None:
        super().__init__(parent, siblingOrder, children)
        self._name = 'ConditionNode'
        self.conditionFunction = conditionFunction
        if description == "" :
            description = str(conditionFunction)
        self.conditionDescription = description
        if ( logger is None ):
            logger = Logger()
        self.logger = logger

    def setCondition(self, conditionFunction : Callable, description = "") -> int:
        try :
            self.conditionFunction = conditionFunction
            if description == "" :
                description = str(conditionFunction)
            self.conditionDescription = description
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
            
            self.logger.logInfo(message=f"Condition function : Description : {str(self.conditionDescription)}")
            result = self.conditionFunction(*args)
            self.logger.logInfo(message=f"Condition function returned {str(result)}")
            
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
    def __init__(self, parent = None, siblingOrder : int = 0, children : list = [] , logger = None) -> None:
        super().__init__(parent, siblingOrder, children)
        self._name = 'SelectorNode'
        if ( logger is None ):
            logger = Logger()
        self.logger = logger

    def iterateOverChildren(self) -> str:
        self.logger.logInfo(message="Iterating over children.")

        for child in self.children:
            child.setTick(True)
            self.setTick(False)
            
            childResponse = None

            if ( child is ConditionNode ):
                childResponse = child.checkCondition()
                self.logger.logInfo(message=f"ConditionNode returned {str(childResponse)}")
            elif child is ActionNode:
                childResponse = child.performAction()
                self.logger.logInfo(message=f"ActionNode returned {str(childResponse)}")
            elif child is SequenceNode:
                childResponse = child.iterateOverChildren()
                self.logger.logInfo(message=f"SequenceNode returned {str(childResponse)}")
            elif child is SelectorNode:
                child.setTick(False)
                self.logger.logError(message="SelectorNode cannot be a child of SelectorNode.")
                childResponse = 'Error'
            
            self.logger.logInfo(message=f"Obtained Child Response : {str(childResponse)}")
            self.setTick(True)
            if ( childResponse == 'Running' or childResponse == 'Success' or childResponse == 'Error' ):
                self.setState(child.getState())
                self.setTick(False)
                return self.getState()
        
        # Code reaching here means that all the children returned Failure.
        self.logger.logInfo(message="All children returned Failure.")
        self.setState('Failure')
        self.setTick(False)
        return self.getState()


class SequenceNode(Node): # '->'
    '''
        SequenceNode class.

        Iterates over all the children 
        nodes and returns the first
        node that returns False.

        Returns False only if all the 
        nodes return True
    '''
    def __init__(self, parent = None, siblingOrder : int = 0, children : list = [] , logger = None) -> None:
        super().__init__(parent, siblingOrder, children)
        self._name = 'SequenceNode'
        if ( logger is None ):
            logger = Logger()
        self.logger = logger

    def iterateOverChildren(self) -> str:
        self.logger.logInfo(message="Iterating over children.")

        for child in self.children:
            child.setTick(True)
            self.setTick(False)
            
            childResponse = None

            if ( child is ConditionNode ):
                childResponse = child.checkCondition()
                self.logger.logInfo(message=f"ConditionNode returned {str(childResponse)}")
            elif child is ActionNode:
                childResponse = child.performAction()
                self.logger.logInfo(message=f"ActionNode returned {str(childResponse)}")
            elif child is SelectorNode:
                childResponse = child.iterateOverChildren()
                self.logger.logInfo(message=f"SelectorNode returned {str(childResponse)}")
            elif child is SequenceNode:
                child.setTick(False)
                self.logger.logError(message="SequenceNode cannot be a child of SequenceNode.")
                childResponse = 'Error'
            
            self.logger.logInfo(message=f"Obtained Child Response : {str(childResponse)}")
            self.setTick(True)
            if ( childResponse == 'Running' or childResponse == 'Failure' or childResponse == 'Error' ):
                self.setState(child.getState())
                self.setTick(False)
                return self.getState()
        
        # Code reaching here means that all the children returned Success.
        self.logger.logInfo(message="All children returned Success.")
        self.setState('Success')
        self.setTick(False)
        return self.getState()
