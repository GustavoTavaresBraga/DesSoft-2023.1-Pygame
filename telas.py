import pygame
import random
from sprites import sprites
from chicken import *
global jogador
class TelaInicial():
    def __init__(self, tela):
        self.tela = tela
        self.fonte  = pygame.font.Font('MinecraftTen-VGORe.ttf', 30)
        self.fundo = pygame.transform.scale((pygame.image.load('sprites/inicio.png').convert_alpha()), (500, 800))
        self.botaoPlay = pygame.Rect(55, 405, 425, 40)
        self.botaoRanking = pygame.Rect(55, 460, 425, 40)
        self.botaoSair = pygame.Rect(275, 585, 210, 40)
        self.botaoOptions = pygame.Rect(55, 585, 210, 40)
        self.play = False
        self.options = False
        self.ranking = False
        self.caixaTexto = CaixaTexto(self.fonte, tela)
    def desenha(self):
        self.tela.fill((255, 255, 255))
        self.tela.blit(self.fundo, (0, 0))
        self.caixaTexto.desenha()
        pygame.display.update()

    def update(self):
        for event in pygame.event.get():
            self.caixaTexto.escreve(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left mouse button click
                mouse_x, mouse_y = event.pos
                if self.botaoPlay.collidepoint(mouse_x, mouse_y):
                    self.play = True
                elif self.botaoRanking.collidepoint(mouse_x, mouse_y):
                    self.ranking = True
                elif self.botaoOptions.collidepoint(mouse_x, mouse_y):
                    self.options = True
                elif self.botaoSair.collidepoint(mouse_x, mouse_y):
                    pygame.quit()
                    return False
        return True
    def troca_tela(self):
        if self.play:
            return TelaJogo(self.tela, self.caixaTexto.texto)
        elif self.ranking:
            return TelaRanking(self.tela)
        elif self.options:
            return self
        else:
            return self
        
class TelaJogo:
    def __init__(self, tela, nome):
        self.frame = 0
        self.tela = tela
        self.y = 0
        self.clock = pygame.time.Clock()
        self.player = Player()
        self.fonte  = pygame.font.Font(None, 36)
        self.dificuldade = 0
        self.nome = nome
        for i in range(17):
            self.nova_fileira(y=800-(i*50))
    def nova_fileira(self, y=0):
        block = random.choice(['grama', 'agua', 'trilho', 'grama', 'trilho', 'grama'])
        if self.dificuldade > 0:
            block = random.choice(['trilho', 'agua', 'trilho', 'grama', 'trilho', 'grama'])
        if y > 500 and y <850:
            block = 'grama'
        direcao = random.choice([1, -1])
        speed = random.randint(2+self.dificuldade, 3+self.dificuldade)
        temBarco = False
        for i in range(10):
            if block == 'grama':Grama(i * 50 + 25, y, self.player)
            elif block == 'agua':Agua(i * 50 + 25, y, self.player)
            elif block == 'trilho':Trilho(i * 50 + 25, y, self.player)
            if block == 'agua' and random.randint(0, 2+self.dificuldade) == 0:
                Barco(i * 50 + 25, y, self.player, speed, direcao)
                temBarco = True
            elif not temBarco and i == 9 and block == 'agua':
                Barco(i * 50 + 25, y, self.player, speed, direcao)
            if block == 'trilho' and random.randint(0, 4-self.dificuldade) == 0:Minecart(i * 50 + 25, y, self.player, speed*2 -1, direcao)
    def salvar_highscore(self):
        if self.nome == '' and self.nome != 'digite seu nome':
            string = '\n'+self.nome+','+str(self.player.score)
            with open('scores.csv', 'a') as f:
                f.write(string)
                print(string)
    def update(self):
        if self.y == 25: # Gerar uma nova fileira em cima
            self.nova_fileira()
            self.y = 0
        self.y += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
        self.player.update()
        self.clock.tick(30)
        if self.player.score > 40:
            self.dificuldade = 2
        return True
    
    def desenha(self):
        self.tela.fill((255, 255, 255))
        for i in self.player.blocos:
            self.tela.blit(i.image, i.rect)
        for i in self.player.obstaculos:
            self.tela.blit(i.image, i.rect)
        self.tela.blit(self.player.image, self.player.rect)
        t = "pontuacao: " + str(self.player.score)
        texto = self.fonte.render(t, True, (255, 255, 255))
        self.tela.blit(texto, (300, 10))
        pygame.display.update()
    
    def troca_tela(self):
        if self.player.checarMorte():
            self.salvar_highscore()
            return TelaInicial(self.tela)
        else:
            return self
class TelaRanking():
    def __init__(self, tela):
        self.ranking = {}
        self.tela = tela
        with open('scores.csv', 'r') as scores:
            for line in scores:
                nome, score = line.split(',')
                self.ranking[nome] = int(score)
        self.ranking = sorted(self.ranking.items(), key=lambda x: x[1], reverse=True)
        self.fonte  = pygame.font.Font('MinecraftTen-VGORe.ttf', 30)
        self.botaoSair = pygame.Rect(0, 0, 100, 50)
        self.voltar = False
    def desenha(self):
        self.tela.fill((0, 0, 0))
        texto1 = self.fonte.render('voltar', True, (255, 255, 255))
        self.tela.blit(texto1, (0, 0))
        for i in range(len(self.ranking)):
            nome, score = self.ranking[i]
            texto = self.fonte.render(str(i+1)+'. '+nome+' - '+str(score), True, (255, 255, 255))
            self.tela.blit(texto, (100, 100+i*50))
        pygame.display.update()

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.botaoSair.collidepoint(event.pos) or (event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE): # Left mouse button click
                self.voltar = True
        return True
    def troca_tela(self):
        if self.voltar:
            return TelaInicial(self.tela)
        else:
            return self