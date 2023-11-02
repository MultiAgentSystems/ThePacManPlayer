import os, random
from .path_finder import path
from .tile import *
from .scriptPath import SCRIPT_PATH

class level():

    def __init__(self, player, ghosts, thisGame, screen, display):
        self.player = player
        self.ghosts = ghosts
        self.game = thisGame
        self.screen = screen
        self.display = display
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
        if row > self.lvlHeight - 1 or row < 0:
            return True

        if col > self.lvlWidth - 1 or col < 0:
            return True

        # check the offending tile ID
        result = self.GetMapTile((row, col))

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
                    result = self.GetMapTile((iRow, iCol))

                    if result == tileID['pellet']:
                        # got a pellet
                        self.SetMapTile((iRow, iCol), 0)
                        # snd_pellet[player.pelletSndNum].play()
                        # player.pelletSndNum = 1 - player.pelletSndNum

                        self.pellets -= 1

                        self.game.AddToScore(10)

                        if self.pellets == 0:
                            # no more pellets left!
                            # WON THE LEVEL
                            self.game.SetMode(6)


                    elif result == tileID['pellet-power']:
                        # got a power pellet
                        self.SetMapTile((iRow, iCol), 0)
                        # snd_powerpellet.play()

                        self.game.AddToScore(100)
                        self.game.ghostValue = 200

                        self.game.ghostTimer = 360
                        for i in range(0, 4, 1):
                            if self.ghosts[i].state == 1:
                                self.ghosts[i].state = 2
                                self.ghosts[i].speed /= 2
                                self.ghosts[i].currentPath = ""

                    elif result == tileID['door-h']:
                        # ran into a horizontal door
                        for i in range(0, self.lvlWidth, 1):
                            if not i == iCol:
                                if self.GetMapTile((iRow, i)) == tileID['door-h']:
                                    self.player.x = i * 16

                                    if self.player.velX > 0:
                                        self.player.x += 16
                                    else:
                                        self.player.x -= 16

                    elif result == tileID['door-v']:
                        # ran into a vertical door
                        for i in range(0, self.lvlHeight, 1):
                            if not i == iRow:
                                if self.GetMapTile((i, iCol)) == tileID['door-v']:
                                    self.player.y = i * 16

                                    if self.player.velY > 0:
                                        self.player.y += 16
                                    else:
                                        self.player.y -= 16

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
            for i in range(0, self.lvlWidth, 1):
                if not i == doorArray[chosenDoor][1]:
                    if self.GetMapTile((doorArray[chosenDoor][0], i)) == tileID['door-h']:
                        return doorArray[chosenDoor], (doorArray[chosenDoor][0], i)
        else:
            # vertical door was chosen
            # look for the opposite one
            for i in range(0, self.lvlHeight, 1):
                if not i == doorArray[chosenDoor][0]:
                    if self.GetMapTile((i, doorArray[chosenDoor][1])) == tileID['door-v']:
                        return doorArray[chosenDoor], (i, doorArray[chosenDoor][1])

        return False

    def PrintMap(self):

        for row in range(0, self.lvlHeight, 1):
            outputLine = ""
            for col in range(0, self.lvlWidth, 1):
                outputLine += str(self.GetMapTile((row, col))) + ", "

            # print outputLine

    def DrawMap(self):

        self.powerPelletBlinkTimer += 1
        if self.powerPelletBlinkTimer == 60:
            self.powerPelletBlinkTimer = 0

        for row in range(-1, self.game.screenTileSize[0] + 1, 1):
            outputLine = ""
            for col in range(-1, self.game.screenTileSize[1] + 1, 1):

                # row containing tile that actually goes here
                actualRow = row
                actualCol = col

                useTile = self.GetMapTile((actualRow, actualCol))
                if not useTile == 0 and not useTile == tileID['door-h'] and not useTile == tileID['door-v']:
                    # if this isn't a blank tile

                    if useTile == tileID['pellet-power']:
                        if self.powerPelletBlinkTimer < 30:
                            self.screen.blit(tileIDImage[useTile], (
                            col * 16, row * 16))

                    elif useTile == tileID['showlogo']:
                        self.screen.blit(self.game.imLogo, (
                        col * 16, row * 16))

                    else:
                        self.screen.blit(tileIDImage[useTile], (
                        col * 16, row * 16))

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

                            self.player.homeX = k * 16
                            self.player.homeY = rowNum * 16
                            self.SetMapTile((rowNum, k), 0)

                        elif thisID >= 10 and thisID <= 13:
                            # one of the ghosts

                            self.ghosts[thisID - 10].homeX = k * 16
                            self.ghosts[thisID - 10].homeY = rowNum * 16
                            self.SetMapTile((rowNum, k), 0)

                        elif thisID == 2:
                            # pellet

                            self.pellets += 1

                    rowNum += 1

        # reload all tiles and set appropriate colors
        GetCrossRef(self, self.display)

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

            self.ghosts[i].x = self.ghosts[i].homeX
            self.ghosts[i].y = self.ghosts[i].homeY
            self.ghosts[i].velX = 0
            self.ghosts[i].velY = 0
            self.ghosts[i].state = 1
            self.ghosts[i].speed = 1
            self.ghosts[i].Move()

            # give each ghost a path to a random spot (containing a pellet)
            (randRow, randCol) = (0, 0)

            while not self.GetMapTile((randRow, randCol)) == tileID['pellet'] or (randRow, randCol) == (0, 0):
                randRow = random.randint(1, self.lvlHeight - 2)
                randCol = random.randint(1, self.lvlWidth - 2)

            self.ghosts[i].currentPath = path.FindPath((self.ghosts[i].nearestRow, self.ghosts[i].nearestCol), (randRow, randCol))
            self.ghosts[i].FollowNextPathWay()

        self.player.x = self.player.homeX
        self.player.y = self.player.homeY
        self.player.velX = 0
        self.player.velY = 0
        self.player.Move()

        if self.display:
            self.player.anim_pacmanCurrent = self.player.anim_pacmanS
            self.player.animFrame = 3
