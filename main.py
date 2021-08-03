import pygame
from pygame.locals import *
import time
import random

SIZE = 40
BACKGROUND_COLOR = (110, 110, 5)
SURFACE_HEIGHT = 800
SURFACE_WIDTH = 1000


class Apple:
    def __init__(self, screen):
        self.image = pygame.image.load('resources/apple.jpg').convert()
        self.x = SIZE * 3
        self.y = SIZE * 3
        self.screen = screen

    def draw(self):
        """
        draw an apple in (x, y)
        :return: None
        """
        self.screen.blit(self.image, (self.x, self.y))
        pygame.display.flip()

    def move(self):
        """
        change the position to random position
        :return: None
        """
        self.x = random.randint(0, 24) * SIZE
        self.y = random.randint(0, 19) * SIZE


class Snake:
    def __init__(self, screen, length=1):
        self.screen = screen
        self.image = pygame.image.load("resources/block.jpg").convert()
        self.x = [SIZE] * length
        self.y = [SIZE] * length
        self.direction = "down"
        self.length = length

    def move_left(self):
        self.direction = 'left'

    def move_right(self):
        self.direction = 'right'

    def move_up(self):
        self.direction = 'up'

    def move_down(self):
        self.direction = 'down'

    def draw(self):
        """
        draw a snake
        :return: None
        """
        self.screen.fill(BACKGROUND_COLOR)
        for i in range(self.length):
            self.screen.blit(self.image, (self.x[i], self.y[i]))
        pygame.display.flip()

    def walk(self):
        """
        snake move to follow to direction
        :return: None
        """
        for i in range(self.length - 1, 0, -1):
            self.x[i] = self.x[i - 1]
            self.y[i] = self.y[i - 1]

        if self.direction == 'up':
            self.y[0] -= SIZE
        elif self.direction == 'down':
            self.y[0] += SIZE
        elif self.direction == 'right':
            self.x[0] += SIZE
        elif self.direction == 'left':
            self.x[0] -= SIZE
        self.draw()

    def increase_length(self):
        """

        :return: None
        """
        self.length += 1
        self.x.append(-1)
        self.y.append(-1)


class Game:
    def __init__(self):
        pygame.init()
        self.surface = pygame.display.set_mode((SURFACE_WIDTH, SURFACE_HEIGHT))
        self.surface.fill(BACKGROUND_COLOR)
        self.snake = Snake(self.surface)
        self.snake.draw()
        self.apple = Apple(self.surface)

    def is_collision(self, x1, y1, x2, y2):
        if x2 <= x1 < x2 + SIZE:
            if y2 <= y1 < y2 + SIZE:
                return True
        return False

    def play(self):
        self.snake.walk()
        self.apple.draw()
        self.display_score()
        pygame.display.flip()

        # snake eating apple
        if self.is_collision(self.snake.x[0], self.snake.y[0], self.apple.x, self.apple.y):
            # sound = pygame.mixer.Sound("resources/ding.mp3")
            # sound.play()
            self.snake.increase_length()
            self.apple.move()
        # snake colliding with itself
        for i in range(3, self.snake.length):
            if self.is_collision(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]):
                raise Exception("game over")
        # snake outside the board
        if self.snake.x[0] < 0 or self.snake.y[0] < 0 or \
                self.snake.x[0] > SURFACE_WIDTH - SIZE or self.snake.y[0] > SURFACE_HEIGHT - SIZE:
            raise Exception("game over")

    def render_background(self):
        bg = pygame.image.load("resources/background.jpg")
        self.surface.blit(bg, (0, 0))

    def show_game_over(self):
        self.surface.fill(BACKGROUND_COLOR)
        font = pygame.font.SysFont('arial', 30)
        line1 = font.render(f"Game is over! Your score is: {self.snake.length}", True, (255, 255, 255))
        self.surface.blit(line1, (200, 300))
        line2 = font.render(f"To play again press Enter, To exit press Escape", True, (255, 255, 255))
        self.surface.blit(line2, (200, 360))
        pygame.display.flip()

    def display_score(self):
        font = pygame.font.SysFont('arial', 30)
        score = font.render(f"Score: {self.snake.length}", True, (255, 255, 255))
        self.surface.blit(score, (800, 10))

    def reset_game(self):
        self.snake = Snake(self.surface)
        self.apple = Apple(self.surface)

    def run(self):
        """
        just run the game
        :return: None
        """
        running = True
        pause = False

        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False
                    if event.key == K_RETURN:
                        pause = False
                    if not pause:
                        if event.key == K_UP:
                            self.snake.move_up()

                        if event.key == K_DOWN:
                            self.snake.move_down()

                        if event.key == K_LEFT:
                            self.snake.move_left()

                        if event.key == K_RIGHT:
                            self.snake.move_right()

                elif event.type == QUIT:
                    running = False
            try:
                if not pause:
                    self.play()
            except Exception:
                self.show_game_over()
                pause = True
                self.reset_game()

            time.sleep(0.2)


if __name__ == "__main__":
    game = Game()
    game.run()
