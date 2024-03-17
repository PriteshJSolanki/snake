'''
This script implements a simple snake game using pygame.
Tutorial: https://www.youtube.com/watch?v=--nsd2ZeYvs&list=PLqnslRFeH2UpKIaGsA3IBhblk3F7aHsvX&index=3

'''
import pygame
import random
from enum import Enum
from collections import namedtuple  # assigns a meaning for each position in a tuple

# Init pygame modules
pygame.init()
font = pygame.font.SysFont('arial.ttf', 25)
Point = namedtuple('Point', 'x, y')
BLOCK_SIZE = 20
STARTING_SPEED = 10

# RGB Colors
WHITE = (255, 255, 255)
RED = (200, 255, 255)
BLUE1 = (0, 0, 255)
BLUE2 = (0, 100, 255)
BLACK = (0, 0, 0)

class Direction(Enum):
    """Enum representing the direction of the snake"""
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4

class SnakeGame:
    def __init__(self, w:int=640, h:int=480) -> None:
        self.w = w
        self.h = h
        self.clock = pygame.time.Clock()
        self.speed = STARTING_SPEED

        # Init display
        self.display = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption('Snake!')

        # Init game state
        self.direction = Direction.RIGHT
        self.head = Point(self.w/2, self.h/2)
        self.snake = [self.head, 
                      Point(self.head.x-BLOCK_SIZE, self.head.y),
                      Point(self.head.x-(2*BLOCK_SIZE), self.head.y)]  # creates a snake 3 block lengths in size
        self.score = 0
        self.food = None
        self._place_food()

    def _place_food(self):
        """Place food on the map in increments of BLOCK_SIZE"""
        x = random.randint(0, (self.w-BLOCK_SIZE )//BLOCK_SIZE )*BLOCK_SIZE
        y = random.randint(0, (self.h-BLOCK_SIZE )//BLOCK_SIZE )*BLOCK_SIZE
        self.food = Point(x,y)

        # Recreate food if in snake
        if self.food in self.snake:
            self._place_food()

    def _update_ui(self):
        self.display.fill(BLACK)

        # draw snake
        for pt in self.snake:
            pygame.draw.rect(self.display, BLUE1, pygame.Rect(pt.x, pt.y, BLOCK_SIZE, BLOCK_SIZE))  # base blocks
            pygame.draw.rect(self.display, BLUE2, pygame.Rect(pt.x+4, pt.y+4, 12, 12))  # highlighted blocks

        # draw food
        pygame.draw.rect(self.display, RED, pygame.Rect(self.food.x, self.food.y, BLOCK_SIZE, BLOCK_SIZE))

        # draw score
        text = font.render('Score: {}'.format(self.score), True, WHITE)
        self.display.blit(text, [0,0])

        # update the display
        pygame.display.flip()

    def _move(self, direction:Direction):
        x = self.head.x
        y = self.head.y

        if direction == Direction.RIGHT:
            x += BLOCK_SIZE
        elif direction == Direction.LEFT:
            x -= BLOCK_SIZE
        elif direction == Direction.UP:
            y -= BLOCK_SIZE
        elif direction == Direction.DOWN:
            y += BLOCK_SIZE

        # update head
        self.head = Point(x,y)
            

    def _update_speed(self, increment:int):
        SPEED += increment

    def _is_collision(self):
        # hits boundary
        if self.head.x > self.w - BLOCK_SIZE or self.head.x < 0 or self.head.y > self.h - BLOCK_SIZE or self.head.y < 0:
            return True
        
        # hits itself
        if self.head in self.snake[1:]:
            return True
        
        # no collision
        return False

    def play_step(self):
        # 1. collect user input
        for event in pygame.event.get():
            # check quit
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            # check keypress
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.direction = Direction.LEFT
                elif event.key == pygame.K_RIGHT:
                    self.direction = Direction.RIGHT
                elif event.key == pygame.K_UP:
                    self.direction = Direction.UP
                elif event.key == pygame.K_DOWN:
                    self.direction = Direction.DOWN

        # 2. move
        self._move(self.direction)  # update head
        self.snake.insert(0, self.head)  # insert new head

        # 3. check if game over
        game_over = False
        if self._is_collision():
            game_over = True
            return game_over, self.score

        # 4. place new food or just move
        if self.head == self.food:
            self.score += 1
            self._place_food()
            self.speed += 1  # increase speed
        else:
            self.snake.pop()  # remove last element of the snake

        # 5. update pygame ui and clock
        self._update_ui()
        self.clock.tick(self.speed)

        # 6. return game over and score
        return game_over, self.score


if __name__ == '__main__':
    game = SnakeGame()

    # Start game
    while True:
        game_over, score = game.play_step()

        if game_over == True:
            break    

    # exit
    print('Final Score: {}'.format(score))
    pygame.quit()
