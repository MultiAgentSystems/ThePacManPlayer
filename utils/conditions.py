'''
    Implement all the conditions proposed in the paper.
    1. isInedibleGhostClose()
    2. isEdibleGhostClose()
    3. isTargetGhostEdibleTime()
    4. isGhostScore()
'''

from pythonPacMan.path_finder import path as Path

def isInedibleGhostClose(game, low, high):
    path = ""
    for i in range(0, 4, 1):
        if game.ghosts[i].state == 1:
            path = Path.FindPath(game.level, (game.player.nearestRow, game.player.nearestCol),
                                 (game.ghosts[i].nearestRow, game.ghosts[i].nearestCol))
            if len(path) >= low and len(path) <= high:
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
    path = ""
    for i in range(0, 4, 1):
        if game.ghosts[i].state == 2:
            path = Path.FindPath(game.level, (game.player.nearestRow, game.player.nearestCol),
                                 (game.ghosts[i].nearestRow, game.ghosts[i].nearestCol))
            if len(path) >= low and len(path) <= high:
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

def isTargetGhostEdibleTime(value, threshold):
    return value >= threshold    

def isTargetGhostEdibleTimeLow(game):
    return isTargetGhostEdibleTime(game.ghostTimer, 90)

def isTargetGhostEdibleTimeMedium(game):
    return isTargetGhostEdibleTime(game.ghostTimer, 180)

def isTargetGhostEdibleTimeHigh(game):
    return isTargetGhostEdibleTime(game.ghostTimer, 270)

#######################################

def isGhostScore(value, threshold):
    return value == threshold

def isGhostScoreHigh(game):
    return isGhostScore(game.ghostValue, 400)

def isGhostScoreVeryHigh(game):
    return isGhostScore(game.ghostValue, 800)

def isGhostScoreMax(game):
    return isGhostScore(game.ghostValue, 1600)
