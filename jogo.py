import pygame
from telas import TelaInicial
import random

def inicializa():
    """Função que inicializa o jogo e carrega os assets
        Retorna um dicionário com os assets
    """
    pygame.init()
    pygame.mixer.init()
    tela = pygame.display.set_mode((500,800))
    pygame.display.set_caption('Crossy Chicken')
    musica = random.choice(['assets/sweden.mp3', 'assets/AriaMath.mp3'])
    pygame.mixer_music.load(musica)
    pygame.mixer_music.set_volume(0.4)
    pygame.mixer_music.play()
    return tela

def game_loop():
    """Função que inicializa o jogo e chama as telas
        Caso a tela seja trocada, a função chama a nova tela
    """
    tela = inicializa()
    tela_atual = TelaInicial(tela)
    while tela_atual.update(): 
        tela_atual = tela_atual.troca_tela()
        tela_atual.desenha()
        
game_loop()