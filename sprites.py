import pygame

sprites = {
    'grama': pygame.transform.scale(pygame.image.load('sprites/grama.png'), (50, 50)),
    'agua': pygame.transform.scale(pygame.image.load('sprites/agua.png'), (50, 50)),
    'trilho': pygame.transform.scale(pygame.image.load('sprites/trilho.png'), (50, 50)),
    'barco': pygame.transform.scale(pygame.image.load('sprites/barco.png'), (50, 50)),
    'minecart': pygame.transform.scale(pygame.image.load('sprites/minecart.png'), (50, 50)),
    'zumbi': pygame.transform.scale(pygame.image.load('sprites/zumbi.png'), (50, 100)),
}
