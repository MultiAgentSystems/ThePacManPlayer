'''
    This module contains code to generate a random tree,
    with some possibly defined constraints.
'''
import random
from classes.nodes import ActionNode, ConditionNode, SelectorNode, SequenceNode
from .actions import ActionFunctions
from .conditions import ConditionFunctions

def generateNodes( limit : int = 1, specific : int = -1 ) -> list:
    nodes = []
    
    for _ in range( limit ):
        '''
            0 : ActionNode
            1 : ConditionNode
            2 : SelectorNode
            3 : SequenceNode
        '''
        choosenNode = random.randint(0,3)
        
        if specific != -1 :
            choosenNode = specific
        
        if choosenNode == 0: # Need to allocate a randomActionFunction.
            nodes.append( ActionNode( ActionFunctions[random.randint(0, len(ActionFunctions) - 1)] ) )
        elif choosenNode == 1: # Need to allocate a randomConditionFunction.
            nodes.append( ConditionNode( ConditionFunctions[random.randint(0, len(ConditionFunctions) - 1)] ) )
        elif choosenNode == 2: # Need to allocate a randomSelectorFunction.
            nodes.append( SelectorNode() )
        elif choosenNode == 3: # Need to allocate a randomSequenceFunction.
            nodes.append( SequenceNode() )

    return nodes


def generateTree( treeSize : int = 10, childrenLimit : int = 3 ):
    #Generate a SelectorNode as the root.
    root = SelectorNode()
    
    possibleParents = [root]

    while ( len(possibleParents) > 0 ):
        numChildren = random.randint(1, childrenLimit)
        children = generateNodes( childrenLimit )
        root.addChild( children )
        treeSize -= 1
