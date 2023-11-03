from classes.nodes import *
from classes.tree import *
from classes.generation import *

from pythonPacMan.runGame import runGame

from utils.generateTree import generateInitialTrees
from utils.actions import *
from utils.conditions import *

import matplotlib.pyplot as plot

def dummyCondition(a: int, b: int) -> bool:
    print(a, b)
    if (a > 2 * b + 1):
        return True
    else:
        return False


def dummyAction(a: int, b: int) -> bool:
    print(a + b + a * b)
    return True


def testActionNode():
    actionNode = ActionNode(actionFunction=dummyAction, )
    actionNode.performAction(5, 6)


def testConditionNode():
    conditionNode = ConditionNode(conditionFunction=dummyCondition, description="Checks whether a > 2b + 1.",
                                  )
    conditionNode.setTick(True)
    conditionNode.checkCondition(5, 6)
    print(conditionNode.getTick())


def testSequenceNode():
    sequenceNode = SequenceNode()
    print(sequenceNode)

def testTreeExectionOrder():

    sequenceNode = SequenceNode()
    sequenceNode.addChild(SelectorNode())

    for _ in range(3):
        sequenceNode.addChild(ConditionNode(conditionFunction=dummyCondition, description="Checks whether a > 2b + 1.",
                                            ))

    for _ in range(2):
        sequenceNode.getChildren()[0].addChild(ActionNode(actionFunction=dummyAction, ))

    thisTree = Tree(root=sequenceNode, )

    thisTree.updateExecutionOrder(backtrack=True)

    expected = ['SequenceNode', 'SelectorNode', 'ActionNode', 'SelectorNode', 'ActionNode', 'SelectorNode',
                'SequenceNode', 'ConditionNode', 'SequenceNode', 'ConditionNode', 'SequenceNode', 'ConditionNode',
                'SequenceNode']
    recieved = []
    for node in thisTree.getExecutionOrder():
        recieved.append(node._name)

    if (expected == recieved):
        print("Test Passed")
        normalised = thisTree.getNormalisedTree()
        print("Parent array:", normalised.getParentArray())
        print("Label array:", normalised.getLabelArray())
    else:
        print("Test For Execution Order Failed")


def testTreeAddNode():

    newSequenceNode = SequenceNode()
    newSequenceNode.addChild(SelectorNode())

    for _ in range(3):
        newSequenceNode.addChild(
            ConditionNode(conditionFunction=dummyCondition, description="Checks whether a > 2b + 1.",
                          ))

    for _ in range(2):
        newSequenceNode.getChildren()[0].addChild(ActionNode(actionFunction=dummyAction, ))

    newTree = Tree(root=newSequenceNode, )

    newTree.addNode(node=ConditionNode(conditionFunction=dummyCondition, description="Checks whether a > 2b + 1.",
                                       ), parentNode=newSequenceNode.getChildren()[0],
                    elderBrother=newSequenceNode.getChildren()[0].getChildren()[0])
    newTree.addNode(
        node=ConditionNode(conditionFunction=dummyCondition, description="Checks Something.", ),
        parentNode=newSequenceNode)

    newTree.updateExecutionOrder()

    expected = ['SequenceNode', 'ConditionNode', 'SelectorNode', 'ActionNode', 'ConditionNode', 'ActionNode',
                'ConditionNode', 'ConditionNode', 'ConditionNode']
    recieved = []
    for node in newTree.getExecutionOrder():
        recieved.append(node._name)

    if (expected == recieved):
        print("Test Passed")
    else:
        print("Test For Add Node Failed")


# testTreeExectionOrder()
# testTreeAddNode()


def createSampleTree():

    newSelectorNode = SelectorNode()
    
    for _ in range(3):
        newSelectorNode.addChild(SequenceNode())

    newSelectorNode.addChild( ActionNode(actionFunction = moveToEatAnyPill, description="Move to eat any pill", ))

    newSelectorNode.getChildren()[0].addChild(ConditionNode(conditionFunction=isInedibleGhostCloseVeryLow, parent=newSelectorNode.getChildren()[0]))
    newSelectorNode.getChildren()[0].addChild(ActionNode(actionFunction=moveAwayFromGhost, parent=newSelectorNode.getChildren()[0])) 
    
    newSelectorNode.getChildren()[1].addChild(ConditionNode(conditionFunction=isInedibleGhostCloseVeryHigh, parent=newSelectorNode.getChildren()[1]))
    newSelectorNode.getChildren()[1].addChild(ActionNode(actionFunction=moveToEatPowerPill, parent=newSelectorNode.getChildren()[1]))

    newSelectorNode.getChildren()[2].addChild(ConditionNode(conditionFunction=isInedibleGhostCloseMedium, parent=newSelectorNode.getChildren()[2]))
    newSelectorNode.getChildren()[2].addChild(ActionNode(actionFunction=moveToEatPowerPill, parent=newSelectorNode.getChildren()[2]))


    newTree = Tree(root=newSelectorNode, )
    newTree.updateExecutionOrder()

    recieved = []
    for node in newTree.getExecutionOrder():
        recieved.append(node._name)

    print(recieved)
    
    return newTree

