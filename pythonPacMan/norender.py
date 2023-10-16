# pacman.pyw
# By David Reilly, Modified by Andy Sommerville

#modified by CS4701 Pac AI team for CS4701 project.


import sys, os, random
import pandas as pd
import numpy as np
import pacai as ga
from scipy.spatial import distance
import math

from path_finder import path
from pacman import pacman
from ghost import ghost
from tile import *

SCRIPT_PATH = sys.path[0]
# SCRIPT_PATH = "Pac-AI-master"
print(SCRIPT_PATH)

#      ___________________
# ___/  class definitions  \_______________________________________________

class game():

    def __init__(self):
        self.levelNum = 0
        self.score = 0
        # self.lives = 3 # ! IMPORTANT
        self.lives = 0

        # game "mode" variable
        # 1 = normal
        # 2 = hit ghost
        # 3 = game over
        # 4 = wait to start
        # 5 = wait after eating ghost
        # 6 = wait after finishing level
        self.mode = 0
        self.elapsedTime = 0  # New!
        self.modeTimer = 0
        self.ghostTimer = 0
        self.ghostValue = 0

        self.SetMode(3)

        # camera variables
        self.screenPixelPos = (0, 0)  # absolute x,y position of the screen from the upper-left corner of the level
        self.screenNearestTilePos = (0, 0)  # nearest-tile position of the screen from the UL corner
        self.screenPixelOffset = (0, 0)  # offset in pixels of the screen from its nearest-tile position

        self.screenTileSize = (23, 21)
        self.screenSize = (self.screenTileSize[1] * 16, self.screenTileSize[0] * 16)

    def StartNewGame(self):
        self.levelNum = 2
        self.score = 0
        # self.lives = 3 #important
        self.lives = 0
        self.elapsedTime = 0

        self.SetMode(4)
        thisLevel.LoadLevel(thisGame.GetLevelNum())
        self.screenTileSize = (thisLevel.lvlHeight, thisLevel.lvlWidth)
        self.screenSize = (self.screenTileSize[1] * 16, self.screenTileSize[0] * 16)

    def AddToScore(self, amount):

        extraLifeSet = [25000, 50000, 100000, 150000]

        for specialScore in extraLifeSet:
            if self.score < specialScore and self.score + amount >= specialScore:
                thisGame.lives += 1

        self.score += amount

    def GetScreenPos(self):
        return self.screenPixelPos

    def GetLevelNum(self):
        return self.levelNum

    def SetNextLevel(self):
        self.levelNum += 1

        self.SetMode(4)
        thisLevel.LoadLevel(thisGame.GetLevelNum())

        self.screenTileSize = (thisLevel.lvlHeight, thisLevel.lvlWidth)
        self.screenSize = (self.screenTileSize[1] * 16, self.screenTileSize[0] * 16)

        player.velX = 0
        player.velY = 0 

    def SetMode(self, newMode):
        self.mode = newMode
        self.modeTimer = 0
        # print " ***** GAME MODE IS NOW ***** " + str(newMode)

