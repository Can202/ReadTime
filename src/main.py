import pygame
import constant
import image
import objects

pygame.init()

class Game:
    def __init__(self) -> None:

        self.window = pygame.display.set_mode((constant.WIDTH, constant.HEIGHT), pygame.RESIZABLE)
        pygame.display.set_caption("Game")

        self.clock = pygame.time.Clock()
        self.running = True

        self.clockOnScreen = objects.Node(pygame.Vector2((constant.WIDTH - 540)/2, 20))
        self.minuteHand = objects.Hand(pygame.Vector2((constant.WIDTH + 10)/2, (constant.HEIGHT + 120)/2), image.MINUTE, 10, 90)
        self.hourHand = objects.Hand(pygame.Vector2((constant.WIDTH + 22)/2, (constant.HEIGHT + 120)/2), image.HOUR, 22, 7.5)
        self.background = objects.Background()

        self.btn1 = objects.Button(pygame.Vector2(5,200), _text="As")
        self.btn2 = objects.Button(pygame.Vector2(950,200), _text="As2")
        self.btn3 = objects.Button(pygame.Vector2(5,500), _text="As3")
        self.btn4 = objects.Button(pygame.Vector2(950,500), _text="As4")

        self.deltaTime = 0

        self.fix = 1
        self.fixx = 1
        self.fixy = 1
    def mainloop(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            # Your game logic and drawing code go here
            self.keys = pygame.key.get_pressed()
            self.update()
            self.draw()

            self.deltaTime = self.clock.tick(60) / 1000.0
            pygame.display.update()
    def update(self):
        self.background.update(self.deltaTime)
        self.clockOnScreen.update(self.deltaTime)
        self.minuteHand.update(self.deltaTime)
        self.hourHand.update(self.deltaTime)

        self.btn1.update(self.deltaTime)
        self.btn2.update(self.deltaTime)
        self.btn3.update(self.deltaTime)
        self.btn4.update(self.deltaTime)

        self.return_angle_by_hour(7, 45)
        self.screenfix()

    def draw(self):
        self.window.fill((0, 0, 0))
        self.background.draw(self.window, self.fix)
        self.clockOnScreen.draw(self.window, self.fix)
        self.minuteHand.draw(self.window, self.fix)
        self.hourHand.draw(self.window, self.fix)

        self.btn1.draw(self.window, self.fix)
        self.btn2.draw(self.window, self.fix)
        self.btn3.draw(self.window, self.fix)
        self.btn4.draw(self.window, self.fix)

    def return_angle_by_hour(self, hour, minutes):
        if hour == 12:
            hour = 0
        
        self.hourHand.rotation = 360 - ((30 * hour) + (minutes * (30 / 60)))
        self.minuteHand.rotation = 360 - (30 * (minutes / 5))

    
    def screenfix(self):
        self.fix = (self.window.get_height() / constant.HEIGHT)
        self.fixx = (self.window.get_width() / constant.WIDTH)
        self.current_width = self.window.get_width()
        self.current_height = self.window.get_height()
        

if __name__ == "__main__":
    game = Game()
    game.mainloop()
