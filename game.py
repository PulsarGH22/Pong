# Example file showing a circle moving on screen
import pygame
from pygame.locals import *

# Import randint method random module
from random import randint

# pygame setup
pygame.init()

WIDTH = 1280
HEIGHT = 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
running = True
dt = 0
# Creating a variable for direction
direction = 1
# Ball setup
ball_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
# speed = [6, 9]
firstRun = True

leftTurn = False
rightTurn = True


playerPos = pygame.Vector2(10, 320)

wall_thickness = 10

#creating objects
paddle = pygame.image.load("paddle.png").convert_alpha()
ball = pygame.image.load("ball.png").convert_alpha()
leftPaddle_rect = paddle.get_rect()
ball_rect = ball.get_rect()
paddle_mask = pygame.mask.from_surface(paddle)
ball_mask = pygame.mask.from_surface(ball)


#top and bottom walls
def draw_walls():
    top = pygame.draw.line(screen,'white',(0,0),(WIDTH,0),wall_thickness)
    bottom = pygame.draw.line(screen,'white',(0,HEIGHT),(WIDTH,HEIGHT),wall_thickness)
    wall_list = [top,bottom]
    return wall_list

class Ball:
    def __init__(self, position, radius, color, x_speed,y_speed):
        self.position=position
        self.radius=radius
        self.color=color
        self.x_speed=x_speed
        self.y_speed=y_speed
        self.circle =''

    def draw(self):
        self.circle = pygame.draw.circle(screen, self.color,self.position,self.radius)

class Paddle:
    def __init__(self, x_pos, y_pos, color, y_speed):
        self.x_pos=x_pos
        self.y_pos=y_pos
        self.color=color
        self.y_speed=y_speed
        self.paddle =''

    def draw(self):
        self.paddle = screen.blit(paddle, (self.x_pos,self.y_pos))

ball = Ball(ball_pos,10,"white",1,0)
newleftPaddle = Paddle(screen.get_width() - 50, screen.get_height() / 2, "white",0)
newrightPaddle = Paddle(50, screen.get_height() / 2, "white",0)

draw_walls()

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("black")
    

    # pygame.draw.rect(screen, "white", leftRect)
    # pygame.draw.rect(screen, "white", rightRect)
    # circle = pygame.draw.circle(screen, "white", ball_pos, 10)

    ball.draw()
    newleftPaddle.draw()
    newrightPaddle.draw()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        newleftPaddle.y_pos -= 300 * dt
    if keys[pygame.K_s]:
        newleftPaddle.y_pos += 300 * dt


    #collision detection
    if (ball.position.x == newrightPaddle.x_pos) or (ball.position.x == newleftPaddle.x_pos):
        ball.position *=-1


    # if rightTurn:
    #     ball_pos[0] += 5
    # elif leftTurn:
    #     ball_pos[0] -= 5

    # collideRight = rightRect.colliderect(circle)
    # collideLeft = leftRect.colliderect(circle)

    # if collideRight:
    #     leftTurn = True
    #     rightTurn = False

    # elif collideLeft:
    #     leftTurn = False
    #     rightTurn = True

    # pygame.draw.circle(screen, "white", ball_pos, 10)
    pygame.display.update()

    if firstRun == True:
        pygame.time.delay(2000)
        firstRun = False

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()