class level():

    def __init__(self):
        self.lvlWidth = 0
        self.lvlHeight = 0
        self.edgeLightColor = (255, 255, 0, 255)
        self.edgeShadowColor = (255, 150, 0, 255)
        self.fillColor = (0, 255, 255, 255)
        self.pelletColor = (255, 255, 255, 255)

        self.map = {}

        self.pellets = 0
        self.powerPelletBlinkTimer = 0

    def SetMapTile(self, row_col, newValue):
        row, col = row_col
        self.map[(row * self.lvlWidth) + col] = newValue

    def GetMapTile(self, row_col):
        row, col = row_col
        if row >= 0 and row < self.lvlHeight and col >= 0 and col < self.lvlWidth:
            return self.map[(row * self.lvlWidth) + col]
        else:
            return 0

    def IsWall(self, row_col):
        row, col = row_col
        if row > thisLevel.lvlHeight - 1 or row < 0:
            return True

        if col > thisLevel.lvlWidth - 1 or col < 0:
            return True

        # check the offending tile ID
        result = thisLevel.GetMapTile((row, col))

        # if the tile was a wall
        if result >= 100 and result <= 199:
            return True
        else:
            return False

    def CheckIfHitWall(self, possiblePlayerX_possiblePlayerY, row_col):
        row, col = row_col
        possiblePlayerX, possiblePlayerY = possiblePlayerX_possiblePlayerY
        numCollisions = 0

        # check each of the 9 surrounding tiles for a collision
        for iRow in range(row - 1, row + 2, 1):
            for iCol in range(col - 1, col + 2, 1):

                if (possiblePlayerX - (iCol * 16) < 16) and (possiblePlayerX - (iCol * 16) > -16) and (
                        possiblePlayerY - (iRow * 16) < 16) and (possiblePlayerY - (iRow * 16) > -16):

                    if self.IsWall((iRow, iCol)):
                        numCollisions += 1

        if numCollisions > 0:
            return True
        else:
            return False

    def CheckIfHit(self, playerX_playerY, x_y, cushion):
        x, y = x_y
        playerX, playerY = playerX_playerY
        if (playerX - x < cushion) and (playerX - x > -cushion) and (playerY - y < cushion) and (
                playerY - y > -cushion):
            return True
        else:
            return False

    def CheckIfHitSomething(self, playerX_playerY, row_col):
        playerX, playerY = playerX_playerY
        row, col = row_col
        for iRow in range(row - 1, row + 2, 1):
            for iCol in range(col - 1, col + 2, 1):

                if (playerX - (iCol * 16) < 16) and (playerX - (iCol * 16) > -16) and (playerY - (iRow * 16) < 16) and (
                        playerY - (iRow * 16) > -16):
                    # check the offending tile ID
                    result = thisLevel.GetMapTile((iRow, iCol))

                    if result == tileID['pellet']:
                        # got a pellet
                        thisLevel.SetMapTile((iRow, iCol), 0)
                        # snd_pellet[player.pelletSndNum].play()
                        # player.pelletSndNum = 1 - player.pelletSndNum

                        thisLevel.pellets -= 1

                        thisGame.AddToScore(10)

                        if thisLevel.pellets == 0:
                            # no more pellets left!
                            # WON THE LEVEL
                            thisGame.SetMode(6)


                    elif result == tileID['pellet-power']:
                        # got a power pellet
                        thisLevel.SetMapTile((iRow, iCol), 0)
                        # snd_powerpellet.play()

                        thisGame.AddToScore(100)
                        thisGame.ghostValue = 200

                        thisGame.ghostTimer = 360
                        for i in range(0, 4, 1):
                            if ghosts[i].state == 1:
                                ghosts[i].state = 2

                    elif result == tileID['door-h']:
                        # ran into a horizontal door
                        for i in range(0, thisLevel.lvlWidth, 1):
                            if not i == iCol:
                                if thisLevel.GetMapTile((iRow, i)) == tileID['door-h']:
                                    player.x = i * 16

                                    if player.velX > 0:
                                        player.x += 16
                                    else:
                                        player.x -= 16

                    elif result == tileID['door-v']:
                        # ran into a vertical door
                        for i in range(0, thisLevel.lvlHeight, 1):
                            if not i == iRow:
                                if thisLevel.GetMapTile((i, iCol)) == tileID['door-v']:
                                    player.y = i * 16

                                    if player.velY > 0:
                                        player.y += 16
                                    else:
                                        player.y -= 16

    def GetGhostBoxPos(self):

        for row in range(0, self.lvlHeight, 1):
            for col in range(0, self.lvlWidth, 1):
                if self.GetMapTile((row, col)) == tileID['ghost-door']:
                    return (row, col)

        return False

    def GetPathwayPairPos(self):

        doorArray = []

        for row in range(0, self.lvlHeight, 1):
            for col in range(0, self.lvlWidth, 1):
                if self.GetMapTile((row, col)) == tileID['door-h']:
                    # found a horizontal door
                    doorArray.append((row, col))
                elif self.GetMapTile((row, col)) == tileID['door-v']:
                    # found a vertical door
                    doorArray.append((row, col))

        if len(doorArray) == 0:
            return False

        chosenDoor = random.randint(0, len(doorArray) - 1)

        if self.GetMapTile(doorArray[chosenDoor]) == tileID['door-h']:
            # horizontal door was chosen
            # look for the opposite one
            for i in range(0, thisLevel.lvlWidth, 1):
                if not i == doorArray[chosenDoor][1]:
                    if thisLevel.GetMapTile((doorArray[chosenDoor][0], i)) == tileID['door-h']:
                        return doorArray[chosenDoor], (doorArray[chosenDoor][0], i)
        else:
            # vertical door was chosen
            # look for the opposite one
            for i in range(0, thisLevel.lvlHeight, 1):
                if not i == doorArray[chosenDoor][0]:
                    if thisLevel.GetMapTile((i, doorArray[chosenDoor][1])) == tileID['door-v']:
                        return doorArray[chosenDoor], (i, doorArray[chosenDoor][1])

        return False

    def PrintMap(self):

        for row in range(0, self.lvlHeight, 1):
            outputLine = ""
            for col in range(0, self.lvlWidth, 1):
                outputLine += str(self.GetMapTile((row, col))) + ", "

            # print outputLine

    def LoadLevel(self, levelNum):

        self.map = {}

        self.pellets = 0

        f = open(os.path.join(SCRIPT_PATH, "images", "levels", str(levelNum) + ".txt"), 'r')
        # ANDY -- edit this
        # fileOutput = f.read()
        # str_splitByLine = fileOutput.split('\n')
        lineNum = -1
        rowNum = 0
        useLine = False
        isReadingLevelData = False

        for line in f:

            lineNum += 1

            # print " ------- Level Line " + str(lineNum) + " -------- "
            while len(line) > 0 and (line[-1] == "\n" or line[-1] == "\r"): line = line[:-1]
            while len(line) > 0 and (line[0] == "\n" or line[0] == "\r"): line = line[1:]
            str_splitBySpace = line.split(' ')

            j = str_splitBySpace[0]

            if (j == "'" or j == ""):
                # comment / whitespace line
                # print " ignoring comment line.. "
                useLine = False
            elif j == "#":
                # special divider / attribute line
                useLine = False

                firstWord = str_splitBySpace[1]

                if firstWord == "lvlwidth":
                    self.lvlWidth = int(str_splitBySpace[2])
                    # print "Width is " + str( self.lvlWidth )

                elif firstWord == "lvlheight":
                    self.lvlHeight = int(str_splitBySpace[2])
                    # print "Height is " + str( self.lvlHeight )

                elif firstWord == "edgecolor":
                    # edge color keyword for backwards compatibility (single edge color) mazes
                    red = int(str_splitBySpace[2])
                    green = int(str_splitBySpace[3])
                    blue = int(str_splitBySpace[4])
                    self.edgeLightColor = (red, green, blue, 255)
                    self.edgeShadowColor = (red, green, blue, 255)

                elif firstWord == "edgelightcolor":
                    red = int(str_splitBySpace[2])
                    green = int(str_splitBySpace[3])
                    blue = int(str_splitBySpace[4])
                    self.edgeLightColor = (red, green, blue, 255)

                elif firstWord == "edgeshadowcolor":
                    red = int(str_splitBySpace[2])
                    green = int(str_splitBySpace[3])
                    blue = int(str_splitBySpace[4])
                    self.edgeShadowColor = (red, green, blue, 255)

                elif firstWord == "fillcolor":
                    red = int(str_splitBySpace[2])
                    green = int(str_splitBySpace[3])
                    blue = int(str_splitBySpace[4])
                    self.fillColor = (red, green, blue, 255)

                elif firstWord == "pelletcolor":
                    red = int(str_splitBySpace[2])
                    green = int(str_splitBySpace[3])
                    blue = int(str_splitBySpace[4])
                    self.pelletColor = (red, green, blue, 255)

                elif firstWord == "startleveldata":
                    isReadingLevelData = True
                    #  "Level data has begun"
                    rowNum = 0

                elif firstWord == "endleveldata":
                    isReadingLevelData = False
                    #  "Level data has ended"

            else:
                useLine = True

            # this is a map data line
            if useLine == True:

                if isReadingLevelData == True:

                    for k in range(0, self.lvlWidth, 1):
                        self.SetMapTile((rowNum, k), int(str_splitBySpace[k]))

                        thisID = int(str_splitBySpace[k])
                        if thisID == 4:
                            # starting position for pac-man

                            player.homeX = k * 16
                            player.homeY = rowNum * 16
                            self.SetMapTile((rowNum, k), 0)

                        elif thisID >= 10 and thisID <= 13:
                            # one of the ghosts

                            ghosts[thisID - 10].homeX = k * 16
                            ghosts[thisID - 10].homeY = rowNum * 16
                            self.SetMapTile((rowNum, k), 0)

                        elif thisID == 2:
                            # pellet

                            self.pellets += 1

                    rowNum += 1

        # reload all tiles and set appropriate colors
        GetCrossRef(thisLevel, display=False)

        # load map into the pathfinder object
        path.ResizeMap((self.lvlHeight, self.lvlWidth))

        for row in range(0, path.size[0], 1):
            for col in range(0, path.size[1], 1):
                if self.IsWall((row, col)):
                    path.SetType((row, col), 1)
                else:
                    path.SetType((row, col), 0)

        # do all the level-starting stuff
        self.Restart()

    def Restart(self):

        for i in range(0, 4, 1):
            # move ghosts back to home

            ghosts[i].x = ghosts[i].homeX
            ghosts[i].y = ghosts[i].homeY
            ghosts[i].velX = 0
            ghosts[i].velY = 0
            ghosts[i].state = 1
            ghosts[i].speed = 1
            ghosts[i].Move()

            # give each ghost a path to a random spot (containing a pellet)
            (randRow, randCol) = (0, 0)

            while not self.GetMapTile((randRow, randCol)) == tileID['pellet'] or (randRow, randCol) == (0, 0):
                randRow = random.randint(1, self.lvlHeight - 2)
                randCol = random.randint(1, self.lvlWidth - 2)

            ghosts[i].currentPath = path.FindPath((ghosts[i].nearestRow, ghosts[i].nearestCol), (randRow, randCol))
            ghosts[i].FollowNextPathWay()

        player.x = player.homeX
        player.y = player.homeY
        player.velX = 0
        player.velY = 0

