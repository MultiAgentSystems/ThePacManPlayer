from .nodes import *
from .normalised_tree import *
import copy


class Tree:
    def __init__(self, root=None) -> None:
        if (root is None):
            root = SelectorNode()

        self.root = root
        self.size = 0

        self.executionOrder = []

        # if (logger is None):
        #     logger = Logger()
        # self.logger = logger

    def setRoot(self, root: Node, prune: bool = False) -> None:
        # if (root is None):
            # self.logger.logWarning(message=f"Root is None")
        self.root = root
        # self.logger.logInfo(f"Set root node as {str(self.root)}")
        if prune:
            self.executionOrder = self.root.getExecutionOrder()
            self.size = len(self.root.getExecutionOrder(backtrack=False))
            # self.logger.logInfo(f"Previous Tree Pruned.")

    def getRoot(self):
        return self.root

    def getSize(self):
        return self.size

    def getExecutionOrder(self, update = False):
        # if (len(self.executionOrder) == 0):
            # self.logger.logWarning(message=f"Execution Order is empty.")
        if update:
            self.updateExecutionOrder()
        return self.executionOrder

    def updateExecutionOrder(self, backtrack: bool = False):
        try:
            self.executionOrder = self.root.getExecutionOrder(backtrack=backtrack)
        except Exception:
            print(Exception)
            # self.logger.logException(message="Could not update execution order.")

    def addNode(self, node: Node, parentNode: Node, elderBrother=None) -> None:
        try:
            # if (node is None):
            #     self.logger.logError(message=f"Node is None")
            # if (parentNode is None):
            #     self.logger.logError(message=f"Parent Node is None")

            if (node is None or parentNode is None):
                raise Exception

            # Now, we can safely add the node as a child to parentNode
            if (elderBrother is None):
                # Add the new node at the first position.
                parentNode.addChild(node, position=0)
                node.setParent(parentNode)

                # self.logger.logInfo(f"Added the node {node._name} to the parent {parentNode._name} at the start.")
                for i in range(0, len(parentNode.getChildren())):
                    parentNode.getChildren()[i].setSiblingOrder(i)
            else:
                # Add the new node after the elderBrother.
                parentNode.addChild(child=node, position=elderBrother.getSiblingOrder() + 1)
                node.setParent(parentNode)

                # self.logger.logInfo(
                #     f"Added the node {node._name} to the parent {parentNode._name} at position {node.getSiblingOrder()}.")
                for i in range(elderBrother.getSiblingOrder() + 1, len(parentNode.getChildren())):
                    parentNode.getChildren()[i].setSiblingOrder(i)

            self.updateExecutionOrder()
            self.size += 1
        except Exception:
            # self.logger.logException(message="Could not add node.")
            print(Exception)

    def getSubTree(self, node: Node, copying=True):
        # Return a subtree using the passed node as 
        # the root.
        try:
            if (node is None):
                # self.logger.logError(message=f"Node is None")
                raise Exception
                # self.logger.logWarning(message=f"Subtree of a leaf node is just the node itself.")

            if (copying is False):
                # self.logger.logInfo(f"Creating a copy of the node {node._name}.")
                return Tree(root=copy.copy(node))
            else:
                # self.logger.logInfo(f"Creating a deepcopy of the node {node._name}.")
                return Tree(root=copy.deepcopy(node))
        except Exception:
            # self.logger.logException(message=str(E))
            raise Exception

    def getNormalisedTree(self):
        # Returns the normalised tree representation of the tree.
        parents, labels = [], []
        node_idx = 0

        def preorderTraversal(node, parent_idx):
            nonlocal node_idx
            parents.append(parent_idx)
            labels.append(node.getLabel())
            my_idx = node_idx
            node_idx += 1
            for child in node.getChildren():
                preorderTraversal(child, my_idx)

        preorderTraversal(self.root, -1)
        return NormalisedTree(parents, labels)
    
    def getCopyAfterReplacing( self, nodeToBeSwapped, nodeToBeSwappedWith ):
        # Returns a copy of the tree after swapping the passed nodes.
        if (nodeToBeSwapped is None or nodeToBeSwappedWith is None):
            # self.logger.logError(message=f"NodeToBeSwapped or NodeToBeSwappedWith is None.")
            print("Given string is None")
            return None
        
        # print(nodeToBeSwapped.getParent())

        Tree = copy.deepcopy(self)
        newNode = copy.deepcopy(nodeToBeSwappedWith);

        if ( not self.isTreeFit() ):
            print("Tree is not fit.")
            return None #### POTENTIALLY DANGEROUS, THIS SHOULD NOT HAPPEN
        elif ( not Tree.isTreeFit() ):
            print("Copied Tree is not fit.")
            return None #### POTENTIALLY DANGEROUS, THIS SHOULD NOT HAPPEN

        ## If the root is passed, just swap the root.
        if (nodeToBeSwapped == self.getRoot()):
            # Tree.logger.logWarning(message=f"Swapping the root node with {nodeToBeSwappedWith._name}.")
            newNode.setParent(None)
            newNode.setSiblingOrder(0)
            Tree.setRoot(newNode)
            Tree.updateExecutionOrder()
            return Tree
        
        ## Get the execution Order and find the node.
        executionOrderCopy = Tree.getExecutionOrder()
        executionOrder = self.getExecutionOrder()


        for nodeIndex, node in enumerate(executionOrder):
            if (node == nodeToBeSwapped):
                ## Change the parent.
                ## Change the node's order in parent.
                # print( executionOrderCopy[nodeIndex].getParent() )

                newNode.setParent(executionOrderCopy[nodeIndex].getParent())
                newNode.setSiblingOrder(executionOrderCopy[nodeIndex].getSiblingOrder())
                executionOrderCopy[nodeIndex].getParent().getChildren()[executionOrderCopy[nodeIndex].getSiblingOrder()] = newNode
        
        Tree.updateExecutionOrder()
        return Tree
                
    def performChangeMutation( self, nodeToBeSwapped, nodeToBeSwappedWith ):
        # Returns the same tree.
        
        assert(nodeToBeSwappedWith is not None and nodeToBeSwapped is not None)
        assert( self.isTreeFit() )

        ## If the root is passed, just swap the root.
        if (nodeToBeSwapped == self.getRoot()):
            self.setRoot(nodeToBeSwappedWith)
            self.updateExecutionOrder()
            return self
        
        ## Get the execution Order and find the node.
        executionOrder = self.getExecutionOrder()

        for nodeIndex, node in enumerate(executionOrder):
            if (node == nodeToBeSwapped):
                ## Change the parent.
                ## Change the node's order in parent.
                # print( executionOrderCopy[nodeIndex].getParent() )

                nodeToBeSwappedWith.setParent(executionOrder[nodeIndex].getParent())
                nodeToBeSwappedWith.setSiblingOrder(executionOrder[nodeIndex].getSiblingOrder())
                if nodeToBeSwappedWith._name == "SelectorNode" or nodeToBeSwappedWith._name == "SequenceNode":
                    nodeToBeSwappedWith.setChildren(executionOrder[nodeIndex].getChildren())
                executionOrder[nodeIndex].getParent().getChildren()[executionOrder[nodeIndex].getSiblingOrder()] = nodeToBeSwappedWith
        
        self.updateExecutionOrder()
        return self
    
    def performDeleteMutation(self, nodeToDelete ):
        # Returns the same tree, with the node passed deleted.
        assert(self.isTreeFit())
        assert(nodeToDelete is not None)

        executionOrder = self.getExecutionOrder()

        for node in executionOrder:
            if (node == nodeToDelete):
                updatedChildren = nodeToDelete.getParent().getChildren()
                updatedChildren.remove(nodeToDelete)
                nodeToDelete.getParent().setChildren(updatedChildren)
        
        self.updateExecutionOrder()
        return self
    
    def performAdditionMutation(self, nodeToAddto, newNode ):
        # Returns the same tree, with the node passed added.
        assert(self.isTreeFit())
        assert(nodeToAddto is not None)
        assert(newNode is not None)
        
        # If the node is Condition node or Action Node :
        # then we add the same node as its next brother and update the children of parent.
        if ( nodeToAddto._name == "ConditionNode" or nodeToAddto._name == "ActionNode" ):
            updatedChildren = nodeToAddto.getParent().getChildren()
            updatedChildren.insert(nodeToAddto.getSiblingOrder() + 1, newNode)

            newNode.setParent(nodeToAddto.getParent())

            newNode.getParent().setChildren(updatedChildren)

            self.updateExecutionOrder()
            return self
        else :
            # Add the newNode as the child of nodeToAddto.
            nodeToAddto.addChild(newNode)
            self.updateExecutionOrder()
            return self

        # If the node is Selector Node or Sequence Node:
    def __str__(self):
        # Printing a tree in a nice way
        treeAsString = f"Tree with root {self.getRoot()._name}"
        return treeAsString

    def isTreeFit(self):
        #Ensures that the tree is consistent.
        if ( self.getRoot() is None ):
            print("Root is None")
            return False

        if ( self.getRoot().getParent() is not None ):
            print("Root has a parent")
            return False

        executionOrder = self.getRoot().getExecutionOrder()

        for node in executionOrder:
            if ( node == self.getRoot() ):
                continue
            elif ( node.getParent() is None ):
                print(f"{node._name} has no parent")
                return False
            elif ( node.getParent().getChildren() is None or node.getParent().getChildren() == [] ):
                print(f"{node.getParent()._name} has no children")
                return False
            elif ( node not in node.getParent().getChildren() ):
                print(f"{node._name} is not a child of {node.getParent()._name}")
                return False

        return True

class BehaviourTree(Tree):
    def __init__(self, root=None) -> None:
        super().__init__(root)

    def checkForStaticConstraints(self) -> None:
        pass

    def checkForDynamicConstraints(self) -> None:
        pass

    def checkForHybridConstraints(self) -> None:
        pass
