import pygame
from os import path

NOME = 'Crossy Chicken'
WIDTH = 500
HEIGHT = 800

FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

MENU = {'':['START','RANKING','SAIR']}

def init_screen(screen):
    # Variável para o ajuste de velocidade
    clock = pygame.time.Clock()

    # Carrega a fonte padrão do sistema
    font = pygame.font.SysFont(None, 40)

    # Vamos utilizar esta variável para controlar o texto a ser mostrado
    text_index = 0
    game = True
    menu_atual = ''
    item_atual = 0
    while menu_atual != 'Sair' and game:
        menu = MENU[menu_atual]
        # Ajusta a velocidade do jogo.
        clock.tick(FPS)

        # Processa os eventos (mouse, teclado, botão, etc).
        for event in pygame.event.get():

            # Verifica se foi fechado.
            if event.type == pygame.QUIT:
                game = False

            # Verifica se soltou alguma tecla.
            if event.type == pygame.KEYDOWN:
                # Dependendo da tecla, altera o estado do jogador.
                if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                    menu_atual = menu[item_atual]
                if event.key == pygame.K_UP:
                    item_atual -= 1
                    if item_atual < 0:
                        item_atual = 0
                if event.key == pygame.K_DOWN:
                    item_atual += 1
                    if item_atual >= len(menu):
                        item_atual = len(menu) - 1

        # A cada loop, redesenha o fundo e os sprites
        screen.fill(BLACK)

        # Desenha os textos na tela
        # Desenha o título do menu
        text_image = font.render(menu_atual, True, WHITE)
        screen.blit(text_image, (10, 10))
        for i in range(len(menu)):
            text = menu[i]
            if i == item_atual:
                text = '> ' + text
            else:
                text = '  ' + text
            text_image = font.render(text, True, WHITE)
            screen.blit(text_image, (170, 400 + (i + 1) * 16))

        # Depois de desenhar tudo, inverte o display.
        pygame.display.flip()

# Inicialização do Pygame.
pygame.init()
pygame.mixer.init()

# Tamanho da tela.
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Nome do jogo
pygame.display.set_caption(NOME)

# Imprime instruções
print('*' * len(NOME))
print(NOME.upper())
print('*' * len(NOME))
print('Aperte a tecla espaço para avançar para o próximo texto.')

# Comando para evitar travamentos.
try:
    init_screen(screen)
finally:
    pygame.quit()