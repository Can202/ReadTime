import pygame
import constant
import image
import objects
import random
import sound
import platformdetect

pygame.init()

class Game:
    def __init__(self) -> None:

        self.window = pygame.display.set_mode((constant.DEFINEWIDTH, constant.DEFINEHEIGHT), pygame.FULLSCREEN)
        
        pygame.display.set_caption("Read Time")

        self.clock = pygame.time.Clock()
        self.running = True

        self.mouseposX = 0
        self.mouseposY = 0
        self.realmouseposX = 0
        self.realmouseposY = 0

        self.deltaTime = 0

        self.xoffset = 0
        self.offset = pygame.Vector2(0, 0)
        self.fix = 1
        self.mousepressed = False

        self.mainGame = GameLogic(False)
        self.mainMenu = Menu()

        self.sound_channel = pygame.mixer.Channel(2)
        self.musicallowed = True
        self.hardmode = False





    def mainloop(self):
        while self.running:
            self.mousepressed = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.mousepressed = True
                    self.realmouseposX, self.realmouseposY = event.pos
                    self.mouseposX = (self.realmouseposX - self.offset.x) / self.fix
                    self.mouseposY = (self.realmouseposY - self.offset.y) / self.fix
                    pygame.mouse.get_rel()
                elif platformdetect.platform() != "android":
                    self.realmouseposX, self.realmouseposY = pygame.mouse.get_pos()
                    self.mouseposX = (self.realmouseposX - self.offset.x) / self.fix
                    self.mouseposY = (self.realmouseposY - self.offset.y) / self.fix
                #if event.type == pygame.MOUSEBUTTONUP:
                #    self.mousepressed = False
            self.keys = pygame.key.get_pressed()

            if self.sound_channel.get_busy() == False and self.musicallowed:
                self.sound_channel.play(sound.SONG)
            
            if self.musicallowed == False:
                self.sound_channel.stop()
                
            if self.mainGame.running:
                self.mainGame.mainloop(self.fix, self.offset,
                                    self.deltaTime,
                                    self.mouseposX, self.mouseposY,
                                    self.mousepressed, self.hardmode)
            if self.mainMenu.running:
                self.mainMenu.mainloop(self.fix, self.offset,
                                    self.deltaTime,
                                    self.mouseposX, self.mouseposY,
                                    self.mousepressed)
            
            if self.mainMenu.playbtn.get_pressed:
                self.mainMenu.playbtn.get_pressed = False
                self.mainMenu.running = False
                self.mainGame.running = True
                self.mainGame.goods = 0
            elif self.mainGame.quitbtn.get_pressed:
                self.mainGame.quitbtn.get_pressed = False
                self.mainGame.goods = 0
                self.mainMenu.running = True
                self.mainGame.running = False
                self.mainMenu.quitTime.timing = True
            elif self.mainMenu.quitbtn.get_pressed:
                if self.mainMenu.quitTime.timing == False:
                    self.running = False
                self.mainMenu.quitbtn.get_pressed = False

            
            if self.mainMenu.hardbtn.get_pressed:
                self.mainMenu.hardbtn.get_pressed = False
                if self.mainMenu.hardbtntime.timing == False:
                    self.mainMenu.hardbtntime.timing = True
                    if self.hardmode:
                        self.hardmode = False
                        self.mainMenu.hardmode.image = image.resize(image.ERROR,40,40)
                    else:
                        self.hardmode = True
                        self.mainMenu.hardmode.image = image.resize(image.TICKET,40,40)
            if self.mainMenu.musicbtn.get_pressed:
                self.mainMenu.musicbtn.get_pressed = False
                if self.mainMenu.musicbtntime.timing == False:
                    self.mainMenu.musicbtntime.timing = True
                    if self.musicallowed:
                        self.musicallowed = False
                        self.mainMenu.musicmode.image = image.resize(image.ERROR,40,40)
                    else:
                        self.musicallowed = True
                        self.mainMenu.musicmode.image = image.resize(image.TICKET,40,40)
            if self.mainMenu.languagebtn.get_pressed:
                self.mainMenu.languagebtn.get_pressed = False
                if self.mainMenu.languagebtntime.timing == False:
                    if self.mainGame.language == "en":
                        self.mainGame.language = "es"
                        self.mainMenu.languagebtn.image = image.ES
                        self.mainMenu.languagebtn.get_pressed = image.ES
                        self.mainMenu.languagebtn.image_hover = image.ES
                        self.mainMenu.languagebtn.normal_image = image.ES
                    elif self.mainGame.language == "es":
                        self.mainGame.language = "en"
                        self.mainMenu.languagebtn.image = image.EN
                        self.mainMenu.languagebtn.get_pressed = image.EN
                        self.mainMenu.languagebtn.image_hover = image.EN
                        self.mainMenu.languagebtn.normal_image = image.EN
                self.mainMenu.languagebtntime.timing = True

            self.screenfix()
            self.deltaTime = self.clock.tick(60) / 1000.0


            self.window.fill((0, 0, 0))
            if self.mainGame.running:
                self.window.blit(pygame.transform.scale(
                    self.mainGame.screen, (int(constant.WIDTH*self.fix), int(constant.HEIGHT*self.fix))), 
                    self.offset)
            if self.mainMenu.running:
                self.window.blit(pygame.transform.scale(
                    self.mainMenu.screen, (int(constant.WIDTH*self.fix), int(constant.HEIGHT*self.fix))), 
                    self.offset)

            pygame.display.update()
    
    def screenfix(self):
        height = self.window.get_height()
        width = self.window.get_width()
        if (height / 9) <= (width/16):
            self.fix = (height / constant.HEIGHT)
            self.offset.x = (width - (constant.WIDTH * self.fix)) / 2
            self.offset.y = 0
        else:
            self.fix = (width / constant.WIDTH)
            self.offset.x = 0
            self.offset.y = (height - (constant.HEIGHT * self.fix)) / 2

