import pygame
from os import *
from constantes import *
from sprites import *

def init_screen(screen):

    start_position = (180, 280)

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
        
        screen.fill((0, 0, 0))
        screen.blit(sprites['start'], start_position)

        pygame.display.flip()
    
    return state