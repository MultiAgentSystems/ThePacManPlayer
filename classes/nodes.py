from typing import Callable

from logs.logger import Logger

"""
    Implementing the Node BaseClass. 
"""

"""
    Each node must only carry out its functions
    when its tick has beeen set, furthermore, 
    when a node calls a child node, it must itself
    pass the tick to this child, and set its own 
    tick to False until the time the child returns 
    any response. 
"""


class Node:
    """
        Node class.
    """

    def __init__(self, parent=None, siblingOrder: int = -1, children=None) -> None:
        self.parent = parent
        self.siblingOrder = siblingOrder
        self.children = children if children is not None else []
        self.tick = False
        self.state = 'Initialized'  # Can only be 'Initialized', 'Error', 'Running', 'Success' or 'Failure'
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

    def getExecutionOrder(self, backtrack: bool = False) -> list:
        executionOrder = [self]

        for child in self.children:
            executionOrder += child.getExecutionOrder(backtrack=backtrack)
            if (backtrack is True):
                executionOrder += [self]

        return executionOrder

    def addChild(self, child, position=None) -> int:
        if (position is None or position >= len(self.children)):
            self.children.append(child)
        elif (position < len(self.children)):
            self.children.insert(position, child)

        for order, child in enumerate(self.children):
            child.setSiblingOrder(order)
            child.setParent(self)

        return len(self.children)
    
    def setChildren(self, children) -> None:
        self.children = children
        for order, child in enumerate(self.children):
            child.setParent(self)
            child.setSiblingOrder(order)

    def getChildren(self) -> list:
        return self.children

    def removeChild(self, child) -> int:
        if (child in self.children):
            self.children.remove(child)
            for order, child in enumerate(self.children):
                child.setSiblingOrder(order)
        else:
            return -1
        return len(self.children)

    def setSiblingOrder(self, siblingOrder: int) -> None:
        self.siblingOrder = siblingOrder

    def getSiblingOrder(self) -> int:
        return self.siblingOrder

    def getYoungestChild(self):
        if (len(self.getChildren()) == 0):
            return None
        else:
            return self.getChildren()[-1]

    def getLabel(self) -> str:
        raise NotImplementedError
    
    def _isMutable(self):
        return isinstance(self, ActionNode) or isinstance(self, ConditionNode)

    def __str__(self) -> str:
        printableString = ""
        attributeList = [a for a in dir(self) if not a.startswith('__') and not callable(getattr(self, a))]
        for attribute in attributeList:
            printableString += f"{attribute} : {getattr(self, attribute)}\n"
        return "*" * 20 + "\n" + printableString + "*" * 20
    
    def SequenceSelectorAlternate(self):
        for child in self.children:
            if ((isinstance(self, SelectorNode) and isinstance(child, SelectorNode) )
                or (isinstance(child, SequenceNode) and isinstance(self, SequenceNode) )):
                return False
        satisfied = True

        for child in self.children:
            satisfied = satisfied and child.SequenceSelectorAlternate()
        
        return satisfied

    def OnlyChildNodeMeansNoConditonNode(self):
        if ( len( self.getChildren() ) == 1 ):
            if isinstance(self.getChildren()[0], ConditionNode):
                return False
        satisfied = True

        for child in self.children:
            satisfied = satisfied and child.OnlyChildNodeMeansNoConditonNode()

        return satisfied

    def ActionNodesFollowAllConditionNodes(self):
        foundActionNode = False

        for child in self.children :
            if isinstance(child, ConditionNode) and foundActionNode:
                return False
            elif isinstance(child, ActionNode):
                foundActionNode = True
        satisfied = True

        for child in self.children:
            satisfied = satisfied and child.ActionNodesFollowAllConditionNodes()

        return satisfied
    
    def ConditionActionNoChildren(self):
        satisfied = True

        if ( isinstance(self, ConditionNode) or isinstance(self, ActionNode ) ):
            if ( len( self.getChildren() ) != 0 ):
                return False
        
        for child in self.children:
            satisfied = satisfied and child.ConditionActionNoChildren()

        return satisfied

    def SequenceSelectorMustHaveOneChild(self):
        satisfied = True

        if ( isinstance(self, SequenceNode) or isinstance(self, SelectorNode ) ):
            if ( len( self.getChildren() ) == 0 ):
                return False

        for child in self.children:
            satisfied = satisfied and child.SequenceSelectorMustHaveOneChild()

        return satisfied

