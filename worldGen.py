from chicken import *
from sprites import *
import random
class World:
    def __init__(self, screen, opcoes=None):
        self.opcoes = opcoes if opcoes else {'Vidas': 3, 'Velocidade': 2, 'NBarcos': 3, 'NMinecarts': 3, 'VB': 2, 'VM': 2}
        self.player = Player(self, vidas=self.opcoes['Vidas'])
        self.entities = []
        self.screen = screen
        self.speed = self.opcoes['Velocidade']
        self.y = 0
        self.previousSpeed = 0
        self.biomes = {
            0: Plains,
            50: Nether,
            100: NetherHard,
            200: End
        }
        self.map = [['X']*9]*16
        self.currentBiome = self.biomes[0](self)
        self.currentBiome.load_sprites()
        for i in range(16):
            new_row = self.currentBiome.new_row(y=800-(i*50))
            for entity in new_row:
                self.entities.append(entity)
        
    def draw(self):
        for entity in self.entities:
            if entity.entity_type == 'boat' or entity.entity_type == 'minecart' or entity.entity_type == 'heart':
                continue
            entity.draw(self.screen)
        for entity in self.entities:
            if entity.entity_type == 'boat' or entity.entity_type == 'minecart' or entity.entity_type == 'heart':
                entity.draw(self.screen)
        self.player.draw(self.screen)
    def update(self):
        currentLayer = self.y/(50/self.speed)+14
        if  currentLayer in self.biomes.keys():
            self.currentBiome = self.biomes[currentLayer](self)
            self.currentBiome.load_sprites()
        if self.y%(50/self.speed) == 0: # Gerar uma nova fileira em cima
            self.generate()
        self.y += 1
        for entity in self.entities:
            entity.update()
            if entity.rect.bottom >= 850:
                self.entities.remove(entity)
        self.player.update()
    def getEntities(self):
        return self.entities
    def generate(self, y=0):
        new_row = self.currentBiome.new_row(y)
        row = []
        
        for entity in new_row:
            if entity.entity_type == 'grass' or entity.entity_type == 'rails':
                row.append('X')
            if entity.entity_type == 'boat':
                row = ['X']*9
                break
            if entity.entity_type == 'water':
                row.append(' ')
        self.map.append(row)
        mapa = [row.copy() for row in self.map[self.player.score+2:]]
        mapa[0][min(round(self.player.rect.x/ 50), 8)] = 'P'
        for entity in new_row:
            self.entities.append(entity)

class Biome:
    def __init__(self, world):
        self.world = world
        self.stickTo = ['boat']
    def new_row(self, y=0):
        row = []
        block = random.choices(['grass', 'water', 'rails'], self.weights)[0] #opções das sprites que podem ser escolhidas inicialmete, algumas possuem mais chances de serem escolhidas
        direction = random.choice([1, -1])    #escolhendo aleatoriamente a direção dos barcos e carrinhos
         #garantir que a direção dos barcos e carrinhos não seja a mesma que a anterior
        speed = random.randint(self.speeds[0], self.speeds[1])
        while abs(self.world.previousSpeed- speed*direction) < 2:
            speed = random.randint(self.speeds[0], self.speeds[1])
        self.world.previousSpeed = speed*direction
        
        if y > 500 and y <850:  #condição para o jogador não nascer em cima de uma sprite de water ou rails, e sim sobre um bloco de grass
            block = 'grass'
        # garantir que ao menos um obstaculo/boat seja gerado
        gerouObstaculo = False
        for i in range(10):
            if block == 'water': 
                row.append(Water(self.world, i * 50 + 25, y))
                if random.random() < self.boatChance or (i > 4 and not gerouObstaculo):
                    row.append(Boat(self.world, i * 50 + 25, y, speed*direction))
                    gerouObstaculo = True
                    if random.random() < self.heartChance:
                        row.append(Heart(self.world, i * 50 + 25, y, speedX = speed*direction))
                        print()
            elif block == 'rails': 
                row.append(Rails(self.world, i * 50 +25, y))
                if random.random() < self.minecartChance or (i > 8 and not gerouObstaculo):
                    row.append(Minecart(self.world, i * 50 + 25, y, speed*direction))
                    gerouObstaculo = True
                elif random.random() < self.heartChance:
                    row.append(Heart(self.world, i * 50 + 25, y))
            elif block == 'grass': 
                row.append(Grass(self.world, i * 50 +25, y))
                if random.random() < self.heartChance:
                    row.append(Heart(self.world, i * 50 + 25, y))
        return row
    def load_sprites(self):
        for key, value in self.sprites.items():
            sprites[key] = pygame.transform.scale(pygame.image.load('assets/sprites/'+value), (50, 50))

