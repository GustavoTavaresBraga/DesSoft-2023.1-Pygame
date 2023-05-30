# Importa as bibliotecas que serão utilizadas no código
import pygame
from sprites import sprites, efeitos_sonoros
# Cria a classe do jogador
class Player():
    def __init__(self, velocidade = 2, vidas = 3):
        pygame.sprite.Sprite.__init__(self)
        self.image = sprites['chicken']
        self.rect = pygame.Rect(0, 0, 40, 40)
        self.rect.centerx = 500 / 2
        self.rect.bottom = 690
        self.movimento = None
        self.original_image = self.image.copy()
        self.moveu = 0
        self.noBarco = False
        self.blocos = []
        self.vidas = vidas
        self.speedBoat = 0
        self.score = 0
        self.obstaculos = []
        self.velocidade = velocidade
        self.imunidade = 0

    # Cria a função update para atualizar a posição do jogador
    def update(self):
        # nomeando as direções do jogador baseado na seta em que o usuario aperta ou segura
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and self.movimento is None and self.rect.bottom >= 50: self.movimento = 'cima'
        if keys[pygame.K_DOWN] and self.movimento is None and self.rect.bottom <= 750: self.movimento = 'baixo'
        if keys[pygame.K_LEFT] and self.movimento is None and self.rect.centerx >= 50: self.movimento = 'esquerda'
        if keys[pygame.K_RIGHT] and self.movimento is None and self.rect.centerx <= 450: self.movimento = 'direita'
       
        if self.noBarco:        #condição para o jogador se movimentar junto com o barco
            self.rect.centerx += self.speedBoat
            if self.rect.centerx < -25:
                self.rect.centerx = 525
            if self.rect.centerx > 525:
                self.rect.centerx = -25

        # criancriando as velocidades em que o jogador ira se mexer, baseado na tecla em que ele apertou
        if self.movimento == 'cima':
            self.rect.y -= 10
            self.moveu +=1
            if self.moveu == 5:
                self.movimento = None
                self.moveu = 0
                self.score += 1
        if self.movimento == 'baixo':
            self.rect.y += 10
            self.moveu +=1
            if self.moveu == 5:
                self.movimento = None
                self.moveu = 0
                self.score -= 1
        if self.movimento == 'esquerda':
            self.rect.x -= 10
            self.moveu +=1
            if self.moveu == 5:
                self.movimento = None
                self.moveu = 0
        if self.movimento == 'direita':
            self.rect.x += 10
            self.moveu +=1
            if self.moveu > 5:
                self.movimento = None
                self.moveu = 0

        #conferir estado
        for i in self.blocos:
            if i.rect.bottom > 850:
                self.blocos.remove(i)
            i.update(self.velocidade)
        for i in self.obstaculos:
            if i.rect.bottom > 850:
                self.obstaculos.remove(i)
            i.update(self.velocidade)
        self.imunidade -= 1
        self.rect.bottom += self.velocidade # Mexer a galinha pra baixo

    # Confere se o jogador morreu
    def checarMorte(self):
        if self.vidas <= 0:     #conferindo se morreu pela falta de vidas
                return True
        self.image.blit(self.original_image, (0, 0))
        if self.rect.bottom > 840:      #conferindo se morreu porque a galinha foi mais devagar do que a tela e sumiu 
            efeitos_sonoros['morte_som'].play()     #som de morte da galinha
            return True
        self.noBarco = False
        for i in self.obstaculos:
            # Conferindo se a galinha colidiu sem estar imune, o que a faz perder uma vida e recber imunidade por um curto tempo
            if i.rect.colliderect(self.rect) and i.tipo == 'minecart' and self.imunidade <= 0:
                self.vidas -= 1
                efeitos_sonoros['morte_som'].play()
                self.imunidade = 50
                return False
            if i.rect.colliderect(self.rect) and i.tipo == 'barco':
                self.noBarco = True
                self.speedBoat = i.speedX
        for i in self.blocos:
            # Conferindo se a galinha se afougou sem estar imune, o que a faz perder uma vida e recber imunidade por um curto tempo
            if i.rect.colliderect(self.rect) and i.tipo == 'agua':
                if not self.noBarco and self.imunidade <= 0:
                    self.vidas -= 1
                    efeitos_sonoros['morte_som'].play()
                    self.imunidade = 50
                    return False
        if self.imunidade > 25:
            # fazendo a galinha ficar vermelha, para ilustrar que ela sofreu dano/perdeu uma vida
            tint = pygame.Surface(self.image.get_size()).convert_alpha()
            tint.fill((255, 0, 0))
            self.image.blit(tint, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
        return False

# Cria a classe do carrinho de mineração (obstaculos)
class Minecart():
    def __init__(self, x, y, player, speed, direcao):
        pygame.sprite.Sprite.__init__(self)
        self.image = sprites['minecart']
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.direcao = direcao
        self.rect.bottom = y
        self.tipo = 'minecart'
        self.speedX = speed*direcao
        player.obstaculos.append(self)

    # Atualiza as posições do carrinho de mineração
    def update(self, velocidade = 2):
        self.rect.bottom += velocidade # 
        self.rect.centerx += self.speedX
        #condição para o carrinho que sair de um lado da tela, voltar para a outra extremidade
        if self.rect.centerx < -50 and self.direcao == -1:
            self.rect.centerx = 550
            efeitos_sonoros['minecart_som'].play()
            efeitos_sonoros['minecart_som'].set_volume(0.1)
            efeitos_sonoros['minecart_som'].fadeout(4000)
        elif self.rect.centerx > 550 and self.direcao == 1:
            self.rect.centerx = -50

# Cria a classe do barco
class Barco():
    #
    def __init__(self, x, y, player, speed, direcao):
        pygame.sprite.Sprite.__init__(self)
        self.image = sprites['barco']
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.tipo = 'barco'
        self.direcao = direcao
        self.speedX = speed*direcao
        player.obstaculos.append(self)

    # Atualiza a posição do barco
    def update(self, velocidade = 2):
        self.rect.bottom += velocidade # 
        self.rect.centerx += self.speedX
        #condição para o barco que sair de um lado da tela, voltar para a outra extremidade
        if self.rect.centerx < -25 and self.direcao == -1:
            self.rect.centerx = 525
        elif self.rect.centerx > 525 and self.direcao == 1:
            self.rect.centerx = -25

# Cria a classe da água
class Agua():
    def __init__(self, x, y, player):
        pygame.sprite.Sprite.__init__(self)
        self.image = sprites['agua']
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.tipo = 'agua'
        player.blocos.append(self)

    #velocidade para a agua ir descendo na tela
    def update(self, velocidade = 2):
        self.rect.bottom += velocidade # 

# Cria a classe da grama
class Grama():
    def __init__(self, x, y, player):
        pygame.sprite.Sprite.__init__(self)
        self.image = sprites['grama']
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.tipo = 'grama'
        player.blocos.append(self)
    
    #velocidade em que a grama desce na tela
    def update(self, velocidade = 2):
        self.rect.bottom += velocidade # 

# Cria classe do trilho
class Trilho():
    #
    def __init__(self, x, y, player):
        pygame.sprite.Sprite.__init__(self)
        self.image = sprites['trilho']
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.tipo = 'trilho'
        player.blocos.append(self)

    # velocidade em que o trilho desce na tela
    def update(self, velocidade = 2):
        self.rect.bottom += velocidade # 

# Cria a classe da caixa de texto
class CaixaTexto():
    # caixa de texto para o jogador registrar seu nome e salvar sua pontuação no Ranking
    def __init__ (self, fonte, tela):
        self.rect = pygame.Rect(140, 510, 430 , 35)
        self.texto = 'escreva seu nome'
        self.texto_surface = fonte.render(self.texto, True, (211, 211, 211))
        self.pode_escrever = False
        self.fonte = fonte
        self.cor = 'Yellow'
        self.tela = tela
        self.nome = ''
    
    def escreve(self, event): # função para o jogador poder escrever 
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            #Muda cor caso clicado
            if  self.rect.collidepoint(event.pos):      #condição para saber se o usuario ainda está escrevendo
                self.pode_escrever = True
                self.texto = ''
                self.rect.x = 250
                self.texto_surface = self.fonte.render(self.texto, True, (211, 211, 211))
            else:
                self.pode_escrever = False
        #Salva o texto
        if event.type == pygame.KEYDOWN and self.pode_escrever:
            if event.key == pygame.K_BACKSPACE:
                self.texto = self.texto[:-1]
                self.rect.width -= 20
                self.rect.x += 7
            #Aumenta o tamanho
            else:
                self.texto += event.unicode #https://www.pygame.org/docs/ref/event.html
                self.rect.width += 20
                self.rect.x -= 7
            self.texto_surface = self.fonte.render(self.texto, True, (211, 211, 211))

    # Função para aparecer na tela a escrita
    def desenha(self):
        self.tela.blit(self.texto_surface, (self.rect.x + 5, self.rect.y + 5))