import pygame
import sys
import random
from math import *
from button import Button
pause = False

pygame.init()
width = 1400
height = 800
display = pygame.display.set_mode((width, height))
pygame.display.set_caption("Balloon Shooter Game PBL Project")
clock = pygame.time.Clock()


margin = 150
lowerBound = 120
score = 0


white = (230, 230, 230)
lightBlue = (4, 27, 96)
red = (231, 76, 60)
lightGreen = (25, 111, 61)
darkGray = (40, 55, 71)
darkBlue = (64, 178, 239)
green = (35, 155, 86)
yellow = (244, 208, 63)
blue = (46, 134, 193)
purple = (155, 89, 182)
orange = (243, 156, 18)
black = (0,0,0)



font = pygame.font.SysFont("Algerian", 35)

class Balloon:
    
    def __init__(self, speed):
        self.a = random.randint(50, 90)
        self.b = self.a + random.randint(0, 50)
        self.x = random.randrange(margin, width - self.a - margin)
        self.y = height - lowerBound
        self.angle = 200
        self.speed = -speed
        self.proPool= [-1, -1, -1, 0, 0, 0, 2, 2, 2, 2]
        self.length = random.randint(100, 100)
        self.color = random.choice([red, green, purple, orange, yellow, blue, darkGray, darkBlue, lightGreen, lightBlue])
        
    
    def move(self):
        direct = random.choice(self.proPool)

        if direct == -1:
            self.angle += -8
        elif direct == 0:
            self.angle += 2
        else:
            self.angle += 6

        self.y += self.speed*sin(radians(self.angle))
        self.x += self.speed*cos(radians(self.angle))

        if (self.x + self.a > width) or (self.x < 0):
            if self.y > height/5:
                self.x -= self.speed*cos(radians(self.angle)) 
            else:
                self.reset()
        if self.y + self.b < 0 or self.y > height + 3:
            self.reset()
            
    
    def show(self):
        pygame.draw.line(display, black, (self.x + self.a, self.y + 3*self.b), (self.x + self.a/2, self.y + self.b + 2*self.length))
        pygame.draw.ellipse(display, self.color, (self.x, self.y, 3*self.a, 3*self.b))
        pygame.draw.ellipse(display, self.color, (self.x + self.a - 5, self.y + 3*self.b - 8, 10, 10))
            
    
    def burst(self):
        global score
        pos = pygame.mouse.get_pos()

        if isonBalloon(self.x, self.y, 3*self.a, 3*self.b, pos):
            score += 1
            self.reset()
            
    def reset(self):
        self.a = random.randint(30, 40)
        self.b = self.a + random.randint(0, 10)
        self.x = random.randrange(margin, width - self.a - margin)
        self.y = height - lowerBound 
        self.angle = 90
        self.speed -= 0.002
        self.proPool = [-1, -1, -1, 0, 0, 0, 0, 1, 1, 1]
        self.length = random.randint(50, 100)
        self.color = random.choice([red, green, purple, orange, yellow, blue, darkGray, darkBlue, lightGreen, lightBlue])


balloons = []
noBalloon = 10


for i in range(noBalloon):
    obj = Balloon(random.choice([5, 5, 5, 5, 6, 5, 3, 3, 3, 4]))
    balloons.append(obj)


def isonBalloon(x, y, a, b, pos):
    if (x < pos[0] < x + a) and (y < pos[1] < y + b):
        return True
    else:
        return False

    

def pointer():
    pos = pygame.mouse.get_pos()
    r = 25
    l = 20
    color = red
    for i in range(noBalloon):
        if isonBalloon(balloons[i].x, balloons[i].y, balloons[i].a, balloons[i].b, pos):
            color = red
    pygame.draw.ellipse(display, color, (pos[0] - r/2, pos[1] - r/2, r, r), 4)
    pygame.draw.line(display, color, (pos[0], pos[1] - l/2), (pos[0], pos[1] - l), 4)
    pygame.draw.line(display, color, (pos[0] + l/2, pos[1]), (pos[0] + l, pos[1]), 4)
    pygame.draw.line(display, color, (pos[0], pos[1] + l/2), (pos[0], pos[1] + l), 4)
    pygame.draw.line(display, color, (pos[0] - l/2, pos[1]), (pos[0] - l, pos[1]), 4)