class Plains(Biome):
    def __init__(self, world):
        super().__init__(world)
        opcoes = world.opcoes
        self.weights = [5, 2, 3] # grass water rails
        self.boatChance = 0.1 * opcoes.get('NBarcos', 3)
        self.minecartChance = 0.08 * opcoes.get('NMinecarts', 3)
        self.heartChance = 0.005
        self.speeds = [opcoes.get('VB', 2), opcoes.get('VM', 2) + 6]
        self.biomeName = 'plains'
        self.sprites = {
            'grass': 'grass.png',
            'rails': 'rails.png',
            'water': 'water.png',
            'boat': 'boat.png'
        }
        

class Nether(Biome):
    def __init__(self, world):
        super().__init__(world)
        opcoes = world.opcoes
        self.weights = [4, 5,2] # grass water rails
        self.boatChance = 0.12 * opcoes.get('NBarcos', 3)
        self.minecartChance = 0.07 * opcoes.get('NMinecarts', 3)
        self.heartChance = 0.003
        self.speeds = [opcoes.get('VB', 2) + 1, opcoes.get('VM', 2) + 4]
        self.biomeName = 'nether'
        self.sprites = {
            'grass': 'netherack.png',
            'rails': 'railsNether.png',
            'water': 'lava.png',
        }
class NetherHard(Biome):
    def __init__(self, world):
        super().__init__(world)
        opcoes = world.opcoes
        self.weights = [3, 5,3] # grass water rails
        self.boatChance = 0.13 * opcoes.get('NBarcos', 3)
        self.minecartChance = 0.1 * opcoes.get('NMinecarts', 3)
        self.heartChance = 0.001
        self.speeds = [opcoes.get('VB', 2) + 2, opcoes.get('VM', 2) + 5]
        self.biomeName = 'netherHard'
        self.sprites = {
            'grass': 'netherack.png',
            'rails': 'railsNether.png',
            'water': 'lava.png',
        }
class End(Biome):
    def __init__(self, world):
        super().__init__(world)
        opcoes = world.opcoes
        self.weights = [5, 5,0] # grass water rails
        self.boatChance = 0.07 * opcoes.get('NBarcos', 3)
        self.minecartChance = 0.07 * opcoes.get('NMinecarts', 3)
        self.heartChance = 0.001
        self.speeds = [opcoes.get('VB', 2) + 4, opcoes.get('VM', 2) + 8]
        self.stickTo = ['boat', 'grass']
        self.biomeName = 'end'
        self.sprites = {
            'grass': 'endstone.png',
            'water': 'void.png',
            'boat': 'elitra.png'
        }
        self.previousRow =[]
    def new_row(self, y=0):
        row = super().new_row(y)
        remove = random.choices(range(10), k=4)
        while set(remove) == set(self.previousRow):
            remove = random.choices(range(10), k=4)
        self.previousRow = remove
        for i in remove:
            if row[i].entity_type == 'grass':
                row[i].entity_type = 'water'
                row[i].image = sprites['water']
        
        return row
def can_reach_last_layer(grid):
    gridCopy = [row.copy() for row in grid]
    posInicial = [len(grid) - 1, grid[-1].index('P')]
    new_pos = posInicial
    found = False
    direction = 1
    for i in range(100):
        print(new_pos)
        if new_pos[0] == 0:
            found = True
        if grid[new_pos[0]-1][new_pos[1]] == 'X':
            new_pos = [new_pos[0]-1, new_pos[1]]
        elif grid[new_pos[0]][new_pos[1]+direction] == 'X':
            new_pos = [new_pos[0], new_pos[1]+direction]
        elif grid[new_pos[0]][new_pos[1]-direction] == 'X':
            new_pos = [new_pos[0], new_pos[1]-direction]
        else:
            direction = -direction
            new_pos = posInicial
            grid = [row.copy() for row in gridCopy]

        grid[new_pos[0]][new_pos[1]] = ' '
    if found:
        return True
    else:
        return False