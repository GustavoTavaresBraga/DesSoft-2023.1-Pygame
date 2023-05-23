import pygame
import random
from sprites import sprites
from chicken import Player
class TelaInicial():
    def __init__(self, tela):
        self.tela = tela
        self.fundo = pygame.transform.scale((pygame.image.load('sprites/inicio.png').convert_alpha()), (500, 800))
        self.botaoPlay = pygame.Rect(55, 405, 425, 40)
        self.botaoRanking = pygame.Rect(55, 460, 425, 40)
        self.botaoSair = pygame.Rect(55, 510, 425, 40)
        self.play = False
        self.ranking = False
    def desenha(self):
        self.tela.fill((255, 255, 255))
        self.tela.blit(self.fundo, (0, 0))
        pygame.display.update()

    def update(self):

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left mouse button click
                mouse_x, mouse_y = event.pos
                if self.botaoPlay.collidepoint(mouse_x, mouse_y):
                    self.play = True
                elif self.botaoRanking.collidepoint(mouse_x, mouse_y):
                    self.ranking = True
                elif self.botaoSair.collidepoint(mouse_x, mouse_y):
                    pygame.quit()
                    return False
        return True
    def troca_tela(self):
        if self.play:
            return TelaJogo(self.tela)
        elif self.ranking:
            return TelaRanking(self.tela)
        else:
            return self
class TelaJogo:
    def __init__(self, tela):
        self.blocos = []
        self.barcos = []
        self.gerarBlocos(self.generateGrid())
        self.frame = 0
        self.tela = tela
        self.clock = pygame.time.Clock()
        self.player = Player()
    def gerarBlocos(self, grid): # Gerar todos os blocos que vão ocupar a tela
        y = 800
        for row in grid:
            centro = 25
            for block in row:
                if block == 'agua' and random.randint(0, 2) == 0: # 1/3 de chance de gerar um barco, por bloco de agua
                    barco = sprites['barco'].get_rect()
                    barco.centerx = centro
                    barco.bottom = y
                    self.barcos.append(barco)
                bloco = sprites[block].get_rect()
                bloco.centerx = centro
                bloco.bottom = y
                centro += 50
                self.blocos.append((sprites[block], bloco, block)) # (imagem, rect, tipo)
            centro = 25
            y -= 50
    def generateGrid(self):
        grid = []
        for _ in range(16):
            tile = random.choice(['grama', 'agua', 'trilho'])
            grid.append([tile] * 10)
        return grid
    def updateBlocos(self):
        for i in self.blocos:
            i[1].bottom += 1
        for barco in self.barcos:
            barco.centerx -= 1
            barco.bottom += 1
            if barco.centerx < -50:
                barco.centerx = 550
            if barco.bottom > 800:
                self.barcos.remove(barco)
        if self.frame == 0: # Gerar uma nova fileira em cima
            self.nova_fileira()
            self.frame = -50
        self.frame += 1 
    def nova_fileira(self):
        block = random.choice(['grama', 'agua', 'trilho'])
        for i in range(10):
            if block == 'agua' and random.randint(0, 2) == 0: # 1/3 de chance de gerar um barco, por bloco de agua
                barco = sprites['barco'].get_rect()
                barco.centerx = i * 50 + 25
                barco.bottom = 0
                self.barcos.append(barco)
            bloco = sprites[block].get_rect()
            bloco.centerx = i * 50 + 25
            bloco.bottom = 0
            self.blocos.append((sprites[block], bloco, block)) # (imagem, rect, tipo)
    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
        self.updateBlocos()
        self.player.update()
        self.clock.tick(30)
        return True
    def desenha(self):
        for i in self.blocos:
            self.tela.blit(i[0], i[1])
        for i in self.barcos:
            self.tela.blit(sprites['barco'], (i[0], i[1]))
        self.tela.blit(self.player.image, self.player.rect)
        pygame.display.update()
    def troca_tela(self):
        if self.player.checarMorte(self.blocos, self.barcos):
            print('morreu')
            return TelaInicial(self.tela)
        else:
            return self