def GetWallInput():
    walls = [thisLevel.CheckIfHitWall((player.x + player.speed, player.y), (player.nearestRow, player.nearestCol)),
             thisLevel.CheckIfHitWall((player.x - player.speed, player.y), (player.nearestRow, player.nearestCol)),
             thisLevel.CheckIfHitWall((player.x, player.y - player.speed), (player.nearestRow, player.nearestCol)),
             thisLevel.CheckIfHitWall((player.x, player.y + player.speed), (player.nearestRow, player.nearestCol))]
    # map it to become int
    # walls = map(int, walls)
    # multiplying by 1 makes it an int array
    return walls


def GetClosestPellets():
    allDots = []
    allEnergizers = []
    for row in range(-1, thisGame.screenTileSize[0] + 1, 1):
        for col in range(-1, thisGame.screenTileSize[1] + 1, 1):
            actualRow = thisGame.screenNearestTilePos[0] + row
            actualCol = thisGame.screenNearestTilePos[1] + col

            useTile = thisLevel.GetMapTile((actualRow, actualCol))
            if not useTile == 0 and not useTile == tileID['door-h'] and not useTile == tileID['door-v']:
                if useTile == tileID['pellet']:
                    allDots.append((actualRow, actualCol))
                elif useTile == tileID['pellet-power']:
                    allEnergizers.append((actualRow, actualCol))

    curLocation = (player.x, player.y)

    allDots.sort(key=lambda p: distance.euclidean(curLocation, p))
    allEnergizers.sort(key=lambda p: distance.euclidean(curLocation, p))

    distanceClosestDot = distance.euclidean(curLocation, allDots[0])
    distanceClosestEnergizer = distance.euclidean(curLocation, allEnergizers[0])

    return list([distanceClosestDot]) + list([distanceClosestEnergizer])


