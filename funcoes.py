import random
import pygame

sprites = {
    'grama': pygame.transform.scale(pygame.image.load('sprites/grama.png'), (50, 50)),
    'agua': pygame.transform.scale(pygame.image.load('sprites/agua.png'), (50, 50)),
    'trilho': pygame.transform.scale(pygame.image.load('sprites/trilho.png'), (50, 50)),
}
# função para gerar uma fileira aleatória
def generate_row():
    tile = random.choice(['grama', 'agua', 'trilho'])
    return [tile] * 10
#desenhar o fundo
def desenharTela(tela, grid, scroll):
    tela.fill((0, 0, 0))
    for i, row in enumerate(grid):
        for j, tile in enumerate(row):
            sprite = sprites[tile]
            x = j * 50
            y = i * 50 + scroll - 100 
            tela.blit(sprite, (x, y))