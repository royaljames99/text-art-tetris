import time
import os
import keyboard
import random
import json

def play(username, highscore):
    gameHandler = GameHandler(username, highscore)
    gameHandler.play()


class GameHandler():
    def __init__(self, username, highscore):
        self.username = username
        self.highscore = highscore
        self.rotationBuffer = 0
        self.xMovementBuffer = 0
        self.yMovementBuffer = time.time() + 1
        self.score = 0

    #PLAY
    def play(self):
        self.initGame()
        self.game()

    #INITIALISE GAME VARIABLES
    def initGame(self):
        self.screen = Screen()
        self.screen.initScreen()

        self.landedBlocks = []

        self.nextBlock = Block(10, 3, random.randint(1,6))
        self.nextBlock.populate()

        self.newBlock()

    #GAMELOOP
    def game(self):
        while True:

            self.printScreen()

            self.keyPresses()

            self.moveMent()

            self.genBlock()

            self.checkRows()

    def checkRows(self):
        rowsToRemove = []
        for i in range(self.screen.height - 3, 0, -1):
            kill = True
            for j in range(len(self.screen.screenArray[i]) - 1):
                if self.screen.screenArray[i][j] == " " and j != self.screen.width - 1:
                    kill = False
            if kill:
                rowsToRemove.append(i)
            
        if len(rowsToRemove) > 0:
            time.sleep(0.1) #this sleep is here purely because when i remove it the code breaks
            self.removeRows(rowsToRemove)
            self.scoreRows(len(rowsToRemove))

    def scoreRows(self, rowCount):
        if rowCount == 1:
            self.score += 40
        elif rowCount == 2:
            self.score += 100
        elif rowCount == 3:
            self.score += 300
        else:
            self.score += 1200

    def removeRows(self, rows):
        for row in rows:
            for block in self.landedBlocks:
                for comp in block.componants:
                    if comp.y == row:
                        comp.status = "Dead"
        
        highest = 0
        for row in rows:
            if row > highest:
                highest = row

        for row in rows:  
            for block in self.landedBlocks:
                for comp in block.componants:
                    if comp.y <= highest - 1:
                        comp.yoffset += 1

    def end(self):
        self.printScreen()
        print()
        print("GAME OVER")
        print()

        print(f"YOUR SCORE WAS: {self.score}")

        if self.score > self.highscore:

            print("NEW HIGHSCORE")
            with open("Logins.json", "r") as file:
                data = json.load(file)
            index = -1
            found = False
            for user in data["logins"]:
                if not found:
                    index += 1
                    if user["Username"] == self.username:
                        found = True
            data["logins"][index]["Highscore"] = self.score
            with open("Logins.json", "w") as file:
                json.dump(data, file, indent = 4)

        else:

            print(f"YOUR HIGHSCORE IS: {self.highscore}")


        time.sleep(5)
        quit()

    #GET NEW BLOCK IF NECISSARY
    def genBlock(self):
        if not self.block.moving:
            self.landedBlocks.append(self.block)
            self.newBlock()

        self.checkCollisions()
        if not self.block.moving:
            self.end()

    def newBlock(self):
        self.block = self.nextBlock
        self.nextBlock = Block(10, 3, random.randint(1,6))
        self.nextBlock.populate()

    #GET KEY PRESSES
    def keyPresses(self):
        if keyboard.is_pressed("w"):
            if time.time() > self.rotationBuffer:
                if self.block.moving:
                    undone = False
                    self.block.rotate("Left")
                    try:
                        self.screen.screenArray = self.block.display(self.screen.screenArray)
                    except:
                        self.block.rotate("Right")
                    else:
                        for i in self.screen.screenArray:
                            if (i[0] == "█" or i[len(i) - 1] == "█") and not undone:
                                self.block.rotate("Right")
                                undone = True
                    self.rotationBuffer = time.time() + 0.2


        elif keyboard.is_pressed("s"):
            if time.time() > self.rotationBuffer:
                if self.block.moving:
                    undone = False
                    self.block.rotate("Right")
                    try:
                        self.screen.screenArray = self.block.display(self.screen.screenArray)
                    except:
                        self.block.rotate("Left")
                    else:
                        for i in self.screen.screenArray:
                            if (i[0] == "█" or i[len(i) - 1] == "█") and not undone:
                                self.block.rotate("Left")
                                undone = True
                    self.rotationBuffer = time.time() + 0.2


        elif keyboard.is_pressed("a"):
            if time.time() > self.xMovementBuffer:
                if self.block.moving:
                    self.block.move("Left", self)
                    self.xMovementBuffer = time.time() + 0.2
        

        elif keyboard.is_pressed("d"):
            if time.time() > self.xMovementBuffer:
                if self.block.moving:
                    self.block.move("Right", self)
                    self.xMovementBuffer = time.time() + 0.2

        elif keyboard.is_pressed(" "):
            if time.time() > self.xMovementBuffer:
                while self.block.moving:

                    self.checkCollisions()


                    if self.block.moving:
                        self.block.y += 1
                self.xMovementBuffer = time.time() + 0.2
            #self.screen.display()

    #VERTICAL MOVEMENT
    def moveMent(self):
        if self.block.moving:
            if self.yMovementBuffer < time.time():
                self.block.y += 1
                self.yMovementBuffer = time.time() + 1

                self.checkCollisions()

    #check for block collisions
    def checkCollisions(self):
        for i in self.block.componants:
            if self.block.y + i.rely + 1 >= self.screen.height - 2:
                self.block.moving = False

            for a in self.landedBlocks:
                for b in a.componants:
                    if b.status == "Alive":
                        if a.y + b.rely + b.yoffset == self.block.y + i.rely + 1 and b.x == i.x:
                            self.block.moving = False

    #DISPLAY SCREEN
    def printScreen(self):
        #BUFFER CHECK
        if self.screen.displayBuffer < time.time():
            #WIPE SCREEN
            self.screen.wipe()


            #block
            self.screen.screenArray = self.block.display(self.screen.screenArray)

            #landedBlockes
            for i in self.landedBlocks:
                self.screen.screenArray = i.display(self.screen.screenArray)


            #DISPLAY ONTO SCREEN
            self.screen.display(self)

            #UPDATE SCREENBUFFER
            self.screen.displayBuffer = time.time() + 0.02