class GameLogic:
    def __init__(self, _running=True) -> None:

        self.running = _running
        
        self.screen = pygame.Surface((constant.WIDTH, constant.HEIGHT))

        self.clockOnScreen = objects.Node(pygame.Vector2((constant.WIDTH - 540)/2, 20))
        self.minuteHand = objects.Hand(pygame.Vector2((constant.WIDTH + 10)/2, (constant.HEIGHT + 120)/2), image.MINUTE, 10, 90)
        self.hourHand = objects.Hand(pygame.Vector2((constant.WIDTH + 22)/2, (constant.HEIGHT + 120)/2), image.HOUR, 22, 7.5)
        self.background = objects.Background()

        self.btn1 = objects.Button(pygame.Vector2(20,200), _text="As")
        self.btn2 = objects.Button(pygame.Vector2(950,200), _text="As2")
        self.btn3 = objects.Button(pygame.Vector2(20,500), _text="As3")
        self.btn4 = objects.Button(pygame.Vector2(950,500), _text="As4")
        



        self.shuffle = True
        self.correctbtnnumber = random.randint(1,4)
        self.correctbtn = objects.Hour()

        self.otherbtn1 = objects.Hour()
        self.otherbtn2 = objects.Hour() 
        self.otherbtn3 = objects.Hour() 

        self.language = "en"
        self.quitbtn = objects.Button(pygame.Vector2(55,70),
                                    image.resize(image.ERROR,40,40), "",
                                    image.resize(image.ERROR,40,40),image.resize(image.ERROR,40,40))
        

        self.goods = 0
        self.goodstext = objects.Text(str(self.goods),
                                      pygame.Vector2(constant.WIDTH-50,10),
                                      constant.GREEN)
        self.goodsblank = objects.Node(pygame.Vector2(constant.WIDTH-65,2), image.resize(image.BLANK, 60, 40))
        self.good = 0
        self.timegood = objects.Timer(2)
        self.ticketonScreen = objects.Node(
            pygame.Vector2((constant.WIDTH - image.TICKET.get_width())/2, constant.HEIGHT),
            image.TICKET)
        self.ticketanimation = False

        self.erroronScreen = objects.Node(
            pygame.Vector2((constant.WIDTH - image.ERROR.get_width())/2, constant.HEIGHT),
            image.ERROR)
        self.erroranimation = False

    def mainloop(self, _fix, _offset, _dt, _mpx, _mpy, _mp, _hm):

        self.fix = _fix
        self.offset = _offset
        self.deltaTime = _dt
        self.mouseposX = _mpx
        self.mouseposY = _mpy

        self.mousepressed = _mp 
        self.hardmode = _hm

        self.update()
        self.draw()
    
    def update(self):
        if self.shuffle:
            self.correctbtnnumber = random.randint(1,4)
            self.correctbtn.newSet()
            self.otherbtn1.newSet()
            self.otherbtn2.newSet()
            self.otherbtn3.newSet()
            while self.otherbtn1.getTuple() == self.correctbtn.getTuple():
                self.otherbtn1.newSet()
            while self.otherbtn2.getTuple() == self.correctbtn.getTuple():
                self.otherbtn2.newSet()
            while self.otherbtn2.getTuple() == self.otherbtn1.getTuple():
                self.otherbtn2.newSet()
            while self.otherbtn3.getTuple() == self.correctbtn.getTuple():
                self.otherbtn3.newSet()
            while self.otherbtn3.getTuple() == self.otherbtn1.getTuple():
                self.otherbtn2.newSet()
            while self.otherbtn3.getTuple() == self.otherbtn2.getTuple():
                self.otherbtn2.newSet()
            self.otherbtn2.newSet()
            self.otherbtn3.newSet()
            self.shuffle = False



        if self.correctbtnnumber == 1:
            self.btn1.text.text = self.correctbtn.getStrHour(self.language)

            self.btn2.text.text = self.otherbtn1.getStrHour(self.language)
            self.btn3.text.text = self.otherbtn2.getStrHour(self.language)
            self.btn4.text.text = self.otherbtn3.getStrHour(self.language)
        elif self.correctbtnnumber == 2:
            self.btn2.text.text = self.correctbtn.getStrHour(self.language)

            self.btn1.text.text = self.otherbtn1.getStrHour(self.language)
            self.btn3.text.text = self.otherbtn2.getStrHour(self.language)
            self.btn4.text.text = self.otherbtn3.getStrHour(self.language)
        elif self.correctbtnnumber == 3:
            self.btn3.text.text = self.correctbtn.getStrHour(self.language)

            self.btn1.text.text = self.otherbtn1.getStrHour(self.language)
            self.btn2.text.text = self.otherbtn2.getStrHour(self.language)
            self.btn4.text.text = self.otherbtn3.getStrHour(self.language)
        elif self.correctbtnnumber == 4:
            self.btn4.text.text = self.correctbtn.getStrHour(self.language)

            self.btn1.text.text = self.otherbtn1.getStrHour(self.language)
            self.btn2.text.text = self.otherbtn2.getStrHour(self.language)
            self.btn3.text.text = self.otherbtn3.getStrHour(self.language)

        self.return_angle_by_hour(self.correctbtn.hour, self.correctbtn.minutes)

        self.background.update(self.deltaTime)
        self.clockOnScreen.update(self.deltaTime)
        self.ticketonScreen.update(self.deltaTime)
        self.erroronScreen.update(self.deltaTime)
        self.minuteHand.update(self.deltaTime)
        self.hourHand.update(self.deltaTime)
        self.goodstext.text = str(self.goods)

        self.btn1.update(self.deltaTime, self.mousepressed, self.mouseposX, self.mouseposY, self.fix, self.offset)
        self.btn2.update(self.deltaTime, self.mousepressed, self.mouseposX, self.mouseposY, self.fix, self.offset)
        self.btn3.update(self.deltaTime, self.mousepressed, self.mouseposX, self.mouseposY, self.fix, self.offset)
        self.btn4.update(self.deltaTime, self.mousepressed, self.mouseposX, self.mouseposY, self.fix, self.offset)
        
        self.quitbtn.update(self.deltaTime, self.mousepressed, self.mouseposX, self.mouseposY, self.fix, self.offset)

        if self.btn1.get_pressed:
            if self.timegood.time == 0:
                if self.correctbtnnumber == 1:
                    self.good = 1
                else:
                    self.good = -1
            self.btn1.get_pressed = False
        elif self.btn2.get_pressed:
            if self.timegood.time == 0:
                if self.correctbtnnumber == 2:
                    self.good = 1
                else:
                    self.good = -1
            self.btn2.get_pressed = False
        elif self.btn3.get_pressed:
            if self.timegood.time == 0:
                if self.correctbtnnumber == 3:
                    self.good = 1
                else:
                    self.good = -1
            self.btn3.get_pressed = False
        elif self.btn4.get_pressed:
            if self.timegood.time == 0:
                if self.correctbtnnumber == 4:
                    self.good = 1
                else:
                    self.good = -1
            self.btn4.get_pressed = False
        
        if self.good == 1:
            sound.GOOD.play()
            self.shuffle = True
            self.timegood.timing = True
            self.goods += 1
            self.good = 0
            self.ticketanimation = True
        elif self.good == -1:
            if self.hardmode:
                self.goods = 0
            sound.BAD.play()
            self.timegood.timing = True
            self.good = 0
            self.erroranimation = True

        if self.ticketanimation:
            if self.timegood.time < .7:
                self.ticketonScreen.position.y -= 694 * self.deltaTime
            if self.timegood.time > 1.3:
                self.ticketonScreen.position.y += 694 * self.deltaTime
        
        if self.erroranimation:
            if self.timegood.time < .7:
                self.erroronScreen.position.y -= 721 * self.deltaTime
            if self.timegood.time > 1.3:
                self.erroronScreen.position.y += 721 * self.deltaTime
        if self.timegood.timing == False:
            self.ticketonScreen.position.y = constant.HEIGHT
            self.ticketanimation = False
            self.erroronScreen.position.y = constant.HEIGHT
            self.erroranimation = False


        self.timegood.update(self.deltaTime)

    def draw(self):
        self.background.draw(self.screen)
        self.clockOnScreen.draw(self.screen)
        self.minuteHand.draw(self.screen)
        self.hourHand.draw(self.screen)
        self.ticketonScreen.draw(self.screen)
        self.erroronScreen.draw(self.screen)
        self.goodsblank.draw(self.screen)
        self.goodstext.draw(self.screen)

        self.btn1.draw(self.screen)
        self.btn2.draw(self.screen)
        self.btn3.draw(self.screen)
        self.btn4.draw(self.screen)

        self.quitbtn.draw(self.screen)

    def return_angle_by_hour(self, hour, minutes):
        
        self.hourHand.rotation = 360 - ((30 * hour) + (minutes * (30 / 60)))

        if hour == 12:
            self.hourHand.rotation = 360 -(minutes * (30 / 60))

        if minutes == 0:
            minutes = 60
        self.minuteHand.rotation = 360 - (30 * (minutes / 5))
        
