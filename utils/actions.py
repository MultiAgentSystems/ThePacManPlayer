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
    
    code = game.level.GetMapTile( (game.player.nearestRow + stepMapRow[possibleStep], game.player.nearestCol + stepMapCol[possibleStep]) )
    
    if (code >= 100 and code <= 140 ):
        # Found an obstacle.
        for step in "RULD" :
            if ( step in firstOppositeStep + possibleStep ):
                continue

            code = game.level.GetMapTile((game.player.nearestRow + stepMapRow[step], game.player.nearestCol + stepMapCol[step]))
            if ( code >= 100 and code <= 140 ):
                continue
            else :
                return step

    return 'E'

def moveTowardsGhost(game):
    dist = -1
    firstStep = 'E'

    pathToGhost = PathFinder.FindPath((game.player.nearestRow, game.player.nearestCol), 
                                      (game.ghost[game.target].nearestRow, game.ghosts[game.target].nearestCol))

    if ( pathToGhost is None or pathToGhost is False or pathToGhost == "" ):
        return 'E'

    if dist == -1 or dist > len(pathToGhost):
        dist = len(pathToGhost)
        firstStep = pathToGhost[0]
    
    return firstStep
