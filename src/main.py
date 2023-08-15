import pygame
import constant
import image
import objects
import random
import sound


pygame.init()

class Game:
    def __init__(self) -> None:

        self.window = pygame.display.set_mode((constant.DEFINEWIDTH, constant.DEFINEHEIGHT), pygame.FULLSCREEN)
        self.screen = pygame.Surface((constant.WIDTH, constant.HEIGHT))
        pygame.display.set_caption("Game")

        self.clock = pygame.time.Clock()
        self.running = True

        self.clockOnScreen = objects.Node(pygame.Vector2((constant.WIDTH - 540)/2, 20))
        self.minuteHand = objects.Hand(pygame.Vector2((constant.WIDTH + 10)/2, (constant.HEIGHT + 120)/2), image.MINUTE, 10, 90)
        self.hourHand = objects.Hand(pygame.Vector2((constant.WIDTH + 22)/2, (constant.HEIGHT + 120)/2), image.HOUR, 22, 7.5)
        self.background = objects.Background()

        self.btn1 = objects.Button(pygame.Vector2(20,200), _text="As")
        self.btn2 = objects.Button(pygame.Vector2(950,200), _text="As2")
        self.btn3 = objects.Button(pygame.Vector2(20,500), _text="As3")
        self.btn4 = objects.Button(pygame.Vector2(950,500), _text="As4")
        self.mouseposX = 0
        self.mouseposY = 0

        self.language = "es"


        self.shuffle = True
        self.correctbtnnumber = random.randint(1,4)
        self.correctbtn = objects.Hour()

        self.otherbtn1 = objects.Hour()
        self.otherbtn2 = objects.Hour() 
        self.otherbtn3 = objects.Hour() 

        self.esbtn = objects.Button(pygame.Vector2(5,5),
                                    image.ES, "",
                                    image.ES, image.ES)
        self.enbtn = objects.Button(pygame.Vector2(100,5),
                                    image.EN, "",
                                    image.EN, image.EN)

        self.goods = 0
        self.goodstext = objects.Text(str(self.goods),
                                      pygame.Vector2(constant.WIDTH-50,10),
                                      constant.GREEN)
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


        self.deltaTime = 0

        self.xoffset = 0
        self.offset = pygame.Vector2(0, 0)
        self.fix = 1
        self.mousepressed = False
    def mainloop(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.FINGERDOWN:
                    self.mousepressed = True

                    if event.type == pygame.FINGERDOWN:
                        self.mouseposX = event.x * constant.WIDTH
                        self.mouseposY = event.y * constant.HEIGHT
                    else:
                        self.mouseposX, self.mouseposY = (0, 0)
                else:
                    self.mousepressed = False
            self.keys = pygame.key.get_pressed()
            self.update()
            self.draw()

            self.deltaTime = self.clock.tick(60) / 1000.0
            pygame.display.update()
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
            while self.otherbtn3.getTuple() == self.correctbtn.getTuple():
                self.otherbtn3.newSet()
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
        
        self.esbtn.update(self.deltaTime, self.mousepressed, self.mouseposX, self.mouseposY, self.fix, self.offset)
        self.enbtn.update(self.deltaTime, self.mousepressed, self.mouseposX, self.mouseposY, self.fix, self.offset)

        if self.esbtn.get_pressed:
            self.language = "es"
            self.esbtn.get_pressed = False
        if self.enbtn.get_pressed:
            self.language = "en"
            self.enbtn.get_pressed = False
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
            sound.BAD.play()
            self.timegood.timing = True
            self.good = 0
            self.erroranimation = True

        if self.ticketanimation:
            if self.timegood.time < .7:
                self.ticketonScreen.position.y -= (constant.HEIGHT + 252) * self.deltaTime / 1.4
            if self.timegood.time > 1.3:
                self.ticketonScreen.position.y += (constant.HEIGHT + 252) * self.deltaTime / 1.4
        
        if self.erroranimation:
            if self.timegood.time < .7:
                self.erroronScreen.position.y -= (constant.HEIGHT + 290) * self.deltaTime / 1.4
            if self.timegood.time > 1.3:
                self.erroronScreen.position.y += (constant.HEIGHT + 290) * self.deltaTime / 1.4
        if self.timegood.timing == False:
            self.ticketonScreen.position.y = constant.HEIGHT
            self.ticketanimation = False
            self.erroronScreen.position.y = constant.HEIGHT
            self.erroranimation = False

            
            
        


        self.screenfix()
        self.timegood.update(self.deltaTime)



    def draw(self):
        self.window.fill((0, 0, 0))
        self.background.draw(self.screen)
        self.clockOnScreen.draw(self.screen)
        self.minuteHand.draw(self.screen)
        self.hourHand.draw(self.screen)
        self.ticketonScreen.draw(self.screen)
        self.erroronScreen.draw(self.screen)
        self.goodstext.draw(self.screen)

        self.btn1.draw(self.screen)
        self.btn2.draw(self.screen)
        self.btn3.draw(self.screen)
        self.btn4.draw(self.screen)

        self.esbtn.draw(self.screen)
        self.enbtn.draw(self.screen)

        self.window.blit(pygame.transform.scale(
            self.screen, (int(constant.WIDTH*self.fix), int(constant.HEIGHT*self.fix))), 
            self.offset)

    def return_angle_by_hour(self, hour, minutes):
        
        self.hourHand.rotation = 360 - ((30 * hour) + (minutes * (30 / 60)))

        if hour == 12:
            self.hourHand.rotation = 360 -(minutes * (30 / 60))

        if minutes == 0:
            minutes = 60
        self.minuteHand.rotation = 360 - (30 * (minutes / 5))

    
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

        

if __name__ == "__main__":
    game = Game()
    game.mainloop()