def lowerPlatform():
    pygame.draw.rect(display, darkGray, (0, height - lowerBound, width, lowerBound))
    

def showScore():
    scoreText = font.render("Balloons Bursted : " + str(score), True, white)
    display.blit(scoreText, (150, height - lowerBound + 60))
    


font1 = pygame.font.Font('pdark.ttf', 105)
font2 = pygame.font.Font('pdark.ttf', 45)

def is_paused():
    global score
    global pause
    pause=True
    while True:
    
        python = pygame.image.load('pexels-gradienta-7130555.jpg')
        display.blit(python,(0,0))
        PAUSE_MOUSE_POS = pygame.mouse.get_pos()
        CONTINUE_BUTTON = Button(image=pygame.image.load("Continue Rect.jpg"), pos=(690, 290), 
                            text_input="RESUME", font=get_font(80), base_color="#8de0ce", hovering_color="White")
        RESTART_BUTTON = Button(image=pygame.image.load("Restart Rect.jpg"), pos=(690, 440), 
                            text_input="RESTART", font=get_font(80), base_color="#8de0ce", hovering_color="White")
        QUIT_BUTTON = Button(image=pygame.image.load("Quit Rect.png"), pos=(690, 600), 
                            text_input="QUIT", font=get_font(80), base_color="#8de0ce", hovering_color="White")
                    
        for button in [CONTINUE_BUTTON,RESTART_BUTTON,QUIT_BUTTON]:
            button.changeColor(PAUSE_MOUSE_POS)
            button.update(display)

        text = font1.render("PAUSED" ,black,200)
        display.blit(text, (460, 100))

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                    if CONTINUE_BUTTON.checkForInput(PAUSE_MOUSE_POS):
                        game()
                    elif RESTART_BUTTON.checkForInput(PAUSE_MOUSE_POS):
                        score = 0
                        game()
                    elif QUIT_BUTTON.checkForInput(PAUSE_MOUSE_POS):
                        pygame.quit()
                        sys.exit()
            if event.type ==pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game()
                elif event.key == pygame.K_q:
                    pygame.quit()
                    quit()
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
        pygame.display.update()

    
BG = pygame.image.load("Background.png")
def get_font(size):
    return pygame.font.Font("font.ttf", size)   

def close():
    pygame.quit()
    sys.exit()

def main_menu():
    while True:
        display.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(100).render("MAIN MENU", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(680, 100))

        PLAY_BUTTON = Button(image=pygame.image.load("Play Rect.png"), pos=(660, 300), 
                            text_input="PLAY", font=get_font(95), base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = Button(image=pygame.image.load("Quit Rect.png"), pos=(660, 550), 
                            text_input="QUIT", font=get_font(95), base_color="#d7fcd4", hovering_color="White")

        display.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(display)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    game()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()
    


def game():
    
    
    global score
    loop = True
    while loop:
        
        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                close()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    close()
                if event.key == pygame.K_r:
                    score = 0
                    game()
                if event.key == pygame.K_ESCAPE:
                    is_paused()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PAUSE0.checkForInput(GAME_MOUSE_POS):
                    is_paused()
            

            if event.type == pygame.MOUSEBUTTONDOWN:
                for i in range(noBalloon):
                    balloons[i].burst()

        python1 = pygame.image.load('wallpapersden.com_cloudy-field-paint_3840x2160.jpg')
        display.blit(python1,(0,0))
        PAUSE0 = Button(image=pygame.image.load("123-removebg-preview.png"), pos=(40, 38),
                    text_input="PAUSE", font=get_font(1), base_color="#d7fcd4", hovering_color="White")

        GAME_MOUSE_POS = pygame.mouse.get_pos()
        for button in [PAUSE0]:
            button.changeColor(GAME_MOUSE_POS)
            button.update(display)
                
            

        for i in range(noBalloon):
            balloons[i].show()

        pointer()
        
        for i in range(noBalloon):
            balloons[i].move()

        lowerPlatform()
        showScore()
        pygame.display.update()
        clock.tick(60)

main_menu()
