'''
This script train a ML model to play snake.
Tutorial: https://www.youtube.com/watch?v=--nsd2ZeYvs&list=PLqnslRFeH2UpKIaGsA3IBhblk3F7aHsvX&index=3

'''
import pygame
import random
import numpy as np
from enum import Enum
from collections import namedtuple  # assigns a meaning for each position in a tuple
pygame.init() # Init pygame modules

####################################################################################################
# Constants
####################################################################################################
font = pygame.font.SysFont('arial.ttf', 25)
Point = namedtuple('Point', 'x, y')
BLOCK_SIZE = 20
STARTING_SPEED = 40
SPEED_INCREASE = 0

# RGB Colors
WHITE = (255, 255, 255)
RED = (200, 0, 0)
BLUE1 = (0, 0, 255)
BLUE2 = (0, 100, 255)
BLACK = (0, 0, 0)

# Agent Class
# reset
# play (action) -> direction
# game_iteration
# is_collision

####################################################################################################
# Class Definitions
####################################################################################################
class Direction(Enum):
    """Enum representing the direction of the snake"""
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4

class SnakeGameAI:
    def __init__(self, w:int=640, h:int=480) -> None:
        self.w = w
        self.h = h
        self.clock = pygame.time.Clock()
        self.speed = STARTING_SPEED

        # Init display
        self.display = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption('Snake!')

        # Reset
        self.reset()

    def reset(self):
        # Init game state
        self.direction = Direction.RIGHT
        self.head = Point(self.w/2, self.h/2)
        self.snake = [self.head, 
                      Point(self.head.x-BLOCK_SIZE, self.head.y),
                      Point(self.head.x-(2*BLOCK_SIZE), self.head.y)]  # snake = 3 blocks
        self.score = 0
        self.food = None
        self._place_food()
        self.frame_iteration = 0

    def _place_food(self):
        """Place food on the map in increments of BLOCK_SIZE"""
        x = random.randint(0, (self.w-BLOCK_SIZE )//BLOCK_SIZE )*BLOCK_SIZE
        y = random.randint(0, (self.h-BLOCK_SIZE )//BLOCK_SIZE )*BLOCK_SIZE
        self.food = Point(x,y)

        # Recreate food if in snake
        if self.food in self.snake:
            self._place_food()


    def play_step(self, action):
        self.frame_iteration += 1

        # 1. Quit?
        for event in pygame.event.get():
            # check quit
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        # 2. Move
        self._move(action)  # update head
        self.snake.insert(0, self.head)  # insert new head

        # 3. Check if game over
        reward = 0
        game_over = False
        if self.is_collision() or self.frame_iteration > 100*len(self.snake):
            game_over = True
            reward = -10
            return reward, game_over, self.score

        # 4. Place new food or move
        if self.head == self.food:
            self.score += 1
            self.speed += SPEED_INCREASE
            reward = 10
            self._place_food()
        else:
            self.snake.pop()  # remove last element of the snake

        # 5. Update pygame ui and clock
        self._update_ui()
        self.clock.tick(self.speed)

        # 6. return game over and score
        return reward, game_over, self.score
    
    def is_collision(self, pt=None):
        # hits boundary
        if pt is None:
            pt = self.head

        if pt.x > self.w - BLOCK_SIZE or pt.x < 0 or \
           pt.y > self.h - BLOCK_SIZE or pt.y < 0:
            return True
        
        # hits itself
        if pt in self.snake[1:]:
            return True
        
        # no collision
        return False
    
    def _update_ui(self):
        self.display.fill(BLACK)

        # draw snake
        for pt in self.snake:
            pygame.draw.rect(self.display, BLUE1, pygame.Rect(pt.x, pt.y, BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(self.display, BLUE2, pygame.Rect(pt.x+4, pt.y+4, 12, 12))  # highlight

        # draw food
        pygame.draw.rect(self.display, RED, pygame.Rect(self.food.x, self.food.y, 
                                                        BLOCK_SIZE, BLOCK_SIZE))

        # draw score
        text = font.render('Score: {}'.format(self.score), True, WHITE)
        self.display.blit(text, [0,0])

        # update the display
        pygame.display.flip()

    def _move(self, action):
        clock_wise = [Direction.RIGHT, Direction.DOWN, Direction.LEFT, Direction.UP]
        idx = clock_wise.index(self.direction)
        
        # action = [straight, right, left]
        if np.array_equal(action, [1,0,0]):
            new_dir = clock_wise[idx]  # no change
        elif np.array_equal(action, [0,1,0]):
            next_idx = (idx+1) % 4  # mod divide to account for the end
            new_dir = clock_wise[next_idx]  # right turn r->d->l->u
        else:  # [0,0,1]
            next_idx = (idx-1) % 4  # 
            new_dir = clock_wise[next_idx]  # left turn r->u->l->d

        self.direction = new_dir

        x = self.head.x
        y = self.head.y
        if self.direction == Direction.RIGHT:
            x += BLOCK_SIZE
        elif self.direction == Direction.LEFT:
            x -= BLOCK_SIZE
        elif self.direction == Direction.UP:
            y -= BLOCK_SIZE
        elif self.direction == Direction.DOWN:
            y += BLOCK_SIZE

        # update head
        self.head = Point(x,y)