'''
    Implementing the Node BaseClass. 
'''

class Node:
    '''
        Node class.
    '''
    def __init__(self, parent = None, siblingOrder : int = 0, children : list = [] ) -> None:
        if ( parent is None ):
            self.parent = None
            self.parent = None
        else:
            self.parent = parent
            self.siblingOrder = siblingOrder
        self.children = children

    def isRootNode(self) -> bool:
        return self.parent is None

    def isLeafNode(self) -> bool:
        return len(self.children) == 0
