'''
    This module contains code to generate a random tree,
    with some possibly defined constraints.
'''
from math import ceil, floor
import random
from classes.nodes import ActionNode, ConditionNode, SelectorNode, SequenceNode
from classes.tree import Tree
from .actions import ActionFunctions, ActionFunctionDescription
from .conditions import ConditionFunctions, ConditionFunctionDescription
from .constraints import StaticConstraints

def generateNodes( limit : int = 1, specific : int = -1, unwanted : list = [-1] ) -> list:
    nodes = []
    
    for _ in range( limit ):
        '''
            0 : ActionNode
            1 : ConditionNode
            2 : SelectorNode
            3 : SequenceNode
        '''
        choosenNode = unwanted
        
        possibleChoices = [ x for x in range(4) if x not in unwanted ]
        choosenNode = random.choice(possibleChoices)

        if specific != -1 :
            choosenNode = specific
        
        if choosenNode == 0: # Need to allocate a randomActionFunction.
            index = random.randint(0, len(ActionFunctions) - 1)
            nodes.append( ActionNode( actionFunction= ActionFunctions[index], description=ActionFunctionDescription[index] ) )
            choosenNode = 0 #Only action nodes can follow action nodes. 
        elif choosenNode == 1: # Need to allocate a randomConditionFunction.
            index = random.randint(0, len(ConditionFunctions) - 1)
            nodes.append( ConditionNode( conditionFunction= ConditionFunctions[index], description=ConditionFunctionDescription[index] ) )
        elif choosenNode == 2: # Need to allocate a randomSelectorFunction.
            nodes.append( SelectorNode() )
        elif choosenNode == 3: # Need to allocate a randomSequenceFunction.
            nodes.append( SequenceNode() )

    return nodes


def generateInitialTreeDepth2( treeSize : int = 5, SC : bool = False ):
    '''
        Creates a tree with selector node as root node
        and its children as some number of condition nodes
        followed by some number of action nodes.
    '''

    root = SelectorNode()
    
    numberOfNodes = random.randint(2, treeSize - 1)
    children = []
    if SC:
        if numberOfNodes == 1:
            children = generateNodes( limit = numberOfNodes, specific = 0 )
        else:
            numConditions = random.randint(1, numberOfNodes - 1)
            conditionChildren = generateNodes( limit = numConditions, unwanted = [2,3] )
            actionChildren = generateNodes( limit = numberOfNodes - numConditions, specific = 0 )
            children = conditionChildren + actionChildren
    else:
        children = generateNodes( limit = numberOfNodes, unwanted = [2,3] )

    for child in children:
        root.addChild( child )

    generatedTree = Tree( root )
    generatedTree.updateExecutionOrder()
    return generatedTree
    
def generateInitialTreeDepth3( treeSize : int = 7, SC : bool = False ):
    '''
        Creates a tree with selector node as root node
        and its children as a random list of recursicve children.
    '''
    root = SelectorNode()
    
    remaining = treeSize

    numberOfControllerNodes = random.randint(1, floor(2*treeSize/5) - 1)
    if SC:
        children = generateNodes( limit = numberOfControllerNodes , specific = 3 )
    else:
        children = generateNodes( limit = numberOfControllerNodes , unwanted = [0,1] )

    remaining -= numberOfControllerNodes
    if SC:
        numConditions = random.randint(1, treeSize - 2*numberOfControllerNodes - 1)
        children += generateNodes( limit = numConditions, specific=1 )
        children += generateNodes( limit = treeSize - 2*numberOfControllerNodes - numConditions, specific=0 )
    else:
        children += generateNodes( limit = treeSize - 2*numberOfControllerNodes, unwanted = [2,3] )
    
    remaining -= treeSize - 2*numberOfControllerNodes

    for child in children:
        if ( isinstance(child, SelectorNode) or isinstance(child, SequenceNode) and remaining > numberOfControllerNodes ):
            numGrandChildren = 0
            if ( remaining > numberOfControllerNodes + 1 ):
                numGrandChildren = random.randint(1, remaining - numberOfControllerNodes) 
            else :
                numGrandChildren = 1
            
            grandChildren = []
            if SC:
                if numGrandChildren == 1:
                    grandChildren = generateNodes( limit = numGrandChildren, specific=0 )
                else:
                    numConditions = random.randint(1, numGrandChildren - 1)
                    grandChildren += generateNodes( limit = numConditions, specific=1 )
                    grandChildren += generateNodes( limit = numGrandChildren - numConditions, specific=0 )
            else:
                # if ( numGrandChildren > 1 ):
                grandChildren += generateNodes( limit = numGrandChildren - 1 , unwanted = [2,3] )
                
                # grandChildren += generateNodes( specific = 0 )

            for grandChild in grandChildren:
                child.addChild( grandChild )
            remaining -= numGrandChildren
        elif ( isinstance(child, SelectorNode) or isinstance(child, SequenceNode) and remaining == numberOfControllerNodes ):
            if SC:
                child.addChild( generateNodes( specific = 0 )[0] )
            else:
                child.addChild( generateNodes( unwanted = [2,3] )[0] )
            remaining -= 1
        root.addChild( child )
        numberOfControllerNodes -= 1

    generatedTree = Tree( root )
    generatedTree.updateExecutionOrder()
    return generatedTree

def generateInitialTrees( numTrees : int = 2, depth2SizeLimit : int = 5, depth3SizeLimit : int = 7, SC : bool = False ) -> list :
    trees = []
    for _ in range( numTrees ):
        toss = random.randint(0, 1)
        if toss == 0:
            trees.append( generateInitialTreeDepth2(depth2SizeLimit, SC) )
        else:
            trees.append( generateInitialTreeDepth3(depth3SizeLimit, SC) )

    return trees

def firstGenerationWithStaticConstraints( numTrees : int = 2, depth2SizeLimit : int = 5, depth3SizeLimit : int = 7 ) -> list :
    trees = []
    for _ in range( numTrees ):
        toss = random.randint(0, 1)
        if toss == 0:
            newTree = generateInitialTreeDepth2(depth2SizeLimit)
            while ( not StaticConstraints(newTree) ):
                newTree = generateInitialTreeDepth2(depth2SizeLimit)

            trees.append( newTree )
        else:
            newTree = generateInitialTreeDepth3(depth3SizeLimit)
            while ( not StaticConstraints(newTree) ):
                newTree = generateInitialTreeDepth3(depth3SizeLimit)

            trees.append( newTree )

    return trees
