import pygame, os, random
from .path_finder import path
from .tile import tileID, tileIDImage
from .scriptPath import SCRIPT_PATH

ghostcolor = {}
ghostcolor[0] = (255, 0, 0, 255)
ghostcolor[1] = (255, 128, 255, 255)
ghostcolor[2] = (128, 255, 255, 255)
ghostcolor[3] = (255, 128, 0, 255)
ghostcolor[4] = (50, 50, 255, 255)  # blue, vulnerable ghost
ghostcolor[5] = (255, 255, 255, 255)  # white, flashing ghost

class ghost():
    def __init__(self, ghostID, display=True):
        self.x = 0
        self.y = 0
        self.velX = 0
        self.velY = 0
        self.speed = 0.5

        self.nearestRow = 0
        self.nearestCol = 0

        self.id = ghostID

        # ghost "state" variable
        # 1 = normal
        # 2 = vulnerable
        # 3 = spectacles
        self.state = 1

        self.homeX = 0
        self.homeY = 0

        self.currentPath = ""

        if display:
            self.anim = {}
            for i in range(1, 7, 1):
                self.anim[i] = pygame.image.load(
                    os.path.join(SCRIPT_PATH, "images", "sprite", "ghost " + str(i) + ".gif")).convert()

                # change the ghost color in this frame
                for y in range(0, 16, 1):
                    for x in range(0, 16, 1):

                        if self.anim[i].get_at((x, y)) == (255, 0, 0, 255):
                            # default, red ghost body color
                            self.anim[i].set_at((x, y), ghostcolor[self.id])

            self.animFrame = 1
            self.animDelay = 0

    def set(self, thisGame, thisLevel, ghosts, player):
        self.game = thisGame
        self.level = thisLevel
        self.ghosts = ghosts
        self.player = player

    def Draw(self, screen):

        if self.game.mode == 3:
            return False

        # ghost eyes --
        for y in range(4, 8, 1):
            for x in range(3, 7, 1):
                self.anim[self.animFrame].set_at((x, y), (255, 255, 255, 255))
                self.anim[self.animFrame].set_at((x + 6, y), (255, 255, 255, 255))

                if self.player.x > self.x and self.player.y > self.y:
                    # self.player is to lower-right
                    pupilSet = (5, 6)
                elif self.player.x < self.x and self.player.y > self.y:
                    # self.player is to lower-left
                    pupilSet = (3, 6)
                elif self.player.x > self.x and self.player.y < self.y:
                    # self.player is to upper-right
                    pupilSet = (5, 4)
                elif self.player.x < self.x and self.player.y < self.y:
                    # self.player is to upper-left
                    pupilSet = (3, 4)
                else:
                    pupilSet = (4, 6)

        for y in range(pupilSet[1], pupilSet[1] + 2, 1):
            for x in range(pupilSet[0], pupilSet[0] + 2, 1):
                self.anim[self.animFrame].set_at((x, y), (0, 0, 255, 255))
                self.anim[self.animFrame].set_at((x + 6, y), (0, 0, 255, 255))
                # -- end ghost eyes

        if self.state == 1:
            # draw regular ghost (this one)
            screen.blit(self.anim[self.animFrame],
                        (self.x, self.y))
        elif self.state == 2:
            # draw vulnerable ghost

            if self.game.ghostTimer > 100:
                # blue
                screen.blit(self.ghosts[4].anim[self.animFrame],
                            (self.x, self.y))
            else:
                # blue/white flashing
                tempTimerI = int(self.game.ghostTimer / 10)
                if tempTimerI == 1 or tempTimerI == 3 or tempTimerI == 5 or tempTimerI == 7 or tempTimerI == 9:
                    screen.blit(self.ghosts[5].anim[self.animFrame],
                                (self.x, self.y))
                else:
                    screen.blit(self.ghosts[4].anim[self.animFrame],
                                (self.x, self.y))

        elif self.state == 3:
            # draw glasses
            screen.blit(tileIDImage[tileID['glasses']],
                        (self.x, self.y))

        if self.game.mode == 6 or self.game.mode == 7:
            # don't animate ghost if the level is complete
            return False

        self.animDelay += 1

        if self.animDelay == 2:
            self.animFrame += 1

            if self.animFrame == 7:
                # wrap to beginning
                self.animFrame = 1

            self.animDelay = 0

    def Move(self):
        self.x += self.velX
        self.y += self.velY

        self.nearestRow = int(((self.y + 8) / 16))
        self.nearestCol = int(((self.x + 8) / 16))

        for iRow in range(self.nearestRow - 1, self.nearestRow + 2, 1):
            for iCol in range(self.nearestCol - 1, self.nearestCol + 2, 1):
                if (self.x - (iCol * 16) < 16) and (self.x - (iCol * 16) > -16) and (self.y - (iRow * 16) < 16) and (
                        self.y - (iRow * 16) > -16):
                    
                    result = self.level.GetMapTile((iRow, iCol))

                    if result == tileID['door-h']:
                        # ran into a horizontal door
                        for i in range(0, self.level.lvlWidth, 1):
                            if not i == iCol:
                                if self.level.GetMapTile((iRow, i)) == tileID['door-h']:
                                    self.x = i * 16

                                    if self.velX > 0:
                                        self.x += 16
                                    else:
                                        self.x -= 16

                    elif result == tileID['door-v']:
                        # ran into a vertical door
                        for i in range(0, self.level.lvlHeight, 1):
                            if not i == iRow:
                                if self.level.GetMapTile((i, iCol)) == tileID['door-v']:
                                    self.y = i * 16

                                    if self.velY > 0:
                                        self.y += 16
                                    else:
                                        self.y -= 16

        if (self.x % 16) == 0 and (self.y % 16) == 0:
            # if the ghost is lined up with the grid again
            # meaning, it's time to go to the next path item
            
            if ( self.state != 3 ):
                if (self.velX != 0):
                    tileUp = self.level.GetMapTile((self.nearestRow + 1, self.nearestCol))
                    tileDown = self.level.GetMapTile((self.nearestRow - 1, self.nearestCol))
                    if (tileUp < 100 or tileUp > 140) or (tileDown < 100 or tileDown > 140):
                        # if we're not in a "horizontal" tunnel
                        self.currentPath = ""
                if (self.velY != 0):
                    tileLeft = self.level.GetMapTile((self.nearestRow, self.nearestCol - 1))
                    tileRight = self.level.GetMapTile((self.nearestRow, self.nearestCol + 1))
                    if (tileLeft < 100 or tileLeft > 140) or (tileRight < 100 or tileRight > 140):
                        # if we're not in a "vertical" tunnel
                        self.currentPath = ""

            if (self.currentPath):
                self.FollowNextPathWay()

            else:
                self.x = self.nearestCol * 16
                self.y = self.nearestRow * 16

                randNum = random.random()

                if self.state == 1 and randNum < 0.9:
                    # chase pac-man
                    self.currentPath = path.FindPath((self.nearestRow, self.nearestCol),
                                                     (self.player.nearestRow, self.player.nearestCol))
                    # print(self.currentPath)
                    self.FollowNextPathWay()

                else:
                    # glasses found way back to ghost box
                    if self.state == 3:
                        self.state = 1
                        self.speed = self.speed / 4

                    # give ghost a path to a random spot (containing a pellet)
                    (randRow, randCol) = (0, 0)

                    while not self.level.GetMapTile((randRow, randCol)) == tileID['pellet'] or (randRow, randCol) == (0, 0):
                        randRow = random.randint(1, self.level.lvlHeight - 2)
                        randCol = random.randint(1, self.level.lvlWidth - 2)

                    self.currentPath = path.FindPath((self.nearestRow, self.nearestCol), (randRow, randCol))
                    self.FollowNextPathWay()

    def FollowNextPathWay(self):

        # print("Ghost " + str(self.id) + " rem: " + self.currentPath)

        # only follow this pathway if there is a possible path found!
        if not self.currentPath == False:

            if len(self.currentPath) > 0:
                if self.currentPath[0] == "L":
                    (self.velX, self.velY) = (-self.speed, 0)
                    self.direction = "L"
                elif self.currentPath[0] == "R":
                    (self.velX, self.velY) = (self.speed, 0)
                    self.direction = "R"
                elif self.currentPath[0] == "U":
                    (self.velX, self.velY) = (0, -self.speed)
                    self.direction = "U"
                elif self.currentPath[0] == "D":
                    (self.velX, self.velY) = (0, self.speed)
                    self.direction = "D"
                self.currentPath = self.currentPath[1:]
