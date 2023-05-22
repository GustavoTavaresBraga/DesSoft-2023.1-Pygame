from sprites import sprites
import random
class Blocos():
    def __init__(self):
        self.blocos = []
        self.barcos = []
        self.gerarBlocos(self.generateGrid())
        self.frame = 0
    def gerarBlocos(self, grid): # Gerar todos os blocos que vão ocupar a tela
        y = 800
        for row in grid:
            centro = 25
            for block in row:
                if block == 'agua' and random.randint(0, 2) == 0: # 1/3 de chance de gerar um barco, por bloco de agua
                    self.barcos.append([centro, y-50])
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
        for i in self.barcos:
            i[0] -= 1
            i[1] +=1
            if i[0] < -50:
                i[0] = 550
        if self.frame == 0: # Gerar uma nova fileira em cima
            self.frame = -50
            block = random.choice(['grama', 'agua', 'trilho'])
            for i in range(10):
                if block == 'agua' and random.randint(0, 2) == 0: # 1/3 de chance de gerar um barco, por bloco de agua
                    self.barcos.append([i*50+25, -50])
                bloco = sprites[block].get_rect()
                bloco.centerx = i * 50 + 25
                bloco.bottom = 0
                self.blocos.append((sprites[block], bloco, block)) # (imagem, rect, tipo)
        self.frame += 1
   