# Example file showing a circle moving on screen
import pygame
from pygame.locals import *

# Import randint method random module
from random import randint

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
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

leftRect = pygame.Rect(10, 320, 30, 100)
rightRect = pygame.Rect(1240, 320, 30, 100)

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("black")

    pygame.draw.rect(screen, "white", leftRect)
    pygame.draw.rect(screen, "white", rightRect)
    circle = pygame.draw.circle(screen, "white", ball_pos, 10)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        leftRect.y -= 300 * dt
    if keys[pygame.K_s]:
        leftRect.y += 300 * dt

    if rightTurn:
        ball_pos[0] += 5
    elif leftTurn:
        ball_pos[0] -= 5

    collideRight = rightRect.colliderect(circle)
    collideLeft = leftRect.colliderect(circle)

    if collideRight:
        leftTurn = True
        rightTurn = False

    elif collideLeft:
        leftTurn = False
        rightTurn = True

    pygame.draw.circle(screen, "white", ball_pos, 10)
    pygame.display.update()

    if firstRun == True:
        pygame.time.delay(2000)
        firstRun = False

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()
