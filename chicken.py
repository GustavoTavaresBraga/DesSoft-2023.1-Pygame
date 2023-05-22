import pygame
class Player():
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(pygame.image.load('sprites/chicken.png'), (50, 50))
        self.rect = self.image.get_rect()
        self.rect.centerx = 500 / 2
        self.rect.bottom = 700
        self.movimento = None
        self.moveu = 0
        self.noBarco = False
    def update(self, blocos, barcos):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and self.movimento is None: self.movimento = 'cima'
        if keys[pygame.K_DOWN] and self.movimento is None: self.movimento = 'baixo'
        if keys[pygame.K_LEFT] and self.movimento is None: self.movimento = 'esquerda'
        if keys[pygame.K_RIGHT] and self.movimento is None: self.movimento = 'direita'

        self.rect.bottom += 1 # Mexer a galinha pra baixo
        if self.noBarco:
            self.rect.centerx -= 1
        if self.movimento == 'cima':
            self.rect.y -= 2
            self.moveu +=1
            if self.moveu == 25:
                self.movimento = None
                self.moveu = 0

        if self.movimento == 'baixo':
            self.rect.y += 2
            self.moveu +=1
            if self.moveu == 25:
                self.movimento = None
                self.moveu = 0
        if self.movimento == 'esquerda':
            self.rect.x -= 2
            self.moveu +=1
            if self.moveu == 25:
                self.movimento = None
                self.moveu = 0

        if self.movimento == 'direita':
            self.rect.x += 2
            self.moveu +=1
            if self.moveu == 25:
                self.movimento = None
                self.moveu = 0

        #conferir estado
        self.noBarco = False
        for i in blocos:
            if i[2] == 'agua' and self.rect.colliderect(i[1]):
                for barco in barcos:
                    if abs(self.rect.centerx - barco.centerx) < 50 and abs(self.rect.bottom - barco.bottom) < 50:
                        self.noBarco = True
                if not self.noBarco:
                    pygame.quit() # falta fazer o barco funcionar
        return False