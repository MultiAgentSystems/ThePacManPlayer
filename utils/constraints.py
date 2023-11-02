'''
    Make functions that return a boolean
    corresponding to the constraints.
'''

from classes.nodes import SelectorNode

## StaticConstraints for BehaviourTree

def SequenceSelectorAlternate( tree ):
    Root = tree.getRoot()
    return ( isinstance(Root, SelectorNode) ) and Root.SequenceSelectorAlternate()

def OnlyChildNodeMeansNoConditonNode(tree):
    Root = tree.getRoot()
    return Root.OnlyChildNodeMeansNoConditonNode()

def ActionNodesFollowAllConditionNodes(tree):
    Root = tree.getRoot()
    return Root.ActionNodesFollowAllConditionNodes()

def ConditionActionNoChildren(tree):
    Root = tree.getRoot()
    return Root.ConditionActionNoChildren()

def SequenceSelectorMustHaveOneChild(tree):
    Root = tree.getRoot()
    return Root.SequenceSelectorMustHaveOneChild()

def StaticConstraints(tree):
    return SequenceSelectorAlternate(tree) and OnlyChildNodeMeansNoConditonNode(tree) and ActionNodesFollowAllConditionNodes(tree) and ConditionActionNoChildren(tree) and SequenceSelectorMustHaveOneChild(tree)


## DynamicConstraints for BehaviourTree
