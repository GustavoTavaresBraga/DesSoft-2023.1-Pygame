import pygame

sprites = {
    'grama': pygame.transform.scale(pygame.image.load('sprites/grama.png'), (50, 50)),
    'agua': pygame.transform.scale(pygame.image.load('sprites/agua.png'), (50, 50)),
    'trilho': pygame.transform.scale(pygame.image.load('sprites/trilho.png'), (50, 50)),
    'barco': pygame.transform.scale(pygame.image.load('sprites/barco.png'), (50, 50)),
    'minecart': pygame.transform.scale(pygame.image.load('sprites/minecart.png'), (50, 50)),
    'chicken':pygame.transform.scale(pygame.image.load('sprites/chicken.png'), (50, 50)),
    'botaoVelocidade':pygame.transform.scale(pygame.image.load('sprites/botaoVelocidade.png'), (400, 40)),
    'botaoNBarcos':pygame.transform.scale(pygame.image.load('sprites/botaoNBarcos.png'), (400, 40)),
    'botaoNMinecarts':pygame.transform.scale(pygame.image.load('sprites/botaoNMinecarts.png'), (400, 40)),
    'botaoEfeitos':pygame.transform.scale(pygame.image.load('sprites/botaoEfeitos.png'), (200, 40)),
    'botaoMusica':pygame.transform.scale(pygame.image.load('sprites/botaoMusica.png'), (200, 40)),
    'ranking':pygame.transform.scale(pygame.image.load('sprites/ranking.png'), (500, 800)),
    'inicio':pygame.transform.scale(pygame.image.load('sprites/inicio.png'), (500, 800)),
    'botaoVB':pygame.transform.scale(pygame.image.load('sprites/botaoVB.png'), (400, 40)),
    'botaoVM':pygame.transform.scale(pygame.image.load('sprites/botaoVM.png'), (400, 40)),
    'botaoVidas':pygame.transform.scale(pygame.image.load('sprites/botaoVidas.png'), (400, 40)),
    'botaoVoltar':pygame.transform.scale(pygame.image.load('sprites/botaoVoltar.png'), (200, 40)),
    'botaoJogar':pygame.transform.scale(pygame.image.load('sprites/botaoJogar.png'), (200, 40)),
}