def GetGhostModes():
    # 0=normal, 1=vunerable or spectacle
    modes = []
    for i in range(0, 4, 1):
        modes.append(ghosts[i].state != 1)
    return 1 * modes


# New!
def GAInput(ghostDistance, ghostDirection):
    # ** New Inputs: [ WALL_R WALL_L WALL_U WALL_D | GDIST_1 GDIST_2 GDIST_3 GDIST_4 | GMODE_1 GMODE_2 GMODE_3 GMODE_4 | CLOSESTFOOD_EDIST | CLOSESTENG_EDIST ] = size is 26
    walls = GetWallInput()
    closestDotEnergizerDistance = GetClosestPellets()
    # ghostModes = GetGhostModes()
    ghostDirectionList = [item for t in ghostDirection for item in t]
    # print(f"walls {walls}")
    # print(f"ghostDistance {ghostDistance}")
    # print(f"ghostDirection {ghostDirectionList}")
    # print(f"closestDotEnergizerDistance {closestDotEnergizerDistance}")
    ghostDistance = [float(i) / 30 for i in ghostDistance]
    closestDotEnergizerDistance = [float(i) / 300 for i in closestDotEnergizerDistance]

    inputValues = walls + ghostDistance + ghostDirectionList + closestDotEnergizerDistance
    inputArray = np.asarray(inputValues)

    # print(input)
    # print(inputArray)

    # Run genetic algorithm to determine output

    return inputArray


