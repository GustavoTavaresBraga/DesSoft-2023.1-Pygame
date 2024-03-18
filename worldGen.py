from chicken import *
from sprites import *
import random
class World:
    def __init__(self,screen):
        self.player = Player(self)
        self.entities = []
        self.screen = screen
        self.speed = 2
        self.y = 0
        self.previousSpeed = 0
        self.biomes = {
            0: Plains,
            50: Nether,
            100: End

        }
        self.currentBiome = self.biomes[0](self)
        self.currentBiome.load_sprites()
        for i in range(16):
            self.generate(y=800-(i*50))
    def draw(self):
        for entity in self.entities:
            if entity.entity_type == 'boat' or entity.entity_type == 'minecart':
                continue
            entity.draw(self.screen)
        for entity in self.entities:
            if entity.entity_type == 'boat' or entity.entity_type == 'minecart':
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
                
            elif block == 'rails': 
                row.append(Rails(self.world, i * 50 +25, y))
                if random.random() < self.minecartChance or (i > 8 and not gerouObstaculo):
                    row.append(Minecart(self.world, i * 50 + 25, y, speed*direction))
                    gerouObstaculo = True
            elif block == 'grass': row.append(Grass(self.world, i * 50 +25, y))
        return row
    def load_sprites(self):
        for key, value in self.sprites.items():
            sprites[key] = pygame.transform.scale(pygame.image.load('assets/sprites/'+value), (50, 50))

class Plains(Biome):
    def __init__(self, world):
        super().__init__(world)
        self.weights = [5, 2, 3] # grass water rails
        self.boatChance = 0.35
        self.minecartChance = 0.25
        self.speeds = [2, 8]
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
        self.weights = [4, 5,2] # grass water rails
        self.boatChance = 0.45
        self.minecartChance = 0.2
        self.speeds = [3, 6]
        self.biomeName = 'nether'
        self.sprites = {
            'grass': 'netherack.png',
            'rails': 'railsNether.png',
            'water': 'lava.png',
        }

class End(Biome):
    def __init__(self, world):
        super().__init__(world)
        self.weights = [5, 5,0] # grass water rails
        self.boatChance = 0.2
        self.minecartChance = 0.2
        self.speeds = [6, 10]
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