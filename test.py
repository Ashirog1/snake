import pygame
import time

pygame.init()

DISPLAYSURF = pygame.display.set_mode((400, 300))
pygame.display.set_caption('Memes.')


pygame.mixer.music.load("resources/ding.mp3")
pygame.mixer.music.play()
time.sleep(2)
pygame.mixer.music.stop()
