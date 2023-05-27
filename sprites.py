import pygame

sprites = {
    'grama': pygame.transform.scale(pygame.image.load('assets/sprites/grama.png'), (50, 50)),
    'agua': pygame.transform.scale(pygame.image.load('assets/sprites/agua.png'), (50, 50)),
    'trilho': pygame.transform.scale(pygame.image.load('assets/sprites/trilho.png'), (50, 50)),
    'barco': pygame.transform.scale(pygame.image.load('assets/sprites/barco.png'), (50, 50)),
    'minecart': pygame.transform.scale(pygame.image.load('assets/sprites/minecart.png'), (50, 50)),
    'chicken':pygame.transform.scale(pygame.image.load('assets/sprites/chicken.png'), (50, 50)),
    'botaoVelocidade':pygame.transform.scale(pygame.image.load('assets/sprites/botaoVelocidade.png'), (400, 40)),
    'botaoNBarcos':pygame.transform.scale(pygame.image.load('assets/sprites/botaoNBarcos.png'), (400, 40)),
    'botaoNMinecarts':pygame.transform.scale(pygame.image.load('assets/sprites/botaoNMinecarts.png'), (400, 40)),
    'botaoEfeitos':pygame.transform.scale(pygame.image.load('assets/sprites/botaoEfeitos.png'), (200, 40)),
    'botaoMusica':pygame.transform.scale(pygame.image.load('assets/sprites/botaoMusica.png'), (200, 40)),
    'ranking':pygame.transform.scale(pygame.image.load('assets/sprites/ranking.png'), (500, 800)),
    'inicio':pygame.transform.scale(pygame.image.load('assets/sprites/inicio.png'), (500, 800)),
    'botaoVB':pygame.transform.scale(pygame.image.load('assets/sprites/botaoVB.png'), (400, 40)),
    'botaoVM':pygame.transform.scale(pygame.image.load('assets/sprites/botaoVM.png'), (400, 40)),
    'botaoVidas':pygame.transform.scale(pygame.image.load('assets/sprites/botaoVidas.png'), (400, 40)),
    'botaoVoltar':pygame.transform.scale(pygame.image.load('assets/sprites/botaoVoltar.png'), (200, 40)),
    'botaoJogar':pygame.transform.scale(pygame.image.load('assets/sprites/botaoJogar.png'), (200, 40)),
}
