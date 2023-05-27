import pygame
from telas import TelaInicial
global musica, efeitos

def inicializa():
    """Função que inicializa o jogo e carrega os assets
        Retorna um dicionário com os assets
    """
    pygame.init()
    tela = pygame.display.set_mode((500,800))
    pygame.display.set_caption('Crossy Chicken')
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