# New!
def CheckInputs(direction, mode_game):
    '''
    Sets new velocities for player.move() to act upon
    If it's end game - we want to return the score and time and generate a fitness value then run on a new set of weights.
    '''
    # r l u d
    result = [None] * 4
    if direction == 0:
        result[0] = 1
    if direction == 1:
        result[1] = 1
    if direction == 2:
        result[2] = 1
    if direction == 3:
        result[3] = 1

    if mode_game == 1:
        if result[0]:
            if not thisLevel.CheckIfHitWall((player.x + player.speed, player.y),
                                            (player.nearestRow, player.nearestCol)):
                player.velX = player.speed
                player.velY = 0

        elif result[1]:
            if not thisLevel.CheckIfHitWall((player.x - player.speed, player.y),
                                            (player.nearestRow, player.nearestCol)):
                player.velX = -player.speed
                player.velY = 0

        elif result[3]:
            if not thisLevel.CheckIfHitWall((player.x, player.y + player.speed),
                                            (player.nearestRow, player.nearestCol)):
                player.velX = 0
                player.velY = player.speed

        elif result[2]:
            if not thisLevel.CheckIfHitWall((player.x, player.y - player.speed),
                                            (player.nearestRow, player.nearestCol)):
                player.velX = 0
                player.velY = -player.speed

    # if pygame.key.get_pressed()[pygame.K_ESCAPE]:
    #     sys.exit(0)

    # New!
    if mode_game == 3:
        global thisGeneration
        global thisPopulation
        global allFitness

        if (thisGeneration == n_generations):
            print("Max Generations reached")
            np.savetxt("fitness_Scores.csv", allFitness, delimiter=",")
            sys.exit(0)


        print(f"GAME END! my score is {thisGame.score}, and my elapsed time is {thisGame.elapsedTime}")
        fitness = ga.cal_pop_fitness(thisGame.score, (thisGame.elapsedTime + 1.0e-21) / 1000)
        print(f"MY GENERATION {thisGeneration} and MY POP {thisPopulation}")
        allFitness[thisGeneration][thisPopulation] = fitness
        thisPopulation = thisPopulation + 1
        print(f"FITNESS ARRAY AT MY GENERATION IS {allFitness[thisGeneration]}")

        # finished entire population data/weights - now we have to cross/mutate based on fitness scores!


        if (thisPopulation >= population_size):
            curGenFitnessArr = allFitness[thisGeneration - 1]
            # indxBest = np.argmax(curGenFitnessArr)
            newParents = curGenFitnessArr.argsort()[-3:][::-1]
            ga.crossover(newParents[0], newParents[1])
            thisPopulation = 0
            thisGeneration = thisGeneration + 1
        thisGame.StartNewGame()

#      __________________
# ___/  main code block  \_____________________________________________________

# create the pacman
player = pacman(display=False)

# create ghost objects
ghosts = {}
for i in range(0, 6, 1):
    # remember, ghost[4] is the blue, vulnerable ghost
    ghosts[i] = ghost(i, display=False)
    # print(ghosts.items())

# create game and level objects and load first level

