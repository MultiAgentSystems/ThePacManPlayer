'''
    Implement all the actions proposed in the paper.
    1. moveToEatAnyPill
    2. moveToEatNormalPill
    3. moveToEatPowerPill
    4. moveAwayFromGhost
    5. moveTowardsGhost
'''
from pythonPacMan.tile import tileID as Tile
from pythonPacMan.path_finder import path as PathFinder


def moveToEatPill( game, normalPill : bool , powerPill : bool ) -> str:
    pathStepForNearestPill = 'E'
    pathLengthForNearestPill = -1
    ## Now, we iterate over the coordinates, and 
    ## check if there is a pill at that coordinate.
    ## If there is, we add it to the possiblePillsToEat 
    ## list. We compute the path to every such possible 
    ## pill and then return the shortest one.

    for row in range(0, game.level.lvlHeight, 1):
        for col in range(0, game.level.lvlWidth, 1):
            code = game.level.GetMapTile((row, col))
            if ( normalPill and code == Tile['pellet'] ) or ( powerPill and code == Tile['pellet-power'] ):
                pathToPill = PathFinder.FindPath( (game.player.nearestRow, game.player.nearestCol), (row, col) )

                if ( pathToPill is None or pathToPill is False or pathToPill == "" ):
                    continue

                pathLength = len(pathToPill)
                firstStep = pathToPill[0]

                if ( pathLength < pathLengthForNearestPill or pathLengthForNearestPill == -1 ):
                    pathLengthForNearestPill = pathLength
                    pathStepForNearestPill = firstStep

    return pathStepForNearestPill

def moveToEatAnyPill( game ):
    return moveToEatPill( game, True, True )

def moveToEatNormalPill(game):
    return moveToEatPill( game, True, False )

def moveToEatPowerPill(game):
    return moveToEatPill( game, False, True )

def moveAwayFromGhost( game ):
    firstOppositeStep = moveTowardsGhost(game)
    invertedStep = {'L': 'R', 'R': 'L', 'U': 'D', 'D': 'U', 'E' : 'E'}
    return invertedStep[firstOppositeStep]

def moveTowardsGhost(game):
    dist = -1
    firstStep = 'E'

    for i in range (4):
        pathToGhost = PathFinder.FindPath((game.player.nearestRow, game.player.nearestCol), (game.ghosts[i].nearestRow, game.ghosts[i].nearestCol))

        if ( pathToGhost is None or pathToGhost is False or pathToGhost == "" ):
            continue
        if dist == -1 or dist > len(pathToGhost):
            dist = len(pathToGhost)
            firstStep = pathToGhost[0]
    
    return firstStep
