import pygame
import random
from chicken import Player
from funcoes import *

def game(window):
    pygame.init()
    clock = pygame.time.Clock()
    window = pygame.display.set_mode((500, 800)) # criar uma tela retangular
    pygame.display.set_caption('Crossy Chicken') # título da janela
    grid = [generate_row() for _ in range((800 // 50) + 2)]
    scroll = 0 

    running = True
    player = Player()
    while running:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        scroll += 1
        if scroll >= 50:
            # remover a ultima linha e adicionar uma nova
            grid.pop(0)
            grid = grid[::-1]
            grid.append(generate_row())
            grid.append(generate_row())
            grid = grid[::-1]
            scroll = 0 
        desenharTela(window, grid, scroll)
        player.update()
        window.blit(player.image, player.rect)

        pygame.display.flip()
    pygame.quit()
