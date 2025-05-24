# Example file showing a basic pygame "game loop"
import pygame
import pygame.examples
import pygame.freetype
from wad import *
white = (255, 255, 255)
green = (0, 255, 0)
blue = (0, 0, 128)


# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
font = pygame.font.Font('freesansbold.ttf', 32)

new = WADLoader("data\\DOOM.wad")
new.ReadDirectories()

while running:
    fps = str(clock.get_fps())
    text = font.render(fps, True, green)
    textRect = text.get_rect()
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("purple")
    screen.blit(text, textRect)
    # RENDER YOUR GAME HERE

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(0)  # limits FPS to 60

pygame.quit()