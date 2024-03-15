import pygame
pygame.mixer.init()

#criando dicionario com todas as sprites, para facilitar chama-las nas funções
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
    'tutorial':pygame.transform.scale(pygame.image.load('assets/sprites/tutorial.png'), (500, 800)),
    'coracao':pygame.transform.scale(pygame.image.load('assets/sprites/coracao.png'), (35, 35)),
}
#criando dicionario com todas as musicas, para facilitar chama-las nas funções
efeitos_sonoros = {
    'click_som':pygame.mixer.Sound('assets/click.ogg'),
    'morte_som':pygame.mixer.Sound('assets/morte.ogg'),
    'minecart_som':pygame.mixer.Sound('assets/Minecart.ogg'),
    'wasted_som':pygame.mixer.Sound('assets/wasted.ogg')
}
efeitos_sonoros['minecart_som'].set_volume(0.5) #ajuste de volume
def toggle_som():
    for som in efeitos_sonoros.values():
        if som.get_volume() == 0:
            som.set_volume(1)
        else:
            som.set_volume(0)
