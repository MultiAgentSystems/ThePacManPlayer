import pygame, os, sys
from path_finder import path

SCRIPT_PATH = sys.path[0]

class pacman():

    def __init__(self, display=True):

        self.x = 0
        self.y = 0
        self.velX = 0
        self.velY = 0
        self.speed = 1

        self.nearestRow = 0
        self.nearestCol = 0

        self.homeX = 0
        self.homeY = 0

        if display:
            self.anim_pacmanL = {}
            self.anim_pacmanR = {}
            self.anim_pacmanU = {}
            self.anim_pacmanD = {}
            self.anim_pacmanS = {}
            self.anim_pacmanCurrent = {}

            for i in range(1, 9, 1):
                self.anim_pacmanL[i] = pygame.image.load(
                    os.path.join(SCRIPT_PATH, "images", "sprite", "pacman-l " + str(i) + ".gif")).convert()
                self.anim_pacmanR[i] = pygame.image.load(
                    os.path.join(SCRIPT_PATH, "images", "sprite", "pacman-r " + str(i) + ".gif")).convert()
                self.anim_pacmanU[i] = pygame.image.load(
                    os.path.join(SCRIPT_PATH, "images", "sprite", "pacman-u " + str(i) + ".gif")).convert()
                self.anim_pacmanD[i] = pygame.image.load(
                    os.path.join(SCRIPT_PATH, "images", "sprite", "pacman-d " + str(i) + ".gif")).convert()
                self.anim_pacmanS[i] = pygame.image.load(
                    os.path.join(SCRIPT_PATH, "images", "sprite", "pacman.gif")).convert()

        # self.pelletSndNum = 0

    def set(self, thisGame, thisLevel, ghosts):
        self.thisGame = thisGame
        self.thisLevel = thisLevel
        self.ghosts = ghosts

    def Move(self):

        self.nearestRow = int(((self.y + 8) / 16))
        self.nearestCol = int(((self.x + 8) / 16))

        # make sure the current velocity will not cause a collision before moving
        if not self.thisLevel.CheckIfHitWall((self.x + self.velX, self.y + self.velY), (self.nearestRow, self.nearestCol)):
            # it's ok to Move
            self.x += self.velX
            self.y += self.velY

            # check for collisions with other tiles (pellets, etc)
            self.thisLevel.CheckIfHitSomething((self.x, self.y), (self.nearestRow, self.nearestCol))

            # check for collisions with the ghosts
            for i in range(0, 4, 1):
                if self.thisLevel.CheckIfHit((self.x, self.y), (self.ghosts[i].x, self.ghosts[i].y), 8):
                    # hit a ghost

                    if self.ghosts[i].state == 1:
                        # ghost is normal
                        self.thisGame.SetMode(2)

                    elif self.ghosts[i].state == 2:
                        # ghost is vulnerable
                        # give them glasses
                        # make them run
                        self.thisGame.AddToScore(self.thisGame.ghostValue)
                        self.thisGame.ghostValue = self.thisGame.ghostValue * 2
                        # snd_eatgh.play()

                        self.ghosts[i].state = 3
                        self.ghosts[i].speed *= 8
                        # and send them to the ghost box
                        self.ghosts[i].x = self.ghosts[i].nearestCol * 16
                        self.ghosts[i].y = self.ghosts[i].nearestRow * 16
                        self.ghosts[i].currentPath = path.FindPath((self.ghosts[i].nearestRow, self.ghosts[i].nearestCol), (
                        self.thisLevel.GetGhostBoxPos()[0] + 1, self.thisLevel.GetGhostBoxPos()[1]))
                        self.ghosts[i].FollowNextPathWay()

                        # set game mode to brief pause after eating
                        self.thisGame.SetMode(5)

        else:
            # we're going to hit a wall -- stop moving
            self.velX = 0
            self.velY = 0

        # deal with power-pellet ghost timer
        if self.thisGame.ghostTimer > 0:
            self.thisGame.ghostTimer -= 1

            if self.thisGame.ghostTimer == 0:
                for i in range(0, 4, 1):
                    if self.ghosts[i].state == 2:
                        self.ghosts[i].state = 1
                        self.ghosts[i].speed *= 2
                self.ghostValue = 0

    def Draw(self, screen):

        if self.thisGame.mode == 3:
            return False

        # set the current frame array to match the direction pacman is facing
        if self.velX > 0:
            self.anim_pacmanCurrent = self.anim_pacmanR
        elif self.velX < 0:
            self.anim_pacmanCurrent = self.anim_pacmanL
        elif self.velY > 0:
            self.anim_pacmanCurrent = self.anim_pacmanD
        elif self.velY < 0:
            self.anim_pacmanCurrent = self.anim_pacmanU

        screen.blit(self.anim_pacmanCurrent[self.animFrame],
                    (self.x - self.thisGame.screenPixelPos[0], self.y - self.thisGame.screenPixelPos[1]))

        if self.thisGame.mode == 1:
            if not self.velX == 0 or not self.velY == 0:
                # only Move mouth when pacman is moving
                self.animFrame += 1

            if self.animFrame == 9:
                # wrap to beginning
                self.animFrame = 1