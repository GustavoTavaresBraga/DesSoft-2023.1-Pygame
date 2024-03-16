# Importa as bibliotecas que serão utilizadas no código
import pygame
from sprites import sprites, efeitos_sonoros


class Entity(pygame.sprite.Sprite):
    def __init__(self, world, x, y, entity_type, speedX=0):
        self.world = world
        pygame.sprite.Sprite.__init__(self)
        self.entity_type = entity_type
        self.speedX = speedX
        self.image = self.get_image(speedX)
        self.rect = self.image.get_rect(centerx=x, bottom=y)
    def get_image(self, speedX):
        if speedX <= 0:
            return sprites[self.entity_type]
        else:
            return pygame.transform.flip(sprites[self.entity_type], True, False)
    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def update(self):
        self.rect.bottom += self.world.speed

class Boat(Entity):
    def __init__(self, world, x, y, speedX=0):
        super().__init__(world, x, y, 'boat', speedX)
        self.type = 'boat'
    def update(self):
        super().update()
        self.rect.centerx += self.speedX
        if self.rect.centerx < -50 and self.speedX < 0:
            self.rect.centerx = 550
        elif self.rect.centerx > 550 and self.speedX > 0:
            self.rect.centerx = -50

class Minecart(Entity):
    def __init__(self,world, x, y, speedX=0):
        super().__init__( world, x, y, 'minecart', speedX)
        self.type = 'minecart'

    def update(self):
        super().update()
        self.rect.centerx += self.speedX
        if self.rect.centerx < -50 and self.speedX < 0:
            self.rect.centerx = 550
        elif self.rect.centerx > 550 and self.speedX > 0:
            self.rect.centerx = -50

class Water(Entity):
    def __init__(self,world, x, y):
        super().__init__( world,x, y, 'water')
        self.type = 'water'

class Grass(Entity):
    def __init__(self,world, x, y):
        super().__init__(world, x, y, 'grass')
        self.type = 'grass'

class Rails(Entity):
    def __init__(self,world,  x, y):
        super().__init__(world, x, y, 'rails')
        self.type = 'rails'


# Cria a classe do jogador
class Player(Entity):
    def __init__(self, world):
        pygame.sprite.Sprite.__init__(self)
        super().__init__(world, 250, 690, 'chicken')

        self.rect = pygame.Rect(230,650,40,40)
        self.image = sprites['chicken']
        self.red_image = sprites['chickenRed']
        self.movement = None
        self.moveu = 0
        self.onBoat = False
        self.vidas = 10
        self.speedBoat = 0
        self.score = 0
        self.speed = 2
        self.immunity = 0
        self.morreu = False
        self.world = world
    # Cria a função update para atualizar a posição do jogador
    def update(self):
        super().update()
        # nomeando as direções do jogador baseado na seta em que o usuario aperta ou segura
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and self.movement is None and self.rect.bottom >= 50: self.movement = 'cima'
        if keys[pygame.K_DOWN] and self.movement is None and self.rect.bottom <= 750: self.movement = 'baixo'
        if keys[pygame.K_LEFT] and self.movement is None and self.rect.centerx >= 50: self.movement = 'esquerda'
        if keys[pygame.K_RIGHT] and self.movement is None and self.rect.centerx <= 450: self.movement = 'direita'
        self.rect.centerx += self.speedBoat
        # criando as velocidades em que o jogador ira se mexer, baseado na tecla em que ele apertou
        if self.movement == 'cima':
            self.rect.y -= 10
        if self.movement == 'baixo':
            self.rect.y += 10
        if self.movement == 'esquerda':
            self.rect.x -= 10
        if self.movement == 'direita':
            self.rect.x += 10
        if not self.movement is None:
            self.moveu += 1
        if self.moveu == 5:
            if self.movement == 'cima':
                self.score += 1
            elif self.movement == 'baixo':
                self.score -= 1
            self.movement = None
            self.moveu = 0
        
        if self.movement == None:
            self.onBoat = self.noBarco()
            if self.checarMorte():
                self.morreu = True
        #conferir estado
        self.immunity -= 1
        
    # Confere se o jogador morreu
    def noBarco(self):
        clossest = 1000
        for i in self.world.getEntities():
            if i.entity_type != 'boat':
                continue
            if i.rect.colliderect(self.rect):
                distanceToBoat = abs(i.rect.centerx - self.rect.centerx)
                if distanceToBoat < clossest:
                    clossest = distanceToBoat
                    boat = i
        if clossest < 40:
            self.speedBoat = boat.speedX
            self.rect.centerx = boat.rect.centerx
            return True
        self.speedBoat = 0
        return False
    def checarMorte(self):
        if self.rect.bottom > 840:      #conferindo se morreu porque a galinha foi mais devagar do que a screen e sumiu 
            efeitos_sonoros['morte_som'].play()     #som de morte da galinha
            return True
        if self.rect.centerx < -25 or self.rect.centerx > 525:
                return True
        for i in self.world.getEntities():
            if i.entity_type != 'minecart':
                continue
            if i.rect.colliderect(self.rect) and self.immunity <= 0:
                self.vidas -= 1
                efeitos_sonoros['morte_som'].play()
                self.immunity = 50
        for i in self.world.getEntities():
            if i.entity_type != 'water':
                continue
            if i.rect.colliderect(self.rect) and not self.onBoat and self.immunity <= 0:
                self.vidas -= 1
                efeitos_sonoros['morte_som'].play()
                self.immunity = 50
        if self.vidas <= 0:     #conferindo se morreu pela falta de vidas
            return True
        return False
    def draw(self, screen):
        if self.immunity > 0:
            screen.blit(self.red_image, self.rect)
        else:
            screen.blit(self.image, self.rect)

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