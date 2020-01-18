import sys
import csv
import numpy as np
from time import monotonic, sleep
import pygame
import numba as nb
from scipy.spatial.distance import squareform, pdist
from matplotlib import cm
hot = cm.get_cmap('hot')

# global constants

HEIGHT = 400
WIDTH = 600

LOOP_MS = 150  # ms per frame

def current_time_millis():
    return round(monotonic() * 1000)

def initialize(num_boids=5):
    pos = np.array(
        [
            [20, 30],
            [40, 50],
            [60, 70],
            [80, 90],
            [80, 110]
        ]
    )
    vel = np.zeros((5, 2))
    return pos, vel

def update_state(dt, pos, vel):
    print("Updating state")
    # update position
    pos = pos + dt * vel
    # bounce off edges
    for j in range(pos.shape[0]):
        if pos[j, 0] < 0:
            pos[j, 0] = 0
            vel[j, 0] *= -1
        if pos[j, 0] > WIDTH:
            pos[j, 0] = WIDTH
            vel[j, 0] *= -1
        if pos[j, 1] < 0:
            pos[j, 1] = 0
            vel[j, 1] *= -1
        if pos[j, 1] > HEIGHT:
            pos[j, 1] = HEIGHT
            vel[j, 1] *= -1
    # update velocity
    distances = pdist(pos)
    print(distances)
    magnitudes = squareform(10/distances**2 - 1/distances**3)
    print(magnitudes)
    sums = magnitudes.sum(axis=0, keepdims=True)
    print(sums)
    print(vel.dot(sums))
    print("Updated state")
    # boid component 1: close
    # 
    # boid component 2: but not too close
    # add repulsion component ~1/r^2
    # boid component 3: cohesion


    return pos, vel

def draw_boids(screen, pos_vector):
    for j in range(pos_vector.shape[0]):
        color = (155,155,155,0.7)
        pygame.draw.rect(screen, color,
            (pos_vector[j, 0], pos_vector[j, 1], 3, 3))
    return


if __name__ == "__main__":
    pygame.init()
    pygame.font.init()
    size = width, height = WIDTH, HEIGHT
    screen = pygame.display.set_mode(size)

    # init game
    pos, vel = initialize()

    running = True

    while True:
        dt = 0.001
        start_time = current_time_millis()
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
            elif event.type == pygame.KEYDOWN:
                print(event.key)
                # if event.key == pygame.K_i: # i
                # if event.key == pygame.K_u: # u
                # if event.key == pygame.K_d: # d
                # if event.key == pygame.K_h: # h
                # if event.key == pygame.K_c: # c
                # if event.key == pygame.K_r: # r
                # if event.key == pygame.K_1: # 1
                # if event.key == pygame.K_2: # 2
                if event.key == pygame.K_p: # pause
                    running = not running
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                print("Mouse position:", x, y)
                for j in range(vel.shape[0]):
                    if pos[j,0] != y:
                        vel[j, 0] += 10*(pos[j, 0] - x)
                    if pos[j, 1] != x:
                        vel[j, 1] += 10*(pos[j, 1] - y)
                print("New velocity:", vel)
                if event.button == 1: # LMB
                    print("LMB")
                else:   # RMB
                    print("RMB")
        if running:
            # update logic
            pos, vel = update_state(dt, pos, vel)
            # draw the boids
            draw_boids(screen, pos)
            pygame.display.flip()
        end_time = current_time_millis()
        duration = end_time - start_time
        time_left = max(0, LOOP_MS - duration)
        sleep(time_left / 1000)
