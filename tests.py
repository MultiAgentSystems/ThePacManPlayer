import os

from math import floor

from classes.nodes import *
from classes.tree import *
from classes.generation import *

from pythonPacMan.runGame import runGame

from utils.generateTree import generateInitialTrees
from utils.actions import *
from utils.conditions import *
from utils.constraints import StaticConstraints

import matplotlib.pyplot as plot
import pickle

import time

SESSION_ID = str(time.time()).split(".")[0]

def saveTree( behaviourTree, filename, directory ):
    #Use pickle to save the tree.
    filename = "./agentEvolution/" + directory + "/" + filename
    filename += "_" + str( SESSION_ID )
    filename += ".pickle"

    with open( filename, 'wb' ) as f:
        pickle.dump( behaviourTree, f , pickle.HIGHEST_PROTOCOL )

def loadTree( filename, directory ):
    filename = "./agentEvolution/" + directory + "/" + filename
    filename += "_" + str( SESSION_ID )
    filename += ".pickle"

    with open( filename, 'rb' ) as f:
        return pickle.load( f )


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
    nextGeneration = thisGeneration.getNextGeneration()
    
    return nextGeneration


def testFirstGeneration(DC=False, SC=True):
    firstGeneration = generateInitialTrees(numTrees=10, depth2SizeLimit=8, depth3SizeLimit=15, SC=SC)
    
    for tree in firstGeneration:
        if not tree.isTreeFit(): 
            print( "Unfit Tree Generated" )
        if not StaticConstraints(tree) and SC:
            print( "Unsatisfying Tree Generated" )
    
    bestTree = firstGeneration[0]
    firstGeneration = Generation(firstGeneration, DC=DC, SC=SC)
    thisGeneration = firstGeneration
    
    generationScore = []
    generationBestScore = []
    treeScores = thisGeneration.tree_scores
    treeScores.sort(reverse=True)
    top10 = treeScores[:10]

    generationTop10AverageScore = [ ]
    
    directory = "StaticConstraints"
    
    numGenerations = 3

    savedTrees = []

    print(f"Fitness Score For Generation 0 : {thisGeneration.averageTreeScore}")
    for i in range(3):
        # Save the important stuff.
        generationScore.append(thisGeneration.averageTreeScore)
        generationBestScore.append(max(thisGeneration.tree_scores))
        treeScores = thisGeneration.tree_scores
        treeScores.sort(reverse=True)
        top10 = treeScores[:10]
        generationTop10AverageScore.append(sum(top10)/10)

        # Log the important stuff
        print("-*"*20)
        print(f"Fitness Scores For Generation {i+1} : \nAverage Score : {generationScore[-1]} \nBest Score : {generationBestScore[-1]}")
        
        # Save the best tree from this generation as a pickle file.
        bestTree = thisGeneration.getTopTrees(1)[0]
        saveTree(bestTree, filename=f"Gen{i+1}_{int(generationBestScore[-1])}", directory=directory)
        savedTrees.append(f"Gen{i+1}_{int(generationBestScore[-1])}")
        nextGeneration = thisGeneration.getNextGeneration()
        thisGeneration = nextGeneration

    plot.plot( list(range(len(generationScore))), generationScore, color='blue', label = "Average Fiteness Score", marker='o' )
    plot.plot( list(range(len(generationBestScore))), generationBestScore, color='lightgreen', label = "Best Fitness Score", marker='o' )
    plot.plot( list(range(len(generationTop10AverageScore))), generationTop10AverageScore, color='orange', label = "Average Fitness Score For top 10 Trees", marker='o' )
    plot.legend()
    plot.xlabel("Generation")
    plot.ylabel("Fitness Scores")
    plot.show()
    plot.savefig(f"./graphs/sc/Performance.png", dpi=300)
    print("-*"*20)
    print("Generation Average :\n", generationScore)
    print("Generation Best :\n", generationBestScore)
    print("Generation Top 10 Average :\n", generationTop10AverageScore)
    
    seeTreeSimulation = int(input("Do you want to see the tree simulation? (0/1) : "))

    if ( seeTreeSimulation == 0 ):
        return 

    for i in (floor(0.05*numGenerations), floor(0.5*numGenerations), floor(0.75*numGenerations), floor(0.99*numGenerations)):
        getTreeFile = savedTrees[i]
        bestTree = loadTree(getTreeFile, directory=directory)
        runGame(bestTree, display=True)


if __name__ == "__main__":
    testFirstGeneration()