class ActionNode(Node):
    """
        ActionNode class.
    """

    def __init__(self, actionFunction: Callable, parent=None, siblingOrder: int = 0, children=None, description=None,
                 ) -> None:
        super().__init__(parent, siblingOrder, children)
        self._name = 'ActionNode'
        self.actionFunction = actionFunction
        
        if description is None:
            description = str(actionFunction)
        self.actionDescription = description

    def setAction(self, actionFunction: Callable, description="") -> int:
        try:
            self.actionFunction = actionFunction
            if description == "":
                description = str(actionFunction)
            self.actionDescription = description
            # self.logger.logInfo(message=f"Set action function. to {str(self.actionFunction)}")
            return 0
        except Exception:
            # self.logger.logException(message="Could not set action function.")
            return 1

    def performAction(self, *args) -> dict:
        try:
            # if (self.getTick() is False):
                # self.logger.logWarning(message="Tick is FALSE whilst executing.")

            if (self.actionFunction is None):
                return {'result' : 'Failure', 'action' : 'E'}

            action = self.actionFunction(*args)

            # self.logger.logInfo(message=f"Action function description : {str(self.actionDescription)}")
            # self.logger.logInfo(message=f"Action function returned {str(action)}")
            self.setTick(False)

            if ( action == 'E' ):
                return {'result': 'Failure', 'action' : 'E'}
            else :
                # print(self.actionDescription, f"suggestion : {action}")
                return {'result': 'Success', 'action' : action}
        except Exception:
            # self.logger.logException(message="Could not perform action.")
            return {}

    def getAction(self) -> Callable:
        return self.actionFunction

    def getLabel(self) -> str:
        return f"{self._name}_{self.actionDescription}"


class ConditionNode(Node):
    """
        ConditionNode class.
    """

    def __init__(self, conditionFunction: Callable, parent=None, siblingOrder: int = 0, children=None, description=None,
                 ) -> None:
        super().__init__(parent, siblingOrder, children)
        self._name = 'ConditionNode'
        self.conditionFunction = conditionFunction
        if description is None:
            description = str(conditionFunction)
        self.conditionDescription = description

    def setCondition(self, conditionFunction: Callable, description="") -> int:
        try:
            self.conditionFunction = conditionFunction
            if description == "":
                description = str(conditionFunction)
            self.conditionDescription = description
            # self.logger.logInfo(message=f"Set condition function. to {str(self.conditionFunction)}")
            return 0
        except Exception:
            # self.logger.logException(message="Could not set condition function.")
            return 1

    def checkCondition(self, *args) -> dict:
        try:
            if (self.getTick() is False):
                print("Tick is FALSE whilst executing.")
                # self.logger.logWarning(message="Tick is FALSE whilst executing.")

            if (self.conditionFunction is None):
                # self.logger.logError(message="Could not check condition. Condition Function is None.")
                return {}

            # self.logger.logInfo(message=f"Condition function : Description : {str(self.conditionDescription)}")
            result = self.conditionFunction(*args)
            # self.logger.logInfo(message=f"Condition function returned {str(result)}")

            if (result is True):
                self.setState('Success')
                result = 'Success'
            elif (result is False):
                self.setState('Failure')
                result = 'Failure'
            else:
                self.setState('Running')
                result = 'Running'

            self.setTick(False)

            return {'result': result}
        except Exception:
            # self.logger.logException(message="Could not check condition.")
            self.setTick(False)
            return {}

    def getCondition(self) -> Callable:
        return self.conditionFunction

    def getLabel(self) -> str:
        return f"{self._name}_{self.conditionDescription}"


