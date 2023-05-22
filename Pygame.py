import pygame
from blocos import Blocos
from chicken import Player
from sprites import *

pygame.init()
tela = pygame.display.set_mode((500, 800))
pygame.display.set_caption('Chicken')
clock = pygame.time.Clock()

blocos = Blocos()
player = Player()
global running
running = True
while running:
    clock.tick(30)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    for i in blocos.blocos:
        tela.blit(i[0], i[1])
    for i in blocos.barcos:
        tela.blit(sprites['barco'], (i[0], i[1]))
    blocos.updateBlocos()
    player.update()
    if player.checarMorte(blocos.blocos, blocos.barcos):
        running = False
    tela.blit(player.image, player.rect)
    pygame.display.update()
pygame.quit()
