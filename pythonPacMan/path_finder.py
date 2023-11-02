def notAnObstacle( code ) -> bool:
    return ( code < 100 or code > 140 )

class node():

    def __init__(self):
        self.g = -1  # movement cost to move from previous node to this one (usually +10)
        self.h = -1  # estimated movement cost to move from this node to the ending node (remaining horizontal and vertical steps * 10)
        self.f = -1  # total movement cost of this node (= g + h)
        # parent node - used to trace path back to the starting node at the end
        self.parent = (-1, -1)
        # node type - 0 for empty space, 1 for wall (optionally, 2 for starting node and 3 for end)
        self.type = -1

class path_finder():

    def __init__(self):
        # map is a 1-DIMENSIONAL array.
        # use the Unfold( (row, col) ) function to convert a 2D coordinate pair
        # into a 1D index to use with this array.
        self.map = {}
        self.size = (-1, -1)  # rows by columns

        self.pathChainRev = ""
        self.pathChain = ""

        # starting and ending nodes
        self.start = (-1, -1)
        self.end = (-1, -1)

        # current node (used by algorithm)
        self.current = (-1, -1)

        # open and closed lists of nodes to consider (used by algorithm)
        self.openList = []
        self.closedList = []

        # used in algorithm (adjacent neighbors path finder is allowed to consider)
        self.neighborSet = [(0, -1), (0, 1), (-1, 0), (1, 0)]

    def ResizeMap(self, numRows_Cols):
        numRows, numCols = numRows_Cols
        self.map = {}
        self.size = (numRows, numCols)

        # initialize path_finder map to a 2D array of empty nodes
        for row in range(0, self.size[0], 1):
            for col in range(0, self.size[1], 1):
                self.Set((row, col), node())
                self.SetType((row, col), 0)

    def CleanUpTemp(self):

        # this resets variables needed for a search (but preserves the same map / maze)

        self.pathChainRev = ""
        self.pathChain = ""
        self.current = (-1, -1)
        self.openList = []
        self.closedList = []
    
    def FindNearestGhost(self, game, state ):
        self.CleanUpTemp()
        # Given an entity, this function finds the shortest distance to 
        # the entity from the player. This is done using a BFS Algorithm.

        ghostsPositions = [(game.ghosts[i].nearestRow, game.ghosts[i].nearestCol) for i in range(4)]
        
        toVisit = []
        visited = []

        toVisit.append( (game.player.nearestRow, game.player.nearestCol) )
        targetGhost = -1
        # print(f"Pacman position : {game.player.nearestRow}, {game.player.nearestCol}")

        while ( len(toVisit) > 0 ):
            (row, col) = toVisit.pop(0)
            visited.append( (row, col) )
            
            code = game.thisLevel.GetMapTile((row, col))

            if ( (row, col) in ghostsPositions ): # Found the nearest ghost.
                targetGhost = ghostsPositions.index( (row, col) )
                if game.ghosts[targetGhost].state == state:
                    break;
                else:
                    targetGhost = -1
                    continue
            else : #Found a different point.
                for i in range(-1,2):
                    for j in range(-1,2):
                        if ( i == j or i == -j ):
                            continue
                        # if ( row + i < 0 or row + i >= game.thisLevel.lvlHeight or col + j < 0 or col + j >= game.thisLevel.lvlWidth ):
                        #     continue
                        nRow = (row + i) % game.thisLevel.lvlHeight
                        nCol = (col + j) % game.thisLevel.lvlWidth
                        code = game.thisLevel.GetMapTile( (nRow, nCol) )
                        if ( (nRow, nCol) not in visited and (nRow, nCol) not in toVisit and notAnObstacle(code)):
                            toVisit.append( (nRow, nCol) )

        return targetGhost
           

    def FindPath(self, startPos, endPos):

        self.CleanUpTemp()

        # (row, col) tuples
        self.start = startPos
        self.end = endPos

        # add start node to open list
        self.AddToOpenList(self.start)
        self.SetG(self.start, 0)
        self.SetH(self.start, 0)
        self.SetF(self.start, 0)

        doContinue = True
        
        thisLowestFNode = False

        while (doContinue == True):

            thisLowestFNode = self.GetLowestFNode()

            if not thisLowestFNode == self.end and not thisLowestFNode == False:
                self.current = thisLowestFNode
                self.RemoveFromOpenList(self.current)
                self.AddToClosedList(self.current)

                for offset in self.neighborSet:
                    thisNeighbor = [self.current[0] + offset[0], self.current[1] + offset[1]]
                    if thisNeighbor[0] < 0:
                        thisNeighbor[0] += self.size[0]
                    if thisNeighbor[1] < 0:
                        thisNeighbor[1] += self.size[1]
                    if thisNeighbor[0] > self.size[0] - 1:
                        thisNeighbor[0] -= self.size[0]
                    if thisNeighbor[1] > self.size[1] - 1:
                        thisNeighbor[1] -= self.size[1]
                    thisNeighbor = tuple(thisNeighbor)

                    if not thisNeighbor[0] < 0 and not thisNeighbor[1] < 0 and not thisNeighbor[0] > self.size[
                        0] - 1 and not thisNeighbor[1] > self.size[1] - 1 and not self.GetType(thisNeighbor) == 1:
                        cost = self.GetG(self.current) + 10

                        if self.IsInOpenList(thisNeighbor) and cost < self.GetG(thisNeighbor):
                            self.RemoveFromOpenList(thisNeighbor)

                        # if self.IsInClosedList( thisNeighbor ) and cost < self.GetG( thisNeighbor ):
                        #   self.RemoveFromClosedList( thisNeighbor )

                        if not self.IsInOpenList(thisNeighbor) and not self.IsInClosedList(thisNeighbor):
                            self.AddToOpenList(thisNeighbor)
                            self.SetG(thisNeighbor, cost)
                            self.CalcH(thisNeighbor)
                            self.CalcF(thisNeighbor)
                            self.SetParent(thisNeighbor, self.current)
            else:
                doContinue = False

        if thisLowestFNode == False:
            return False

        # reconstruct path
        self.current = self.end
        while not self.current == self.start:
            # build a string representation of the path using R, L, D, U
            if self.current[1] > self.GetParent(self.current)[1]:
                self.pathChainRev += 'R'
            elif self.current[1] < self.GetParent(self.current)[1]:
                self.pathChainRev += 'L'
            elif self.current[0] > self.GetParent(self.current)[0]:
                self.pathChainRev += 'D'
            elif self.current[0] < self.GetParent(self.current)[0]:
                self.pathChainRev += 'U'
            self.current = self.GetParent(self.current)
            self.SetType(self.current, 4)

        # because pathChainRev was constructed in reverse order, it needs to be reversed!
        for i in range(len(self.pathChainRev) - 1, -1, -1):
            self.pathChain += self.pathChainRev[i]

        # set start and ending positions for future reference
        self.SetType(self.start, 2)
        self.SetType(self.end, 3)

        return self.pathChain

    def Unfold(self, row_col):
        row, col = row_col
        # this function converts a 2D array coordinate pair (row, col)
        # to a 1D-array index, for the object's 1D map array.
        return (row * self.size[1]) + col

    def Set(self, row_col, newNode):
        # sets the value of a particular map cell (usually refers to a node object)
        self.map[self.Unfold(row_col)] = newNode

    def GetType(self, row_col):
        return self.map[self.Unfold(row_col)].type

    def SetType(self, row_col, newValue):
        self.map[self.Unfold(row_col)].type = newValue

    def GetF(self, row_col):
        return self.map[self.Unfold(row_col)].f

    def GetG(self, row_col):
        return self.map[self.Unfold(row_col)].g

    def GetH(self, row_col):
        return self.map[self.Unfold(row_col)].h

    def SetG(self, row_col, newValue):
        self.map[self.Unfold(row_col)].g = newValue

    def SetH(self, row_col, newValue):
        self.map[self.Unfold(row_col)].h = newValue

    def SetF(self, row_col, newValue):
        self.map[self.Unfold(row_col)].f = newValue

    def CalcH(self, row_col):
        row, col = row_col
        self.map[self.Unfold(row_col)].h = abs(row - self.end[0]) + abs(col - self.end[0])

    def CalcF(self, row_col):
        unfoldIndex = self.Unfold(row_col)
        self.map[unfoldIndex].f = self.map[unfoldIndex].g + self.map[unfoldIndex].h

    def AddToOpenList(self, row_col):
        self.openList.append(row_col)

    def RemoveFromOpenList(self, row_col):
        self.openList.remove(row_col)

    def IsInOpenList(self, row_col):
        if self.openList.count(row_col) > 0:
            return True
        else:
            return False

    def GetLowestFNode(self):
        lowestValue = 1000  # start arbitrarily high
        lowestPair = (-1, -1)

        for iOrderedPair in self.openList:
            if self.GetF(iOrderedPair) < lowestValue:
                lowestValue = self.GetF(iOrderedPair)
                lowestPair = iOrderedPair

        if not lowestPair == (-1, -1):
            return lowestPair
        else:
            return False

    def AddToClosedList(self, row_col):
        self.closedList.append(row_col)

    def IsInClosedList(self, row_col):
        if self.closedList.count(row_col) > 0:
            return True
        else:
            return False

    def SetParent(self, row_col, parentRow_Col):
        parentRow, parentCol = parentRow_Col
        row, col = row_col
        self.map[self.Unfold((row, col))].parent = (parentRow, parentCol)

    def GetParent(self, row_col):
        return self.map[self.Unfold(row_col)].parent
    
path = path_finder()
