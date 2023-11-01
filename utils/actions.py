'''
    Implement all the actions proposed in the paper.
    1. moveToEatAnyPill
    2. moveToEatNormalPill
    3. moveToEatPowerPill
    4. moveAwayFromGhost
    5. moveTowardsGhost
'''
import random
from pythonPacMan.tile import tileID as Tile
from pythonPacMan.path_finder import path as PathFinder


def isDesiredPill(normalPill : bool , powerPill : bool, code ) -> bool:
    return  ( normalPill and code == Tile['pellet'] ) or ( powerPill and code == Tile['pellet-power'] )

def notAnObstacle( code ) -> bool:
    return ( code < 100 or code > 140 ) 

def moveToEatPill( game, normalPill : bool , powerPill : bool ) -> str:
    pathStepForNearestPill = 'E'
    pathLengthForNearestPill = -1
    ## Now, we iterate over the coordinates, and 
    ## check if there is a pill at that coordinate.
    ## If there is, we add it to the possiblePillsToEat 
    ## list. We compute the path to every such possible 
    ## pill and then return the shortest one.


    ## -- This implementation is too slow but makes sure to go 
    ## -- to the closest pill.
    # for row in range(0, game.thisLevel.lvlHeight, 1):
    #     for col in range(0, game.thisLevel.lvlWidth, 1):
    #         code = game.thisLevel.GetMapTile((row, col))
    #         if ( normalPill and code == Tile['pellet'] ) or ( powerPill and code == Tile['pellet-power'] ):
    #             # pathToPill = PathFinder.FindPath( (game.player.nearestRow, game.player.nearestCol), (row, col) )
    #             #
    #             # if ( pathToPill is None or pathToPill is False or pathToPill == "" ):
    #             #     continue
    #             #
    #             pathLength = random.randint(0, 30)
    #             # firstStep = pathToPill[0]
    #
    #             pathToGhost = "RLUD"
    #             index = random.randint(0, len(pathToGhost) - 1)
    #             firstStep = pathToGhost[index]
    #
    #             if ( pathLength < pathLengthForNearestPill or pathLengthForNearestPill == -1 ):
    #                 pathLengthForNearestPill = pathLength
    #                 pathStepForNearestPill = firstStep
    
    # Implementing a BFS over the graph.
    toVisit = set()
    visited = set()

    toVisit.add( (game.player.nearestRow, game.player.nearestCol) )
    target = tuple()
    print(f"Pacman position : {game.player.nearestRow}, {game.player.nearestCol}")

    while ( len(toVisit) > 0 ):
        (row, col) = toVisit.pop()
        visited.add( (row, col) )
        
        code = game.thisLevel.GetMapTile((row, col))
        print(row,col)

        if ( isDesiredPill(normalPill, powerPill, code) ): # Found the nearest pill.
            target = (row, col)
            break;
        else : #Found a different point.
            for i in range(-1,2):
                for j in range(-1,2):
                    if ( row + i < 0 or row + i >= game.thisLevel.lvlHeight or col + j < 0 or col + j >= game.thisLevel.lvlWidth ):
                        continue
                    code = game.thisLevel.GetMapTile( (row + i, col + j) )
                    if ( (row + i, col + j) not in visited and (row + i, col + j) not in toVisit and notAnObstacle(code)):
                        toVisit.add( (row + i, col + j) )

    if ( target == tuple() ):
        return 'E'


    #Just find the path from the current node to the target.
    path = PathFinder.FindPath( (game.player.nearestRow, game.player.nearestCol), target )
    
    if ( path is None or path is False or path == "" ):
        return 'E'

    pathStepForNearestPill = path[0]

    return pathStepForNearestPill

def moveToEatAnyPill( game ):
    return moveToEatPill( game, True, True )

def moveToEatNormalPill( game ):
    return moveToEatPill( game, True, False )

def moveToEatPowerPill( game ):
    return moveToEatPill( game, False, True )

def moveAwayFromGhost( game ):
    firstOppositeStep = moveTowardsGhost(game)
    invertedStep = {'L': 'R', 'R': 'L', 'U': 'D', 'D': 'U', 'E' : 'E'}
    
    possibleStep = invertedStep[firstOppositeStep]
    
    if ( possibleStep == 'E' ):
        return 'E'

    stepMapRow = { 'R' : 0, 'L' : 0, 'U' : -1, 'D' : 1 }
    stepMapCol = { 'R' : 1, 'L' : -1, 'U' : 0, 'D' : 0 }
    
    code = 60
    
    code = game.thisLevel.GetMapTile( (game.player.nearestRow + stepMapRow[possibleStep], game.player.nearestCol + stepMapCol[possibleStep]) )
    
    if (code >= 100 and code <= 140 ):
        # Found an obstacle.
        for step in "RULD" :
            if ( step in firstOppositeStep + possibleStep ):
                continue

            code = game.thisLevel.GetMapTile((game.player.nearestRow + stepMapRow[step], game.player.nearestCol + stepMapCol[step]))
            if ( code >= 100 and code <= 140 ):
                continue
            else :
                return step

    return 'E'

def moveTowardsGhost(game):
    dist = -1
    firstStep = 'E'

    pathToGhost = PathFinder.FindPath((game.player.nearestRow, game.player.nearestCol), 
                                      (game.ghosts[game.target].nearestRow, game.ghosts[game.target].nearestCol))


    if ( pathToGhost is None or pathToGhost is False or pathToGhost == "" ):
        return 'E'

    if dist == -1 or dist > len(pathToGhost):
        dist = len(pathToGhost)
        firstStep = pathToGhost[0]
    
    # pathToGhost = "RLUD"
    # index = random.randint(0, len(pathToGhost) - 1)
    
    # firstStep = pathToGhost[index]

    return firstStep
