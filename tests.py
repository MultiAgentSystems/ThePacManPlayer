from classes.nodes import *
from classes.tree import *

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

def testSequenceNode():
    global universalLogger
    sequenceNode = SequenceNode(logger=universalLogger)
    print(sequenceNode)

# testConditionNode()
# testActionNode()
# testSequenceNode()


def testTreeExectionOrder():
    global universalLogger
    
    sequenceNode = SequenceNode(logger=universalLogger)
    sequenceNode.addChild(SelectorNode(logger=universalLogger))
    
    for _ in range(3):
        sequenceNode.addChild(ConditionNode(conditionFunction=dummyCondition, description="Checks whether a > 2b + 1.", logger=universalLogger))
    
    for _ in range(2):
        sequenceNode.getChildren()[0].addChild(ActionNode(actionFunction=dummyAction, logger=universalLogger))
    
    thisTree = Tree(root=sequenceNode, logger=universalLogger)

    thisTree.updateExecutionOrder(backtrack=True)

    expected = ['SequenceNode', 'SelectorNode', 'ActionNode', 'SelectorNode', 'ActionNode', 'SelectorNode', 'SequenceNode', 'ConditionNode', 'SequenceNode', 'ConditionNode', 'SequenceNode', 'ConditionNode', 'SequenceNode']
    recieved = []
    for node in thisTree.getExecutionOrder():
        recieved.append(node._name)

    if ( expected == recieved ):
        print("Test Passed")
    else :
        print("Test For Execution Order Failed")


def testTreeAddNode():
    global universalLogger

    newSequenceNode = SequenceNode(logger=universalLogger)
    newSequenceNode.addChild(SelectorNode(logger=universalLogger))

    for _ in range(3):
        newSequenceNode.addChild(ConditionNode(conditionFunction=dummyCondition, description="Checks whether a > 2b + 1.", logger=universalLogger))

    for _ in range(2):
        newSequenceNode.getChildren()[0].addChild(ActionNode(actionFunction=dummyAction, logger=universalLogger))

    newTree = Tree(root=newSequenceNode, logger=universalLogger)
    
    newTree.addNode(node=ConditionNode(conditionFunction=dummyCondition, description="Checks whether a > 2b + 1.", logger=universalLogger), parentNode=newSequenceNode.getChildren()[0], elderBrother=newSequenceNode.getChildren()[0].getChildren()[0] )
    newTree.addNode(node=ConditionNode(conditionFunction=dummyCondition, description="Checks Something.", logger=universalLogger ), parentNode=newSequenceNode)

    newTree.updateExecutionOrder()
    
    expected = ['SequenceNode', 'ConditionNode', 'SelectorNode', 'ActionNode', 'ConditionNode', 'ActionNode', 'ConditionNode', 'ConditionNode', 'ConditionNode']
    recieved = []
    for node in newTree.getExecutionOrder():
        recieved.append(node._name)
    
    if ( expected == recieved ):
        print("Test Passed")
    else :
        print("Test For Add Node Failed")


testTreeExectionOrder()
testTreeAddNode()