population_size = ga.population_size
n_generations = ga.n_generations

thisGame = game()
thisLevel = level()
player.set(thisGame, thisLevel, ghosts)
for i in range(0, 6, 1):
    ghosts[i].set(thisGame, thisLevel, ghosts, player)
thisLevel.LoadLevel(thisGame.GetLevelNum())
thisPopulation = -1
thisGeneration = 0
allFitness = np.zeros((n_generations, population_size))

while True:

    if thisGame.mode == 1:
        # normal gameplay mode
        thisGame.modeTimer += 1
        thisGame.elapsedTime += 1
        # NEW
        ghostDirection = {"R": [1, 0, 0, 0], "L": [0, 1, 0, 0], "U": [0, 0, 1, 0], "D": [0, 0, 0, 1]}
        #### ghost distance and direction
        d_ghosts = [None] * 4
        # change distance variable name
        ghostDistance = [None] * 4
        # print(d_ghosts,distance)
        for i in range(0, 4, 1):
            ghosts[i].Move()
            d_ghosts[i] = ghosts[i].currentPath[-1]
            # print(d_ghosts)
            ghostDistance[i] = len(ghosts[i].currentPath)
        ghostDirections = (ghostDirection[d_ghosts[0]], ghostDirection[d_ghosts[1]], ghostDirection[d_ghosts[2]],
                           ghostDirection[d_ghosts[3]])


        input_ga = GAInput(ghostDistance, ghostDirections)

        # print(f"i am input {input_ga}")
        # print(f"current population {thisPopulation}")
        rand = ga.neural_net(thisPopulation, input_ga)
        # print(f"i am rand: {rand}")

        CheckInputs(rand, mode_game=1)

        player.Move()

    if thisGame.mode == 3:
        # game over
        CheckInputs(0, mode_game=3)

    # out of the loop

    if thisGame.mode == 2:
        # waiting after getting hit by a ghost
        thisGame.modeTimer += 1
        thisGame.elapsedTime += 1

        if thisGame.modeTimer == 90:
            thisLevel.Restart()

            thisGame.lives -= 1
            if thisGame.lives == -1:
                thisGame.SetMode(3)
            else:
                thisGame.SetMode(4)

    # elif thisGame.mode == 3:
    # game over
    #    CheckInputs(0)

    elif thisGame.mode == 4:
        # waiting to start
        thisGame.modeTimer += 1

        if thisGame.modeTimer == 90:
            thisGame.SetMode(1)
            player.velX = player.speed

    elif thisGame.mode == 5:
        # brief pause after munching a vulnerable ghost
        thisGame.modeTimer += 1

        if thisGame.modeTimer == 30:
            thisGame.SetMode(1)

    elif thisGame.mode == 6:
        # pause after eating all the pellets
        thisGame.modeTimer += 1

        if thisGame.modeTimer == 60:
            thisGame.SetMode(7)
            oldEdgeLightColor = thisLevel.edgeLightColor
            oldEdgeShadowColor = thisLevel.edgeShadowColor
            oldFillColor = thisLevel.fillColor

    elif thisGame.mode == 7:
        # flashing maze after finishing level
        thisGame.modeTimer += 1

        whiteSet = [10, 30, 50, 70]
        normalSet = [20, 40, 60, 80]

        if not whiteSet.count(thisGame.modeTimer) == 0:
            # member of white set
            thisLevel.edgeLightColor = (255, 255, 255, 255)
            thisLevel.edgeShadowColor = (255, 255, 255, 255)
            thisLevel.fillColor = (0, 0, 0, 255)
            GetCrossRef(thisLevel, display=False)
        elif not normalSet.count(thisGame.modeTimer) == 0:
            # member of normal set
            thisLevel.edgeLightColor = oldEdgeLightColor
            thisLevel.edgeShadowColor = oldEdgeShadowColor
            thisLevel.fillColor = oldFillColor
            GetCrossRef(thisLevel, display=False)
        elif thisGame.modeTimer == 150:
            thisGame.SetMode(8)

    elif thisGame.mode == 8:
        # blank screen before changing levels
        thisGame.modeTimer += 1
        if thisGame.modeTimer == 10:
            thisGame.SetNextLevel()
