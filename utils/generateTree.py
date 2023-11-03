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


def generateInitialTreeDepth2( treeSize : int = 5 ):
    '''
        Creates a tree with selector node as root node
        and its children as some number of condition nodes
        followed by some number of action nodes.
    '''

    root = SelectorNode()
    
    numberOfNodes = random.randint(2, treeSize - 1)
    children = generateNodes( limit = numberOfNodes, unwanted = [2,3] )

    for child in children:
        root.addChild( child )

    generatedTree = Tree( root )
    generatedTree.updateExecutionOrder()
    return generatedTree
    
def generateInitialTreeDepth3( treeSize : int = 7 ):
    '''
        Creates a tree with selector node as root node
        and its children as a random list of recursicve children.
    '''
    root = SelectorNode()
    
    remaining = treeSize

    numberOfSequenceNodes = random.randint(1, floor(2*treeSize/5) - 1)
    children = generateNodes( limit = numberOfSequenceNodes , specific = 3 )

    remaining -= numberOfSequenceNodes
    children += generateNodes( limit = treeSize - 2*numberOfSequenceNodes, unwanted = [2,3] )
    
    remaining -= treeSize - 2*numberOfSequenceNodes

    for child in children:
        if ( isinstance(child, SelectorNode) or isinstance(child, SequenceNode) and remaining > 0 ):
            numGrandChildren = 0
            if ( remaining > 1 ):
                numGrandChildren = random.randint(1, remaining) 
            else :
                numGrandChildren = 1
            
            grandChildren = []
            if ( numGrandChildren > 1 ):
                grandChildren += generateNodes( limit = numGrandChildren - 1 , unwanted = [2,3] )
            
            grandChildren += generateNodes( specific = 0 )

            for grandChild in grandChildren:
                child.addChild( grandChild )
            remaining -= numGrandChildren
        root.addChild( child )

    generatedTree = Tree( root )
    generatedTree.updateExecutionOrder()
    return generatedTree

def generateInitialTrees( numTrees : int = 2, depth2SizeLimit : int = 5, depth3SizeLimit : int = 7 ) -> list :
    trees = []
    for _ in range( numTrees ):
        toss = random.randint(0, 1)
        if toss == 0:
            trees.append( generateInitialTreeDepth2(depth2SizeLimit) )
        else:
            trees.append( generateInitialTreeDepth3(depth3SizeLimit) )

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
