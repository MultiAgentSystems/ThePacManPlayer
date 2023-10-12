from classes.nodes import *

universalLogger = Logger()

def dummyCondition( a : int, b : int) -> bool:
    print(a,b)
    if ( a > 2*b + 1):
        return True
    else :
        return False

def dummyAction( a : int, b : int) -> bool:
    print(a + b + a*b)
    return True

def testActionNode():
    global universalLogger
    actionNode = ActionNode(actionFunction=dummyAction, logger=universalLogger)
    actionNode.performAction(5,6)

def testConditionNode():
    global universalLogger
    conditionNode = ConditionNode(conditionFunction=dummyCondition, description="Checks whether a > 2b + 1.", logger=universalLogger)
    conditionNode.setTick(True)
    conditionNode.checkCondition(5,6)
    print(conditionNode.getTick())

testConditionNode()
testActionNode()
