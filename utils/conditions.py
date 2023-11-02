'''
    Implement all the conditions proposed in the paper.
    1. isInedibleGhostClose()
    2. isEdibleGhostClose()
    3. isTargetGhostEdibleTime()
4. isGhostScore()
'''

from pythonPacMan.path_finder import path as Path

def isInedibleGhostClose(game, low, high):
    # for i in range(0, 4, 1):
    #     if game.ghosts[i].state == 1:
    #         path = Path.FindPath((game.player.nearestRow, game.player.nearestCol),(game.ghosts[i].nearestRow, game.ghosts[i].nearestCol))
    #         if ( path is None or path is False or path == "" ):
    #             continue
            
    #         # print(f"Low : {low}, Path length : {len(path)}, High : {high}")
    #         if len(path) >= low and len(path) <= high:
    #             game.target = i
    #             # print(f"Target : {game.target}")
    #             # if ( low == 6 and high == 10 ):
    #                 # print("Reached Here")
    #             return True
    target = Path.FindNearestGhost(game, 1)
    if target == -1:
        return False
    path = Path.FindPath((game.player.nearestRow, game.player.nearestCol),(game.ghosts[target].nearestRow, game.ghosts[target].nearestCol))

    if ( path is None or path is False or path == "" ):
        return False

    if len(path) >= low and len(path) <= high:
        game.target = target
        return True
    return False

def isInedibleGhostCloseVeryLow(game):
    return isInedibleGhostClose(game, 0, 5)

def isInedibleGhostCloseLow(game):
    return isInedibleGhostClose(game, 6, 10)

def isInedibleGhostCloseMedium(game):
    return isEdibleGhostClose(game, 11, 15)

def isInedibleGhostCloseHigh(game):
    return isEdibleGhostClose(game, 16, 20)

def isInedibleGhostCloseVeryHigh(game):
    return isEdibleGhostClose(game, 21, 25)

def isInedibleGhostCloseLong(game):
    return isEdibleGhostClose(game, 26, 30)

#######################################

def isEdibleGhostClose(game, low, high):
    # for i in range(0, 4, 1):
    #     if game.ghosts[i].state == 2:
    #         path = Path.FindPath( (game.player.nearestRow, game.player.nearestCol), (game.ghosts[i].nearestRow, game.ghosts[i].nearestCol) )
    #         if ( path is None or path is False or path == "" ):
    #             continue
    #         if len(path) >= low and len(path) <= high:
    #             game.target = i
    #             return True
    # return False
    target = Path.FindNearestGhost(game, 2)
    if target == -1:
        return False
    path = Path.FindPath((game.player.nearestRow, game.player.nearestCol),(game.ghosts[target].nearestRow, game.ghosts[target].nearestCol))

    if ( path is None or path is False or path == "" ):
        return False

    if len(path) >= low and len(path) <= high:
        game.target = target
        return True
    return False

def isEdibleGhostCloseVeryLow(game):
    return isEdibleGhostClose(game, 0, 5)

def isEdibleGhostCloseLow(game):
    return isEdibleGhostClose(game, 6, 10)

def isEdibleGhostCloseMedium(game):
    return isEdibleGhostClose(game, 11, 15)

def isEdibleGhostCloseHigh(game):
    return isEdibleGhostClose(game, 16, 20)

def isEdibleGhostCloseVeryHigh(game):
    return isEdibleGhostClose(game, 21, 25)

def isEdibleGhostCloseLong(game):
    return isEdibleGhostClose(game, 26, 30)

#######################################

def isTargetGhostEdibleTime(game, threshold):
    return game.ghostTimer >= threshold if game.ghosts[game.target].state == 2 else False

def isTargetGhostEdibleTimeLow(game):
    return isTargetGhostEdibleTime(game, 90)

def isTargetGhostEdibleTimeMedium(game):
    return isTargetGhostEdibleTime(game, 180)

def isTargetGhostEdibleTimeHigh(game):
    return isTargetGhostEdibleTime(game, 270)

#######################################

def isGhostScore(value, threshold):
    return value == threshold

def isGhostScoreHigh(game):
    return isGhostScore(game.ghostValue, 400)

def isGhostScoreVeryHigh(game):
    return isGhostScore(game.ghostValue, 800)

def isGhostScoreMax(game):
    return isGhostScore(game.ghostValue, 1600)


ConditionFunctions = [
    isInedibleGhostCloseVeryLow,
    isInedibleGhostCloseLow,
    isInedibleGhostCloseMedium,
    isInedibleGhostCloseHigh,
    isInedibleGhostCloseVeryHigh,
    isInedibleGhostCloseLong,
    
    isEdibleGhostCloseVeryLow,
    isEdibleGhostCloseLow,
    isEdibleGhostCloseMedium,
    isEdibleGhostCloseHigh,
    isEdibleGhostCloseVeryHigh,
    isEdibleGhostCloseLong,

    isTargetGhostEdibleTimeLow,
    isTargetGhostEdibleTimeMedium,
    isTargetGhostEdibleTimeHigh,

    isGhostScoreHigh,
    isGhostScoreVeryHigh,
    isGhostScoreMax
]
