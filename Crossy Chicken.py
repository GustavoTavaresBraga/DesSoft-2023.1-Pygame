import pygame
from init_screen import init_screen
from Pygame import main_loop
from constantes import *

pygame.init()
pygame.mixer.init()

window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Crossy Chicken')

state = INITIAL
while state != END:
    if state == INITIAL:
        state = init_screen(window)
    elif state == PLAYING:
        state = main_loop(window)
    else:
        state = END

# ===========FINALIZAÇÃO DO JOGO==============
# font = pygame.font.SysFont(None, 80)
# game_over = font.render('GAME OVER', True, (255, 0, 0))
# window.blit(game_over, (80, 250))
# pygame.display.update()
# pygame.time.set_timer(pygame.USEREVENT+1, 5000)

pygame.quit()