def somewhatSmartTree():
    global universalLogger

    newSelectorNode = SelectorNode()

    
    conditions = [isInedibleGhostCloseVeryLow, 
                isEdibleGhostCloseVeryLow, 
                isInedibleGhostCloseVeryHigh,
                isInedibleGhostCloseMedium ]
    
    actions = [moveAwayFromGhost,
               moveTowardsGhost,
               moveToEatPowerPill,
               moveToEatAnyPill]

    description = ["moveAwayFromGhost",
                "moveTowardsGhost",
                "moveToEatPowerPill",
                "moveToEatAnyPill"]



    for _ in range( len(conditions) ):
        newSelectorNode.addChild(SequenceNode(parent=newSelectorNode))
    for _ in range( 1 ):
        newSelectorNode.addChild( ActionNode(actionFunction = moveToEatAnyPill, description="moveToEatAnyPill", parent=newSelectorNode))
    
    for node,conditionFunction,actionFunction,actionDescription in zip(newSelectorNode.getChildren(),conditions, actions, description):
        node.addChild(ConditionNode(conditionFunction=conditionFunction,parent=node ))
        node.addChild(ActionNode(actionFunction=actionFunction,description=actionDescription, parent=node ))

    newTree = Tree(root=newSelectorNode, )

    newTree.updateExecutionOrder()
    
    return newTree

def somewhatDumbTree():
    global universalLogger

    newSelectorNode = SelectorNode()

    
    conditions = [isInedibleGhostCloseVeryLow, 
                isEdibleGhostCloseVeryLow]
    
    actions = [moveAwayFromGhost,
               moveTowardsGhost]

    description = ["moveAwayFromGhost",
                "moveTowardsGhost"]

    for _ in range( len(conditions) ):
        newSelectorNode.addChild(SequenceNode( parent=newSelectorNode))
    for _ in range( 1 ):
        newSelectorNode.addChild( ActionNode(actionFunction = moveToEatAnyPill, description="moveToEatAnyPill", parent=newSelectorNode ))
    
    for node,conditionFunction,actionFunction,actionDescription in zip(newSelectorNode.getChildren(),conditions, actions, description):
        node.addChild(ConditionNode(conditionFunction=conditionFunction,parent=node ))
        node.addChild(ActionNode(actionFunction=actionFunction,description=actionDescription,parent=node ))

    newTree = Tree(root=newSelectorNode, )

    newTree.updateExecutionOrder()
    
    return newTree


def anotherTree():
    global universalLogger

    newSelectorNode = SelectorNode()
    
    conditions = [isInedibleGhostCloseVeryLow]
    
    actions = [moveAwayFromGhost]

    description = ["moveAwayFromGhost"]

    for _ in range( len(conditions) ):
        newSelectorNode.addChild( SequenceNode(parent=newSelectorNode))
    for _ in range( 1 ):
        newSelectorNode.addChild( ActionNode(actionFunction = moveToEatAnyPill, description="moveToEatAnyPill", parent=newSelectorNode ))
    
    for node,conditionFunction,actionFunction,actionDescription in zip(newSelectorNode.getChildren(),conditions, actions, description):
        node.addChild(ConditionNode(conditionFunction=conditionFunction, parent = node))
        node.addChild(ActionNode(actionFunction=actionFunction,description=actionDescription, parent=node))

    newTree = Tree(root=newSelectorNode, )

    newTree.updateExecutionOrder()
    
    return newTree


def runTheGame():
    behaviourTree = createSampleTree()
    runGame(behaviourTree, display=True)

def runTheSmartGame():
    behaviourTree = somewhatSmartTree()
    runGame(behaviourTree, display=True)

def generationTest():
    trees = [] 
    trees.append(createSampleTree())
    trees.append(somewhatSmartTree())
    trees.append(somewhatDumbTree())
    trees.append(anotherTree())

    thisGeneration = Generation(trees)
    nexGeneration = thisGeneration.getNextGeneration()

def testFirstGeneration():
    firstGeneration = generateInitialTrees(numTrees=100, depth2SizeLimit=5, depth3SizeLimit=7)

    for tree in firstGeneration:
        if not tree.isTreeFit(): 
            print( "Unfit Tree Generated" )

    firstGeneration = Generation(firstGeneration)
    thisGeneration = firstGeneration
    
    generationScore = []

    print(f"Fitness Score For Generation 0 : {thisGeneration.averageTreeScore}")
    for i in range(10):
        nextGeneration = thisGeneration.getNextGeneration()
        thisGeneration = nextGeneration
        print(f"Fitness Score For Generation {i+1} : {thisGeneration.averageTreeScore}")
        generationScore.append(thisGeneration.averageTreeScore)
    
    ## Plotting the Fitness Score
    plot.plot( list(range(len(generationScore))), generationScore, color='lightgreen' )
    print(generationScore)
    plot.show()

if __name__ == "__main__":
    testFirstGeneration()
