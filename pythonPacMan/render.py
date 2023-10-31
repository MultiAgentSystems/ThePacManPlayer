# pacman.pyw
# By David Reilly, Modified by Andy Sommerville

#modified by CS4701 Pac AI team for CS4701 project.


import pygame, sys, os, random
import pandas as pd
import numpy as np
from pygame.locals import *
import pacai as ga
from scipy.spatial import distance
import math

from path_finder import path
from pacman import pacman
from ghost import ghost
from tile import *
from level import level
from game import game

SCRIPT_PATH = sys.path[0]
# SCRIPT_PATH = "Pac-AI-master"
print(SCRIPT_PATH)

pygame.init()

clock = pygame.time.Clock()

window = pygame.display.set_mode((1, 1))
pygame.display.set_caption("Pacman")

screen = pygame.display.get_surface()

img_Background = pygame.image.load(os.path.join(SCRIPT_PATH, "images", "1.gif")).convert()

def CheckIfCloseButton(events):
    for event in events:
        if event.type == QUIT:
            sys.exit(0)


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
            actualRow = row
            actualCol = col

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
        window = pygame.display.set_mode(thisGame.screenSize, pygame.DOUBLEBUF | pygame.HWSURFACE)


#      __________________
# ___/  main code block  \_____________________________________________________

def runGame(BT, numRuns, display=False):
    player = pacman(display=display)
    ghosts = {}
    for i in range(0, 6, 1):
        ghosts[i] = ghost(i, display=display)
    thisGame = game()
    thisLevel = level(player, ghosts, thisGame, screen)
    player.set(thisGame, thisLevel, ghosts)
    for i in range(0, 6, 1):
        ghosts[i].set(thisGame, thisLevel, ghosts, player)
    thisGame.set(thisLevel, player, ghosts)
    thisLevel.LoadLevel(thisGame.GetLevelNum())
    thisGame.screenTileSize = (thisLevel.lvlHeight, thisLevel.lvlWidth)
    thisGame.screenSize = (thisGame.screenTileSize[1] * 16, thisGame.screenTileSize[0] * 16)
    if display :
        window = pygame.display.set_mode(thisGame.screenSize, pygame.DOUBLEBUF | pygame.HWSURFACE)


# create the pacman
player = pacman()

# create ghost objects
ghosts = {}
for i in range(0, 6, 1):
    # remember, ghost[4] is the blue, vulnerable ghost
    ghosts[i] = ghost(i)
    # print(ghosts.items())

# create game and level objects and load first level

population_size = ga.population_size
n_generations = ga.n_generations

thisGame = game(screen)
thisLevel = level(player, ghosts, thisGame, screen)
player.set(thisGame, thisLevel, ghosts)
for i in range(0, 6, 1):
    ghosts[i].set(thisGame, thisLevel, ghosts, player)
thisGame.set(thisLevel, player, ghosts)
thisLevel.LoadLevel(thisGame.GetLevelNum())
thisPopulation = -1
thisGeneration = 0
allFitness = np.zeros((n_generations, population_size))

thisGame.screenTileSize = (thisLevel.lvlHeight, thisLevel.lvlWidth)
thisGame.screenSize = (thisGame.screenTileSize[1] * 16, thisGame.screenTileSize[0] * 16)
# print (thisGame.screenSize)
window = pygame.display.set_mode(thisGame.screenSize, pygame.DOUBLEBUF | pygame.HWSURFACE)

rand = 0
while True: 
    events = pygame.event.get()

    CheckIfCloseButton(events)

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
            d_ghosts[i] = ghosts[i].direction
            # print(d_ghosts)
            ghostDistance[i] = 5
        ghostDirections = (ghostDirection[d_ghosts[0]], ghostDirection[d_ghosts[1]], ghostDirection[d_ghosts[2]],
                           ghostDirection[d_ghosts[3]])


        # input_ga = GAInput(ghostDistance, ghostDirections)

        # print(f"i am input {input_ga}")
        # print(f"current population {thisPopulation}")
        # rand = ga.neural_net(thisPopulation, input_ga)
        # print(f"i am rand: {rand}")
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    rand = 0
                if event.key == pygame.K_LEFT:
                    rand = 1
                if event.key == pygame.K_UP:
                    rand = 2
                if event.key == pygame.K_DOWN:
                    rand = 3

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
            GetCrossRef(thisLevel)
        elif not normalSet.count(thisGame.modeTimer) == 0:
            # member of normal set
            thisLevel.edgeLightColor = oldEdgeLightColor
            thisLevel.edgeShadowColor = oldEdgeShadowColor
            thisLevel.fillColor = oldFillColor
            GetCrossRef(thisLevel)
        elif thisGame.modeTimer == 150:
            thisGame.SetMode(8)

    elif thisGame.mode == 8:
        # blank screen before changing levels
        thisGame.modeTimer += 1
        if thisGame.modeTimer == 10:
            thisGame.SetNextLevel()
            window = pygame.display.set_mode(thisGame.screenSize, pygame.DOUBLEBUF | pygame.HWSURFACE)

    bgsize = img_Background.get_size()

    for i in range(0, thisGame.screenSize[0], bgsize[0]):
        for j in range(0, thisGame.screenSize[1], bgsize[1]):
            screen.blit(img_Background, (i, j))

    if not thisGame.mode == 8:
        thisLevel.DrawMap()

        for i in range(0, 4, 1):
            ghosts[i].Draw(screen)
        player.Draw(screen)

    if thisGame.mode == 5:
        thisGame.DrawNumber(thisGame.ghostValue / 2,
                            (player.x - 4, player.y + 6))

    thisGame.DrawScore()

    pygame.display.flip()

    clock.tick(60)
