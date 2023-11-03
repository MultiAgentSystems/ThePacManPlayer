import pygame, os, sys

from pygame.locals import *

from classes.play.parser import DecisionSimulator

from .pacman import pacman
from .ghost import ghost
from .tile import *
from .level import level
from .game import game
from .scriptPath import SCRIPT_PATH

print(SCRIPT_PATH)

def CheckIfCloseButton(events):
    for event in events:
        if event.type == QUIT:
            sys.exit(0)

# New!
def CheckInputs(direction, mode_game, thisLevel, player):
    '''
    Sets new velocities for player.move() to act upon
    If it's end game - we want to return the score and time and generate a fitness value then run on a new set of weights.
    '''
    # r l u d
    result = [0] * 4
    if direction == "R":
        result[0] = 1
    if direction == "L":
        result[1] = 1
    if direction == "U":
        result[2] = 1
    if direction == "D":
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

#      __________________
# ___/  main code block  \_____________________________________________________

def runGame(BT, numRuns=1, display=False):
    screen = None
    if display:
        pygame.init()

        clock = pygame.time.Clock()

        window = pygame.display.set_mode((1, 1), pygame.NOFRAME)
        pygame.display.set_caption("Pacman")

        screen = pygame.display.get_surface()

        img_Background = pygame.image.load(os.path.join(SCRIPT_PATH, "images", "1.gif")).convert()
    else:
        pygame.quit()
        screen = None

    score = 0
    for i in range(numRuns):
        player = pacman(display=display)
        ghosts = {}
        for i in range(0, 6, 1):
            ghosts[i] = ghost(i, display=display)
        thisGame = game(screen, display=display)
        thisLevel = level(player, ghosts, thisGame, screen, display=display)
        player.set(thisGame, thisLevel, ghosts)
        for i in range(0, 6, 1):
            ghosts[i].set(thisGame, thisLevel, ghosts, player)
        thisGame.set(thisLevel, player, ghosts)
        thisLevel.LoadLevel(thisGame.GetLevelNum())
        thisGame.screenTileSize = (thisLevel.lvlHeight, thisLevel.lvlWidth)
        thisGame.screenSize = (thisGame.screenTileSize[1] * 16, thisGame.screenTileSize[0] * 16)
        if display :
            window = pygame.display.set_mode(thisGame.screenSize, pygame.DOUBLEBUF | pygame.HWSURFACE)

        thisGame.StartNewGame()

        previousMove = 'R'
        move = 'L'

        k = 2

        while True:
            if display:
                events = pygame.event.get()

                CheckIfCloseButton(events)

            if thisGame.mode == 1:
                # normal gameplay mode
                thisGame.modeTimer += 1
                thisGame.elapsedTime += 1
            
                for i in range(0, 4, 1):
                    ghosts[i].Move()
                
                if ( player.x%16 == 0 and player.y%16 == 0 ):
                    move = DecisionSimulator(BT, thisGame)
                    move = move if move != 'E' else previousMove
                    previousMove = move

                CheckInputs(move, 1, thisLevel, player)

                player.Move()

            if thisGame.mode == 3:
                # game over
                score += thisGame.score
                break

            if thisGame.mode == 2:
                # waiting after getting hit by a ghost
                thisGame.modeTimer += 1
                thisGame.elapsedTime += 1

                if not display or thisGame.modeTimer == 90:
                    thisLevel.Restart()

                    thisGame.lives -= 1
                    if thisGame.lives == 0:
                        thisGame.SetMode(3)
                    else:
                        thisGame.SetMode(4)
            
            elif thisGame.mode == 4:
                # waiting to start
                thisGame.modeTimer += 1

                if not display or thisGame.modeTimer == 90:
                    thisGame.SetMode(1)
                    player.velX = player.speed

            elif thisGame.mode == 5:
                # brief pause after munching a vulnerable ghost
                thisGame.modeTimer += 1

                if not display or thisGame.modeTimer == 30:
                    thisGame.SetMode(1)
            
            elif thisGame.mode == 6:
                # pause after eating all the pellets
                thisGame.modeTimer += 1

                if not display or thisGame.modeTimer == 60:
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
                elif not display or thisGame.modeTimer == 150:
                    thisGame.SetMode(8)

            elif thisGame.mode == 8:
                # blank screen before changing levels
                thisGame.modeTimer += 1
                if not display or thisGame.modeTimer == 10:
                    thisGame.SetNextLevel()
                    if display:
                        window = pygame.display.set_mode(thisGame.screenSize, pygame.DOUBLEBUF | pygame.HWSURFACE)

            if display:
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
    
    print(score / numRuns)
    return score / numRuns
