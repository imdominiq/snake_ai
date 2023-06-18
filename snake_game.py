import pygame
import random
from enum import Enum
from collections import namedtuple
import numpy as np

pygame.init()
font_size = 24
font = pygame.font.Font(None, font_size)

Point = namedtuple('Point', 'x, y')

BLOCK_SIZE = 20
SPEED = 20
WHITE = (255, 255, 255)
RED = (200, 0, 0)
BLUE1 = (0, 0, 255)
BLUE2 = (0, 100, 255)
BLACK = (0, 0, 0)

x_array = np.array([5, 10, 15, 20, 25, 30, 0, 4, 8, 12, 16, 19, 23, 27, 31, 3, 7, 11, 14, 18])
y_array = np.array([2, 5, 8, 12, 15, 18, 21, 25, 28, 32, 7, 10, 13, 16, 19, 22, 26, 29, 1, 4])

class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4

class SnakeGame:
    def __init__(self, w=640, h=480):
        self.w = w
        self.h = h
        self.display = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption('Snake')
        self.clock = pygame.time.Clock()

        self.direction = Direction.RIGHT
        self.head = Point(self.w / 2, self.h / 2)
        self.snake = [self.head,
                      Point(self.head.x - BLOCK_SIZE, self.head.y),
                      Point(self.head.x - (2 * BLOCK_SIZE), self.head.y)]
        self.score = 0
        self.food = None
        self.x_index = 0
        self.y_index = 0
        self._place__food()

    def _place__food(self):
        x = x_array[self.x_index] * 20
        y = y_array[self.y_index] * 20
        self.food = Point(x, y)
        if self.food in self.snake:
            self.score += 1
            self.x_index = (self.x_index + 1) % len(x_array)
            self.y_index = (self.y_index + 1) % len(y_array)
            self.snake.append(self.food)
            self._place__food()

    def play_step(self):
        # Collect the user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.direction = Direction.LEFT
                elif event.key == pygame.K_RIGHT:
                    self.direction = Direction.RIGHT
                elif event.key == pygame.K_UP:
                    self.direction = Direction.UP
                elif event.key == pygame.K_DOWN:
                    self.direction = Direction.DOWN

        # Move
        self._move(self.direction)
        self.snake.insert(0, self.head)

        # Check if game over
        game_over = False
        if self._is_collision():
            game_over = True
            return game_over, self.score

        # Place new food or just move
        if self.head == self.food:
            self.score += 1
            self.x_index = (self.x_index + 1) % len(x_array)
            self.y_index = (self.y_index + 1) % len(y_array)
            self.snake.append(self.food)
            self._place__food()
        else:
            self.snake.pop()

        # Update UI and clock
        self._update_ui()
        self.clock.tick(SPEED)

        # Return game over and display score
        return game_over, self.score

    def _update_ui(self):
        self.display.fill(BLACK)
        for pt in self.snake:
            pygame.draw.rect(self.display, BLUE1, pygame.Rect(pt.x, pt.y, BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(self.display, BLUE2, pygame.Rect(pt.x + 4, pt.y + 4, 12, 12))
        pygame.draw.rect(self.display, RED, pygame.Rect(self.food.x, self.food.y, BLOCK_SIZE, BLOCK_SIZE))
        text = font.render("Score: " + str(self.score), True, WHITE)
        self.display.blit(text, [0, 0])
        pygame.display.flip()

    def _move(self, direction):
        x = self.head.x
        y = self.head.y
        if direction == Direction.RIGHT:
            x += BLOCK_SIZE
        elif direction == Direction.LEFT:
            x -= BLOCK_SIZE
        elif direction == Direction.DOWN:
            y += BLOCK_SIZE
        elif direction == Direction.UP:
            y -= BLOCK_SIZE
        self.head = Point(x, y)

    def _is_collision(self):
        if (
            self.head.x > self.w - BLOCK_SIZE
            or self.head.x < 0
            or self.head.y > self.h - BLOCK_SIZE
            or self.head.y < 0
        ):
            return True
        if self.head in self.snake[1:]:
            return True
        return False


if __name__ == "__main__":
    game = SnakeGame()

    # Game loop
    while True:
        game_over, score = game.play_step()
        if game_over:
            break
    print('Final Score:', score)

    pygame.quit()