class Screen():
    def __init__(self):
        self.width, self.height = 22, 22
        self.displayBuffer = 0
        self.screenArray = []
        self.displayBuffer = 0

    #INITIALISE SCREENARRAY
    def initScreen(self):
        for i in range(self.height):
            self.screenArray.append([])
            for j in range(self.width):
                self.screenArray[i].append(" ")
    
    #WIPE SCREENARRAY
    def wipe(self):
        for i in range(len(self.screenArray)):
            for j in range(len(self.screenArray[i])):
                self.screenArray[i][j] = " "
        for i in range(len(self.screenArray) - 1):
            self.screenArray[i][0] = "<!"
            self.screenArray[i][self.width - 1] = "!>"
        for i in range(1,len(self.screenArray[i]) - 1):
            self.screenArray[self.height - 2][i] = "="
        for i in range(2,self.width):
            if i % 2 == 0:
                self.screenArray[self.height - 1][i] = "\\"
            else:
                self.screenArray[self.height - 1][i] = "/"

    #DISPLAY SCREEN
    def display(self, gameHandler):
        os.system("cls")

        print(f"Score: {gameHandler.score}")
        print(f"Highscore: {gameHandler.highscore}")
        print("Next block:")
        self.getBlockPic(gameHandler)
        print()
        
        #DISPLAY SCREENARRAY ONTO SCREEN
        for i in self.screenArray:
            line = ""
            for j in i:
                line += j
            print(line)

    def getBlockPic(self, gameHandler):
        t = gameHandler.nextBlock.type
        if t == 1:
            print("        ██\n        ████\n        ██")
        elif t == 2:
            print("        ████\n          ██\n          ██")
        elif t == 3:
            print("        ████        \n        ██\n        ██")
        elif t == 4:
            print("        ██\n        ████\n          ██")
        elif t == 5:
            print("          ██\n        ████\n        ██")
        elif t == 6:
            print("\n        ████████\n")


