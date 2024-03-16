# Importa as bibliotecas que serão utilizadas no código
import pygame
from sprites import sprites, efeitos_sonoros

import pygame

class Entity(pygame.sprite.Sprite):
    def __init__(self, player, x, y, entity_type, speedX=0):
        pygame.sprite.Sprite.__init__(self)
        self.entity_type = entity_type
        self.speedX = speedX
        self.image = self.get_image(speedX)
        self.rect = self.image.get_rect(centerx=x, bottom=y)
        self.player = player
        self.player.entities.append(self)

    def get_image(self, speedX):
        if speedX <= 0:
            return sprites[self.entity_type]
        else:
            return pygame.transform.flip(sprites[self.entity_type], True, False)

    def update(self):
        self.rect.bottom += self.player.speed

class Boat(Entity):
    def __init__(self, player, x, y, speedX=0):
        super().__init__(player, x, y, 'boat', speedX)
        self.type = 'boat'
    def update(self):
        super().update()
        self.rect.centerx += self.speedX
        if self.rect.centerx < -50 and self.speedX < 0:
            self.rect.centerx = 550
        elif self.rect.centerx > 550 and self.speedX > 0:
            self.rect.centerx = -50

class Minecart(Entity):
    def __init__(self, player, x, y, speedX=0):
        super().__init__(player, x, y, 'minecart', speedX)
        self.type = 'minecart'

    def update(self):
        super().update()
        self.rect.centerx += self.speedX
        if self.rect.centerx < -50 and self.speedX < 0:
            self.rect.centerx = 550
        elif self.rect.centerx > 550 and self.speedX > 0:
            self.rect.centerx = -50

class Water(Entity):
    def __init__(self, player, x, y):
        super().__init__(player, x, y, 'water')
        self.type = 'water'

class Grass(Entity):
    def __init__(self, player, x, y):
        super().__init__(player, x, y, 'grass')
        self.type = 'grass'

class Rails(Entity):
    def __init__(self, player, x, y):
        super().__init__(player, x, y, 'rails')
        self.type = 'rails'


