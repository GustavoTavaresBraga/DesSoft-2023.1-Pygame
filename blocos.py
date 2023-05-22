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