class Menu:
    def __init__(self, _running = True) -> None:
        
        self.running = _running
        
        self.screen = pygame.Surface((constant.WIDTH, constant.HEIGHT))

        self.menuphoto = objects.Node(pygame.Vector2(300,20),
                                      image.MENU)

        self.background = objects.Background()
        self.playbtn = objects.Button(
            pygame.Vector2((constant.WIDTH-310)/2, (constant.HEIGHT+300)/2),
            _text="        touch to play")
        
        self.quitbtn = objects.Button(pygame.Vector2(55,70),
                                    image.resize(image.ERROR,40,40), "",
                                    image.resize(image.ERROR,40,40),image.resize(image.ERROR,40,40))
        self.quitTime = objects.Timer(.3)


        self.musicbtn = objects.Button(pygame.Vector2(1170,70),
                                    image.resize(image.MUSICMODE,80,80), "",
                                    image.resize(image.MUSICMODE,80,80),image.resize(image.MUSICMODE,80,80))
        self.hardbtn = objects.Button(pygame.Vector2(1170,180),
                                    image.resize(image.HARDMODE,80,80), "",
                                    image.resize(image.HARDMODE,80,80),image.resize(image.HARDMODE,80,80))
        self.musicmode = objects.Node(pygame.Vector2(1120,90),image.resize(image.TICKET,40,40))
        self.hardmode = objects.Node(pygame.Vector2(1120,200),image.resize(image.ERROR,40,40))

        self.languagebtn = objects.Button(pygame.Vector2(1170,300),
                                    image.EN, "",
                                    image.EN,image.EN)
        self.languagebtntime = objects.Timer(.3)
        

        self.musicbtntime = objects.Timer(.3)
        self.hardbtntime = objects.Timer(.3)
    def mainloop(self, _fix, _offset, _dt, _mpx, _mpy, _mp):

        self.fix = _fix
        self.offset = _offset
        self.deltaTime = _dt
        self.mouseposX = _mpx
        self.mouseposY = _mpy

        self.mousepressed = _mp 

        self.update()
        self.draw()
    
    def update(self):
        self.background.update(self.deltaTime)
        self.quitTime.update(self.deltaTime)
        self.playbtn.update(self.deltaTime, self.mousepressed, self.mouseposX, self.mouseposY, self.fix, self.offset)
        self.quitbtn.update(self.deltaTime, self.mousepressed, self.mouseposX, self.mouseposY, self.fix, self.offset)
        self.hardbtn.update(self.deltaTime, self.mousepressed, self.mouseposX, self.mouseposY, self.fix, self.offset)
        self.musicbtn.update(self.deltaTime, self.mousepressed, self.mouseposX, self.mouseposY, self.fix, self.offset)
        self.languagebtn.update(self.deltaTime, self.mousepressed, self.mouseposX, self.mouseposY, self.fix, self.offset)

        self.languagebtntime.update(self.deltaTime)
        self.musicbtntime.update(self.deltaTime)
        self.hardbtntime.update(self.deltaTime)

    def draw(self):
        self.background.draw(self.screen)
        self.menuphoto.draw(self.screen)
        self.playbtn.draw(self.screen)
        self.quitbtn.draw(self.screen)
        self.musicbtn.draw(self.screen)
        self.hardbtn.draw(self.screen)
        self.musicmode.draw(self.screen)
        self.hardmode.draw(self.screen)
        self.languagebtn.draw(self.screen)

if __name__ == "__main__":
    game = Game()
    game.mainloop()