class SelectorNode(Node):  # '?'
    """
        SelectorNode class.

        Iterates over all the children 
        nodes and returns the first
        node that returns True.

        Returns False only if all the 
        nodes return False
    """

    def __init__(self, parent=None, siblingOrder: int = 0, children=None, ) -> None:
        super().__init__(parent, siblingOrder, children)
        self._name = 'SelectorNode'

    def makeDescision(self, player) -> dict:
        # self.logger.logInfo(message=f"Iterating over children For {self._name}.")
        action = 'E'

        for child in self.children:
            child.setTick(True)
            self.setTick(False)

            childResponse = None

            if ( isinstance(child, ConditionNode) ):
                childResponse = child.checkCondition(player)
                # self.logger.logInfo(message=f"ConditionNode returned {str(childResponse)}")
            elif ( isinstance(child, ActionNode) ):
                childResponse = child.performAction(player)
                # self.logger.logInfo(message=f"ActionNode returned {str(childResponse)}")
            elif ( isinstance(child, SequenceNode) ):
                childResponse = child.makeDescision(player)
                # self.logger.logInfo(message=f"SequenceNode returned {str(childResponse)}")
            elif ( isinstance(child, SelectorNode) ):
                # child.setTick(False)
                # self.logger.logError(message="SelectorNode cannot be a child of SelectorNode.")
                # childResponse = 'Error'
                childResponse = child.makeDescision(player)
                # self.logger.logInfo(message=f"SelectorNode returned {str(childResponse)}")
            
            if ( childResponse is None ):
                # self.logger.logWarning(message=f"Child returned None.")
                continue

            # self.logger.logInfo(message=f"Obtained Child Response : {str(childResponse)}")
            self.setTick(True)
            if (childResponse['result'] == 'Running' or childResponse['result'] == 'Success' or childResponse['result'] == 'Error'):
                self.setState(child.getState())
                self.setTick(False)
                if ( 'action' in childResponse.keys() ):
                    action = childResponse['action']
                return { 'result' : self.getState(), 'action' : action}
            
        # Code reaching here means that all the children returned Failure.
        # self.logger.logInfo(message="All children returned Failure.")
        self.setState('Failure')
        self.setTick(False)
        return { 'result' : self.getState(), 'action' : action}

    def getLabel(self) -> str:
        return f"{self._name}"


class SequenceNode(Node):  # '->'
    """
        SequenceNode class.

        Iterates over all the children 
        nodes and returns the first
        node that returns False.

        Returns False only if all the 
        nodes return True
    """

    def __init__(self, parent=None, siblingOrder: int = 0, children=None, ) -> None:
        super().__init__(parent, siblingOrder, children)
        self._name = 'SequenceNode'

    def makeDescision(self, player) -> dict:
        action = 'E'

        for child in self.children:
            child.setTick(True)
            self.setTick(False)

            childResponse = None

            if ( isinstance(child, ConditionNode) ):
                childResponse = child.checkCondition(player)
                # self.logger.logInfo(message=f"ConditionNode returned {str(childResponse)}")
            elif ( isinstance(child, ActionNode) ):
                childResponse = child.performAction(player)
                # self.logger.logInfo(message=f"ActionNode returned {str(childResponse)}")
            elif ( isinstance(child, SequenceNode) ):
                childResponse = child.makeDescision(player)
                # self.logger.logInfo(message=f"SequenceNode returned {str(childResponse)}")
            elif ( isinstance(child, SelectorNode) ):
                # child.setTick(False)
                # self.logger.logError(message="SequenceNode cannot be a child of SequenceNode.")
                # childResponse = 'Error'
                childResponse = child.makeDescision(player)
                # self.logger.logInfo(message=f"SelectorNode returned {str(childResponse)}")

            if ( childResponse is None ):
                # self.logger.logWarning(message=f"Child returned None.")
                continue
            
            # self.logger.logInfo(message=f"Obtained Child Response : {str(childResponse)}")
            self.setTick(True)

            if ( 'action' in childResponse.keys() ):
                if ( childResponse['action'] != 'E' ):
                    return { 'result' : 'Success', 'action' : childResponse['action']}
                else :
                    return { 'result' : 'Failure', 'action' : 'E'}
            if (childResponse['result'] == 'Running' or childResponse['result'] == 'Failure' or childResponse['result'] == 'Error'):
                self.setState(child.getState())
                self.setTick(False)
                return { 'result' : self.getState(), 'action' : 'E'}
            
        # Code reaching here means that all the children returned Success.
        # self.logger.logInfo(message="All children returned Success.")
        self.setState('Success')
        self.setTick(False)
        return { 'result' : self.getState(), 'action' : action}

    def getLabel(self) -> str:
        return f"{self._name}"
