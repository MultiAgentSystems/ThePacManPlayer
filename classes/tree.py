from .nodes import *
import copy

class Tree:
    def __init__(self, root = None, logger = None ) -> None:
        if (root is None ):
            root = SelectorNode()    
        
        self.root = root
        self.size = 0
        
        self.executionOrder = []

        if ( logger is None ):
            logger = Logger()
        self.logger = logger

    def setRoot(self, root : Node) -> None:
        if ( root is None ):
            self.logger.logWarning(message=f"Root is None")
        self.root = root
        self.logger.logInfo(f"Set root node as {str(self.root)}")
    
    def getRoot(self) :
        return self.root

    def getSize(self) :
        return self.size

    def getExecutionOrder(self):
        if ( len(self.executionOrder) == 0 ):
            self.logger.logWarning(message=f"Execution Order is empty.")
        return self.executionOrder
    
    def updateExecutionOrder(self, backtrack : bool = False ):
        try :
            self.executionOrder = self.root.getExecutionOrder(backtrack=backtrack)
        except Exception :
            self.logger.logException(message="Could not update execution order.")


    def addNode(self, node : Node, parentNode : Node, elderBrother = None) -> None:
        try :
            if ( node is None ):
                self.logger.logError(message=f"Node is None")
            if ( parentNode is None ):
                self.logger.logError(message=f"Parent Node is None")
            
            if ( node is None or parentNode is None ):
                raise Exception

            # Now, we can safely add the node as a child to parentNode
            
            if ( elderBrother is None ):
                # Add the new node at the first position.
                parentNode.addChild(node, position=0)
                node.setParent(parentNode)

                self.logger.logInfo(f"Added the node {node._name} to the parent {parentNode._name} at the start.")
                for i in range ( 0, len(parentNode.getChildren()) ):
                    parentNode.getChildren()[i].setSiblingOrder(i)
            else :
                # Add the new node after the elderBrother.
                parentNode.addChild(child = node, position = elderBrother.getSiblingOrder() + 1)
                node.setParent(parentNode)

                self.logger.logInfo(f"Added the node {node._name} to the parent {parentNode._name} at position {node.getSiblingOrder()}.")
                for i in range ( elderBrother.getSiblingOrder() + 1, len(parentNode.getChildren()) ):
                    parentNode.getChildren()[i].setSiblingOrder(i)
            
            self.updateExecutionOrder()
            self.size += 1
        except Exception :
            self.logger.logException(message="Could not add node.")
            print(Exception)

    def getSubTree(self, node : Node, copying = True):
        # Return a subtree using the passed node as 
        # the root.
        try :
            if ( node is None ):
                self.logger.logError(message=f"Node is None")
                raise Exception
            elif ( node.isLeafNode() ):
                self.logger.logWarning(message=f"Subtree of a leaf node is just the node itself.")

            if ( copying is False):
                self.logger.logInfo(f"Creating a copy of the node {node._name}.")
                return Tree(root=copy.copy(node))
            else :
                self.logger.logInfo(f"Creating a deepcopy of the node {node._name}.")
                return Tree(root=copy.deepcopy(node))
        except Exception as E:
            self.logger.logException(message=str(E))

    # def __str__(self) :
        #Printing a tree in a nice way
        # treeAsString = f"Tree with root {self.root._name}"
        # return treeAsString

class BehaviourTree(Tree):
    def __init__(self, root = None ) -> None:
        super().__init__(root)
    
