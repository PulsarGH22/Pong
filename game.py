# Example file showing a circle moving on screen
import pygame
from pygame.locals import *

import pymunk

import random

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
# ball_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
# speed = [6, 9]
firstRun = True

leftTurn = False
rightTurn = True


# playerPos = pygame.Vector2(10, 320)

wall_thickness = 10

# creating objects

paddleImage = pygame.image.load("paddle.png")
ballImage = pygame.image.load("ball.png")
paddle = paddleImage.convert_alpha()
ball = ballImage.convert_alpha()
Paddle_rect = paddle.get_rect()
ball_rect = ball.get_rect()
paddle_mask = pygame.mask.from_surface(paddle)
ball_mask = pygame.mask.from_surface(ball)

space = pymunk.space()


# top and bottom walls
def draw_walls():
    top = pygame.draw.line(screen, "white", (0, 0), (WIDTH, 0), wall_thickness)
    bottom = pygame.draw.line(
        screen, "white", (0, HEIGHT), (WIDTH, HEIGHT), wall_thickness
    )
    wall_list = [top, bottom]
    return wall_list


def convert_coordinates(point):
    return int(point[0]), 600 - int(point[1])


class Ball:
    def __init__(self, x, y):
        self.body = pymunk.Body()
        self.body.position = x, y
        self.body.velocity = (100, 0)
        self.shape = pymunk.Circle(self.body, 10)
        self.collision_type = 1
        space.add(self.body, self.shape, convert_coordinates(self))

    def draw(self):
        # self.circle = pygame.draw.circle(
        #     screen, self.color, (self.x_pos, self.y_pos), self.radius
        # )

        pygame.draw.circle(
            screen,
            "white",
        )


class Paddle:
    def __init__(self, x_pos, y_pos, color, direction):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.color = color
        self.direction = direction
        # self.y_speed = y_speed
        self.paddle = ""

    def draw(self):
        self.paddle = screen.blit(paddle, (self.x_pos, self.y_pos))


ball = Ball(screen.get_width() / 2, screen.get_width() / 2, 10, "white", 1, 0)
newleftPaddle = Paddle(100, HEIGHT / 2, "white", 1)
newrightPaddle = Paddle(WIDTH - 100, HEIGHT / 2, "white", 1)

draw_walls()

x_pos, y_pos = (5, 0)


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
    newrightPaddle.draw()
    newleftPaddle.draw()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        newleftPaddle.y_pos -= 300 * dt
    if keys[pygame.K_s]:
        newleftPaddle.y_pos += 300 * dt

    # collision detection
    if ball_rect.colliderect(Paddle_rect):
        ball.direction *= -1

    if rightTurn:
        ball.x_pos += x_pos
        ball.y_pos += y_pos
    elif leftTurn:
        ball.x_pos -= x_pos
        ball.y_pos -= y_pos

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