class Block():
    def __init__(self, x, y, blktype):
        self.componants = []
        self.x = x
        self.y = y
        self.type = blktype
        self.direction = "W"
        self.moving = True

    def populate(self):
        for i in range(4):
            self.componants.append(Componant(i))

    def move(self, dire, gameHandler):
        if dire == "Left" and self.checkMove(gameHandler, dire):
            self.x -= 2
        elif dire == "Right" and self.checkMove(gameHandler, dire):
            self.x += 2

        #check if moved off screen and reverse if necissary
        for i in self.componants:
            if int(self.x + (2 * i.relx)) < 1:
                self.x += 2
            if int(self.x + (2 * i.relx)) > gameHandler.screen.width - 1:
                self.x -= 2

    def checkMove(self, gameHandler, dire):      

        for landedBlock in gameHandler.landedBlocks:
            for landedComponant in landedBlock.componants:
                for componant in self.componants:
                    if (landedBlock.y + landedComponant.rely + landedComponant.yoffset) == (self.y + componant.rely) and landedComponant.status == "Alive":
                        if dire == "Left":
                            if landedComponant.x == (componant.x - 2):
                                return False
                        else:
                            if landedComponant.x == componant.x + 2:
                                return False
        return True

    def rotate(self, dire):
        if dire == "Right":
            if self.direction == "N":
                self.direction = "E"
            elif self.direction == "E":
                self.direction = "S"
            elif self.direction == "S":
                self.direction = "W"
            elif self.direction == "W":
                self.direction = "N"
        if dire == "Left":
            if self.direction == "N":
                self.direction = "W"
            elif self.direction == "W":
                self.direction = "S"
            elif self.direction == "S":
                self.direction = "E"
            elif self.direction == "E":
                self.direction = "N"

    def display(self, screenArray):
        if self.type == 1:
        #           ██
        #    COR => ████
        #           ██            
            if self.direction == "N":
                screenArray = self.componants[0].display(0,0,screenArray, self)
                screenArray = self.componants[1].display(0,1,screenArray, self)
                screenArray = self.componants[2].display(1,0,screenArray, self)
                screenArray = self.componants[3].display(0,-1,screenArray, self)
            elif self.direction == "E":
                screenArray = self.componants[0].display(0,0,screenArray, self)
                screenArray = self.componants[1].display(0,1,screenArray, self)
                screenArray = self.componants[2].display(1,0,screenArray, self)
                screenArray = self.componants[3].display(-1,0,screenArray, self)
            elif self.direction == "S":
                screenArray = self.componants[0].display(0,0,screenArray, self)
                screenArray = self.componants[1].display(0,1,screenArray, self)
                screenArray = self.componants[2].display(-1,0,screenArray, self)
                screenArray = self.componants[3].display(0,-1,screenArray, self)
            elif self.direction == "W":
                screenArray = self.componants[0].display(0,0,screenArray, self)
                screenArray = self.componants[1].display(0,-1,screenArray, self)
                screenArray = self.componants[2].display(1,0,screenArray, self)
                screenArray = self.componants[3].display(-1,0,screenArray, self)

        elif self.type == 2:
        #         ████
        #    COR => ██
        #           ██
            if self.direction == "N":
                screenArray = self.componants[0].display(0,0,screenArray, self)
                screenArray = self.componants[1].display(-1,-1,screenArray, self)
                screenArray = self.componants[2].display(0,-1,screenArray, self)
                screenArray = self.componants[3].display(0,1,screenArray, self)
            elif self.direction == "E":
                screenArray = self.componants[0].display(0,0,screenArray, self)
                screenArray = self.componants[1].display(-1,0,screenArray, self)
                screenArray = self.componants[2].display(1,-1,screenArray, self)
                screenArray = self.componants[3].display(1,0,screenArray, self)
            elif self.direction == "S":
                screenArray = self.componants[0].display(0,0,screenArray, self)
                screenArray = self.componants[1].display(0,-1,screenArray, self)
                screenArray = self.componants[2].display(0,1,screenArray, self)
                screenArray = self.componants[3].display(1,1,screenArray, self)
            elif self.direction == "W":
                screenArray = self.componants[0].display(0,0,screenArray, self)
                screenArray = self.componants[1].display(-1,1,screenArray, self)
                screenArray = self.componants[2].display(-1,0,screenArray, self)
                screenArray = self.componants[3].display(1,0,screenArray, self)
        
        elif self.type == 3:
        #           ████
        #    COR => ██  
        #           ██
            if self.direction == "N":
                screenArray = self.componants[0].display(0,0,screenArray, self)
                screenArray = self.componants[1].display(0,1,screenArray, self)
                screenArray = self.componants[2].display(1,0,screenArray, self)
                screenArray = self.componants[3].display(0,2,screenArray, self)
            elif self.direction == "E":
                screenArray = self.componants[0].display(0,0,screenArray, self)
                screenArray = self.componants[1].display(1,0,screenArray, self)
                screenArray = self.componants[2].display(1,1,screenArray, self)
                screenArray = self.componants[3].display(-1,0,screenArray, self)
            elif self.direction == "S":
                screenArray = self.componants[0].display(0,0,screenArray, self)
                screenArray = self.componants[1].display(0,1,screenArray, self)
                screenArray = self.componants[2].display(0,-1,screenArray, self)
                screenArray = self.componants[3].display(-1,1,screenArray, self)
            elif self.direction == "W":
                screenArray = self.componants[0].display(0,0,screenArray, self)
                screenArray = self.componants[1].display(-1,-1,screenArray, self)
                screenArray = self.componants[2].display(-1,0,screenArray, self)
                screenArray = self.componants[3].display(1,0,screenArray, self)
        
        elif self.type == 4:
        #           ██  
        #    COR => ████
        #             ██
            if self.direction == "N":
                screenArray = self.componants[0].display(0,0,screenArray, self)
                screenArray = self.componants[1].display(0,1,screenArray, self)
                screenArray = self.componants[2].display(1,1,screenArray, self)
                screenArray = self.componants[3].display(1,2,screenArray, self)
            elif self.direction == "E":
                screenArray = self.componants[0].display(0,0,screenArray, self)
                screenArray = self.componants[1].display(0,1,screenArray, self)
                screenArray = self.componants[2].display(1,0,screenArray, self)
                screenArray = self.componants[3].display(-1,1,screenArray, self)
            elif self.direction == "S":
                screenArray = self.componants[0].display(0,0,screenArray, self)
                screenArray = self.componants[1].display(0,1,screenArray, self)
                screenArray = self.componants[2].display(1,1,screenArray, self)
                screenArray = self.componants[3].display(1,2,screenArray, self)
            elif self.direction == "W":
                screenArray = self.componants[0].display(0,0,screenArray, self)
                screenArray = self.componants[1].display(0,1,screenArray, self)
                screenArray = self.componants[2].display(1,0,screenArray, self)
                screenArray = self.componants[3].display(-1,1,screenArray, self)

        elif self.type == 5:
        #             ██
        #    COR => ████
        #           ██
            if self.direction == "N":
                screenArray = self.componants[0].display(1,0,screenArray, self)
                screenArray = self.componants[1].display(0,0,screenArray, self)
                screenArray = self.componants[2].display(0,1,screenArray, self)
                screenArray = self.componants[3].display(1,-1,screenArray, self)
            elif self.direction == "E":
                screenArray = self.componants[0].display(0,0,screenArray, self)
                screenArray = self.componants[1].display(-1,0,screenArray, self)
                screenArray = self.componants[2].display(1,1,screenArray, self)
                screenArray = self.componants[3].display(0,1,screenArray, self)
            elif self.direction == "S":
                screenArray = self.componants[0].display(1,0,screenArray, self)
                screenArray = self.componants[1].display(0,0,screenArray, self)
                screenArray = self.componants[2].display(0,1,screenArray, self)
                screenArray = self.componants[3].display(1,-1,screenArray, self)
            elif self.direction == "W":
                screenArray = self.componants[0].display(0,0,screenArray, self)
                screenArray = self.componants[1].display(-1,0,screenArray, self)
                screenArray = self.componants[2].display(1,1,screenArray, self)
                screenArray = self.componants[3].display(0,1,screenArray, self)

        elif self.type == 6:
        #           ██
        #    COR => ██
        #           ██
        #           ██            
            if self.direction == "N":
                screenArray = self.componants[0].display(0,0,screenArray, self)
                screenArray = self.componants[1].display(0,1,screenArray, self)
                screenArray = self.componants[2].display(0,2,screenArray, self)
                screenArray = self.componants[3].display(0,3,screenArray, self)
            elif self.direction == "E":
                screenArray = self.componants[0].display(0,0,screenArray, self)
                screenArray = self.componants[1].display(-1,0,screenArray, self)
                screenArray = self.componants[2].display(1,0,screenArray, self)
                screenArray = self.componants[3].display(2,0,screenArray, self)
            elif self.direction == "S":
                screenArray = self.componants[0].display(0,0,screenArray, self)
                screenArray = self.componants[1].display(0,1,screenArray, self)
                screenArray = self.componants[2].display(0,2,screenArray, self)
                screenArray = self.componants[3].display(0,3,screenArray, self)
            elif self.direction == "W":
                screenArray = self.componants[0].display(0,0,screenArray, self)
                screenArray = self.componants[1].display(-1,0,screenArray, self)
                screenArray = self.componants[2].display(1,0,screenArray, self)
                screenArray = self.componants[3].display(-2,0,screenArray, self)

        return screenArray


class Componant():
    def __init__(self, id):
        self.relx = 0
        self.rely = 0
        self.x = 0
        self.y = 0
        self.status = "Alive"
        self.id = id
        self.yoffset = 0

    def display(self, relx, rely, screenArray, base):
        self.x = int(base.x + (2*relx))
        self.y = int(base.y + rely + self.yoffset)
        self.relx = int(relx)
        self.rely = int(rely)
        if self.status == "Alive":
            screenArray[self.y][self.x - 1], screenArray[self.y][self.x] = "█", "█"
        return screenArray
