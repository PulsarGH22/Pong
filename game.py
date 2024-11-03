# Example file showing a circle moving on screen
import pygame
from pygame.locals import *
import pymunk.pygame_util
from pymunk import Vec2d

import pymunk

import random

# pygame setup
pygame.init()

WIDTH = 1280
HEIGHT = 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
running = True

# Ball setup

firstRun = True


wall_thickness = 10


space = pymunk.Space()
pymunk.pygame_util.positive_y_is_up = True
draw_options = pymunk.pygame_util.DrawOptions(screen)

collision_types = {
    "ball": 1,
    "brick": 2,
    "bottom": 3,
    "player": 4,
}


def pre_solve(arbiter, space, data):
    # We want to update the collision normal to make the bounce direction
    # dependent of where on the paddle the ball hits. Note that this
    # calculation isn't perfect, but just a quick example.
    set_ = arbiter.contact_point_set
    if len(set_.points) > 0:
        player_shape = arbiter.shapes[0]
        width = (player_shape.b - player_shape.a).x
        delta = (player_shape.body.position - set_.points[0].point_a).x
        normal = Vec2d(0, 1).rotated(delta / width / 2)
        set_.normal = normal
        set_.points[0].distance = 0
    arbiter.contact_point_set = set_
    return True


h = space.add_collision_handler(collision_types["player"], collision_types["ball"])
h.pre_solve = pre_solve


# top and bottom walls
def draw_walls():
    top = pygame.draw.line(screen, "white", (0, 0), (WIDTH, 0), wall_thickness)
    bottom = pygame.draw.line(
        screen, "white", (0, HEIGHT), (WIDTH, HEIGHT), wall_thickness
    )
    wall_list = [top, bottom]
    return wall_list


def convert_coordinates(point):
    return int(point[0]), 720 - int(point[1])


class Ball:
    def __init__(self, x, y):
        self.body = pymunk.Body()
        self.body.position = x, y
        self.body.velocity = (200, 0)
        self.shape = pymunk.Circle(self.body, 10)
        self.collision_type = collision_types["ball"]
        self.shape.elasticity = 1
        self.shape.density = 1
        space.add(self.body, self.shape)

    # Keep ball velocity at a static value
    def constant_velocity(body, gravity, damping, dt):
        body.velocity = body.velocity.normalized() * 400

    def draw(self):
        pygame.draw.circle(screen, "white", convert_coordinates(self.body.position), 10)


class Paddle:
    def __init__(self, x, y):
        self.body = pymunk.Body(body_type=pymunk.Body.KINEMATIC)
        self.body.position = x, y
        self.shape = pymunk.Poly.create_box(self.body, (20, 10))
        self.shape.color = Color("white")
        self.shape.group = 1
        self.collision_type = collision_types["player"]
        self.shape.elasticity = 1.0
        space.add(self.body, self.shape)


h = space.add_collision_handler(collision_types["brick"], collision_types["ball"])

ball = Ball(WIDTH / 2, HEIGHT / 2)
newleftPaddle = Paddle(100, HEIGHT / 2)
newrightPaddle = Paddle(WIDTH - 100, HEIGHT / 2)

draw_walls()


# print(newleftPaddle.shape.color)

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
        newleftPaddle.body.position = (0, -300)
    if keys[pygame.K_s]:
        newleftPaddle.body.position = (0, 300)

    pygame.display.flip()

    if firstRun == True:
        pygame.time.delay(2000)
        firstRun = False

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    fps = 60
    dt = 1.0 / fps
    space.step(dt)
    clock.tick(fps)

pygame.quit()
