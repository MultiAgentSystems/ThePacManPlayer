from nodes import *
import copy

class Tree:
    def __init__(self, root = None ) -> None:
        self.root = root
        self.size = 0
        self.logger = Logger()

    def setRoot(self, root : Node) -> None:
        if ( root is None ):
            self.logger.logWarning(message=f"Root is None")
        self.root = root
        self.logger.logInfo(f"Set root node as {str(self.root)}")
    
    def getRoot(self) :
        return self.root

    def getSize(self) :
        return self.size

    def getOperationOrder(self):
        pass

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
                parentNode.addChild(node)
                node.setParent(parentNode)

                self.logger.logInfo(f"Added the node {node._name} to the parent {parentNode._name} at the start.")
                for i in range ( 0, len(parentNode.getChildren()) ):
                    parentNode.getChildren()[i].setSiblingOrder(i)

            else :
                # Add the new node after the elderBrother.
                parentNode.addChild(child = node, position = elderBrother.getSiblingOrder() + 1)
                node.setParent(parentNode)

                self.logger.logInfo(f"Added the node {node._name} to the parent {parentNode._name} at position {node.getSiblingOrder()}.")
                for i in range ( elderBrother.setSiblingOrder() + 1, len(parentNode.getChildren()) ):
                    parentNode.getChildren()[i].setSiblingOrder(i)
            
            self.size += 1
        except Exception :
            self.logger.logException(message="Could not add node.")
            print(Exception)

    def getSubTree(self, node : Node, copying = True):
        # Return a subtree using the current node as 
        # the root.
        if ( copying is False):
            return Tree(root=node)
        else :
            return Tree(root=copy.deepcopy(node))

class BehaviourTree(Tree):
    def __init__(self, root = None ) -> None:
        super().__init__(root)
    
