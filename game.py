# Example file showing a circle moving on screen
import random
import sys

import pygame

import pymunk
import pymunk.pygame_util
from pymunk import Vec2d


collision_types = {
    "ball": 1,
    "brick": 2,
    "bottom": 3,
    "player": 4,
}

WIDTH = 1280
HEIGHT = 720
wall_thickness = 10


# top and bottom walls
# def draw_walls():
#     top = pygame.draw.line(screen, "white", (0, 0), (WIDTH, 0), wall_thickness)
#     bottom = pygame.draw.line(
#         screen, "white", (0, HEIGHT), (WIDTH, HEIGHT), wall_thickness
#     )
#     wall_list = [top, bottom]
#     return wall_list


def convert_coordinates(point):
    return int(point[0]), int(point[1])


def spawn_ball(space, position, velocity):
    ball_body = pymunk.Body(1, float("inf"))
    ball_body.position = position

    ball_shape = pymunk.Circle(ball_body, 10)
    ball_shape.color = pygame.Color("white")
    ball_shape.elasticity = 1.0
    ball_shape.collision_type = collision_types["ball"]
    ball_body.velocity = velocity

    # ball_body.apply_impulse_at_local_point(Vec2d(*direction))

    # Keep ball velocity at a static value
    def constant_velocity(body, gravity, damping, dt):
        body.velocity = body.velocity.normalized() * 400

    ball_body.velocity_func = constant_velocity

    space.add(ball_body, ball_shape)

    h = space.add_collision_handler(collision_types["player"], collision_types["ball"])
    h.separate = collide


def spawn_paddle(space, x, y, collision_type):

    # Spawn a ball for the player to have something to play with

    brick_body = pymunk.Body(body_type=pymunk.Body.KINEMATIC)
    brick_body.position = x, y
    brick_shape = pymunk.Poly.create_box(brick_body, (20, 100))
    brick_shape.elasticity = 1.0
    brick_shape.color = pygame.Color("white")
    brick_shape.group = 1
    brick_shape.collision_type = collision_types[collision_type]
    space.add(brick_body, brick_shape)


def collide(arbiter, space, data):
    print("collide")
    return True


def main():
    # pygame setup
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    font = pygame.font.SysFont("Arial", 16)
    clock = pygame.time.Clock()
    running = True

    # Ball setup

    firstRun = True

    space = pymunk.Space()
    pymunk.pygame_util.positive_y_is_up = True
    draw_options = pymunk.pygame_util.DrawOptions(screen)

    ball_position = WIDTH / 2, HEIGHT / 2
    rightPaddle_position = WIDTH - 100, HEIGHT / 2
    leftPaddle_position = 100, HEIGHT / 2

    spawn_ball(space, ball_position, Vec2d(5, 0))
    spawn_paddle(space, rightPaddle_position[0], rightPaddle_position[1], "brick")
    # spawn_paddle(space, leftPaddle_position[0], leftPaddle_position[1], "player")
    # draw_walls()

    leftPaddle = pymunk.Body(body_type=pymunk.Body.KINEMATIC)
    leftPaddle.position = leftPaddle_position
    leftPaddle_shape = pymunk.Poly.create_box(leftPaddle, (20, 100))
    leftPaddle.elasticity = 1.0
    leftPaddle.color = pygame.Color("white")
    leftPaddle.group = 1
    leftPaddle.collision_type = collision_types["player"]

    space.add(leftPaddle, leftPaddle_shape)

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

    while running:
        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        # keys = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:

                if event.key == pygame.K_UP:
                    leftPaddle.velocity = (0, 300)
                    print("up")

                elif event.key == pygame.K_DOWN:
                    leftPaddle.velocity = (0, -300)
                    print("down")
            elif event.type == pygame.KEYUP:
                leftPaddle.velocity = (0, 0)

        # fill the screen with a color to wipe away anything from last frame
        screen.fill("black")

        ### Draw stuff
        space.debug_draw(draw_options)

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


if __name__ == "__main__":
    sys.exit(main())
