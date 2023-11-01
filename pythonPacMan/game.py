import pygame, os, sys

SCRIPT_PATH = sys.path[0]

class game():

    def __init__(self, screen, display):
        self.screen = screen
        self.levelNum = 0
        self.score = 0
        # self.lives = 3 # ! IMPORTANT
        self.lives = 0

        self.target = 0

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

        self.screenTileSize = (23, 21)
        self.screenSize = (self.screenTileSize[1] * 16, self.screenTileSize[0] * 16)

        if display:
            # numerical display digits
            self.digit = {}
            for i in range(0, 10, 1):
                self.digit[i] = pygame.image.load(os.path.join(SCRIPT_PATH, "images", "text", str(i) + ".gif")).convert()
            self.imLife = pygame.image.load(os.path.join(SCRIPT_PATH, "images", "text", "life.gif")).convert()
            self.imGameOver = pygame.image.load(os.path.join(SCRIPT_PATH, "images", "text", "gameover.gif")).convert()
            self.imReady = pygame.image.load(os.path.join(SCRIPT_PATH, "images", "text", "ready.gif")).convert()
            self.imLogo = pygame.image.load(os.path.join(SCRIPT_PATH, "images", "text", "logo.gif")).convert()

    def set(self, thisLevel, player, ghosts):
        self.thisLevel = thisLevel
        self.player = player
        self.ghosts = ghosts

    def StartNewGame(self):
        self.levelNum = 1
        self.score = 0
        self.lives = 3 #important
        self.elapsedTime = 0

        self.target = 0

        self.SetMode(4)
        self.thisLevel.LoadLevel(self.GetLevelNum())
        self.screenTileSize = (self.thisLevel.lvlHeight, self.thisLevel.lvlWidth)
        self.screenSize = (self.screenTileSize[1] * 16, self.screenTileSize[0] * 16)
        window = pygame.display.set_mode(self.screenSize, pygame.DOUBLEBUF | pygame.HWSURFACE)

    def AddToScore(self, amount):

        extraLifeSet = [25000, 50000, 100000, 150000]

        for specialScore in extraLifeSet:
            if self.score < specialScore and self.score + amount >= specialScore:
                self.lives += 1

        self.score += amount

    def DrawScore(self):
        self.DrawNumber(self.score, (24 + 16, self.screenSize[1] - 24))

        for i in range(0, self.lives, 1):
            self.screen.blit(self.imLife, (24 + i * 10 + 16, self.screenSize[1] - 12))

        if self.mode == 3:
            self.screen.blit(self.imGameOver, (self.screenSize[0] / 2 - 32, self.screenSize[1] / 2 - 10))
        elif self.mode == 4:
            self.screen.blit(self.imReady, (self.screenSize[0] / 2 - 20, self.screenSize[1] / 2 + 12))

        self.DrawNumber(self.levelNum, (0, self.screenSize[1] - 12))

    def DrawNumber(self, number, x_y):
        x, y = x_y
        number = int(number)
        strNumber = str(number)

        for i in range(0, len(strNumber), 1):
            iDigit = int(strNumber[i])
            self.screen.blit(self.digit[iDigit], (x + i * 9, y))

    def GetLevelNum(self):
        return self.levelNum

    def SetNextLevel(self):
        self.levelNum += 1

        self.target = 0

        self.SetMode(4)
        self.thisLevel.LoadLevel(self.GetLevelNum())

        self.screenTileSize = (self.thisLevel.lvlHeight, self.thisLevel.lvlWidth)
        self.screenSize = (self.screenTileSize[1] * 16, self.screenTileSize[0] * 16)
        window = pygame.display.set_mode(self.screenSize, pygame.DOUBLEBUF | pygame.HWSURFACE)

        self.player.velX = 0
        self.player.velY = 0
        self.player.anim_pacmanCurrent = self.player.anim_pacmanS

    def SetMode(self, newMode):
        self.mode = newMode
        self.modeTimer = 0
        # print " ***** GAME MODE IS NOW ***** " + str(newMode)