# Cria a classe do jogador
class Player():
    def __init__(self, speed = 2, vidas = 3):
        pygame.sprite.Sprite.__init__(self)
        self.image = sprites['chicken']
        self.rect = pygame.Rect(0, 0, 40, 40)
        self.rect.centerx = 500 / 2
        self.rect.bottom = 690
        self.movement = None
        self.original_image = self.image.copy()
        self.moveu = 0
        self.onBoat = False
        self.vidas = vidas
        self.speedBoat = 0
        self.score = 0
        self.entities = []
        self.speed = speed
        self.immunity = 0

    # Cria a função update para atualizar a posição do jogador
    def update(self):
        # nomeando as direções do jogador baseado na seta em que o usuario aperta ou segura
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and self.movement is None and self.rect.bottom >= 50: self.movement = 'cima'
        if keys[pygame.K_DOWN] and self.movement is None and self.rect.bottom <= 750: self.movement = 'baixo'
        if keys[pygame.K_LEFT] and self.movement is None and self.rect.centerx >= 50: self.movement = 'esquerda'
        if keys[pygame.K_RIGHT] and self.movement is None and self.rect.centerx <= 450: self.movement = 'direita'
       
        if self.onBoat:        #condição para o jogador se movimentar junto com o barco
            self.rect.centerx += self.speedBoat
            if self.rect.centerx < -25:
                self.rect.centerx = 525
            if self.rect.centerx > 525:
                self.rect.centerx = -25

        # criando as velocidades em que o jogador ira se mexer, baseado na tecla em que ele apertou
        if self.movement == 'cima':
            self.rect.y -= 10
            self.moveu +=1
            if self.moveu == 5:
                self.movement = None
                self.moveu = 0
                self.score += 1
            
            if self.onBoat:
                closest_boat = min([i for i in self.entities if i.type == 'boat'], key=lambda x: abs(x.rect.centerx - self.rect.centerx))
                # move towards closes boat
                distance = abs(closest_boat.rect.centerx - self.rect.centerx)
                if distance != 0:
                    self.rect.centerx += 1 if closest_boat.rect.centerx > self.rect.centerx else -20
        if self.movement == 'baixo':
            self.rect.y += 10
            self.moveu +=1
            if self.moveu == 5:
                self.movement = None
                self.moveu = 0
                self.score -= 1
        if self.movement == 'esquerda':
            self.rect.x -= 10
            self.moveu +=1
            if self.moveu == 5:
                self.movement = None
                self.moveu = 0
        if self.movement == 'direita':
            self.rect.x += 10
            self.moveu +=1
            if self.moveu > 5:
                self.movement = None
                self.moveu = 0

        #conferir estado
        for i in self.entities:
            i.update()
            if i.rect.bottom > 850:
                self.entities.remove(i)
        self.immunity -= 1
        self.rect.bottom += self.speed # Mexer a galinha pra baixo

    # Confere se o jogador morreu
    def checarMorte(self):
        if self.vidas <= 0:     #conferindo se morreu pela falta de vidas
                return True
        self.image.blit(self.original_image, (0, 0))
        if self.rect.bottom > 840:      #conferindo se morreu porque a galinha foi mais devagar do que a screen e sumiu 
            efeitos_sonoros['morte_som'].play()     #som de morte da galinha
            return True
        self.onBoat = False
        for i in self.entities:
            # Conferindo se a galinha colidiu sem estar imune, o que a faz perder uma vida e recber immunity por um curto tempo
            if i.rect.colliderect(self.rect) and i.type == 'minecart' and self.immunity <= 0:
                self.vidas -= 1
                efeitos_sonoros['morte_som'].play()
                self.immunity = 50
                return False
            if i.rect.colliderect(self.rect) and i.type == 'boat':
                self.onBoat = True
                self.speedBoat = i.speedX
        for i in self.entities:
            # Conferindo se a galinha se afougou sem estar imune, o que a faz perder uma vida e recber immunity por um curto tempo
            if i.rect.colliderect(self.rect) and i.type == 'water':
                if not self.onBoat and self.immunity <= 0:
                    self.vidas -= 1
                    efeitos_sonoros['morte_som'].play()
                    self.immunity = 50
                    return False
        if self.immunity > 25:
            # fazendo a galinha ficar vermelha, para ilustrar que ela sofreu dano/perdeu uma vida
            tint = pygame.Surface(self.image.get_size()).convert_alpha()
            tint.fill((255, 0, 0))
            self.image.blit(tint, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
        return False

# Cria a classe da caixa de text
class TextBox():
    # caixa de text para o jogador registrar seu nome e salvar sua pontuação no Ranking
    def __init__ (self, fonte, screen, pos = (140, 510, 430 , 35)):
        self.rect = pygame.Rect(pos[0], pos[1], pos[2], pos[3])
        self.text = 'escreva seu nome'
        self.text_surface = fonte.render(self.text, True, (211, 211, 211))
        self.writable = False
        self.fonte = fonte
        self.color = 'Yellow'
        self.screen = screen
        self.nome = ''
    
    def escreve(self, event): # função para o jogador poder escrever 
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            #Muda color caso clicado
            if  self.rect.collidepoint(event.pos):      #condição para saber se o usuario ainda está escrevendo
                self.writable = True
                self.text = ''
                self.rect.x = 250
                self.text_surface = self.fonte.render(self.text, True, (211, 211, 211))
            else:
                self.writable = False
        #Salva o text
        if event.type == pygame.KEYDOWN and self.writable:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
                self.rect.width -= 20
                self.rect.x += 7
            #Aumenta o tamanho
            else:
                self.text += event.unicode #https://www.pygame.org/docs/ref/event.html
                self.rect.width += 20
                self.rect.x -= 7
            self.text_surface = self.fonte.render(self.text, True, (211, 211, 211))

    # Função para aparecer na screen a escrita
    def desenha(self):
        self.screen.blit(self.text_surface, (self.rect.x + 5, self.rect.y + 5))

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