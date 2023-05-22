import pygame
from os import *
from constantes import *

font = pygame.font.SysFont(None, 60)
start = font.render('START GAME', True, (0, 0, 0))

start_position = (50, 100)

def init_screen(screen):
    clock = pygame.time.Clock()

    running = True
    while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                state = END
            
            if event.type == pygame.KEYUP:
                state = PLAYING
                running = False
        
        screen.fill(0, 0, 0)
        screen.blit(start, start_position)

        pygame.display.flip()
    
    return state