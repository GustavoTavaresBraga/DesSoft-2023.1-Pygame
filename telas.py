import pygame
from sprites import sprites, efeitos_sonoros, toggle_som
from chicken import *
global jogador
import random
# criando classe para a tela inicial do jogo

class TelaInicial():
    def __init__(self, tela):
        self.tela = tela
        self.fonte = pygame.font.Font('assets/MinecraftTen-VGORe.ttf', 30)
        self.fundo = sprites['inicio']
        #adicionando os botões funcionais da tela
        self.botaoPlay = pygame.Rect(55, 405, 425, 40)
        self.botaoRanking = pygame.Rect(55, 460, 425, 40)
        self.botaoSair = pygame.Rect(275, 585, 210, 40)
        self.botaoOptions = pygame.Rect(55, 585, 210, 40)
        self.botaoTutorial = pygame.Rect(5,585, 40, 42 )
        # variaveis como falsas, caso cliquem no botão elaa mudam para verdadeiras, e permitem a troca de tela
        self.play = False
        self.options = False
        self.ranking = False
        self.tutorial = False
        self.TextBox = TextBox(self.fonte, tela)
    def desenha(self):  #para o usuario escrever o nome
        self.tela.blit(self.fundo, (0, 0))
        self.TextBox.desenha()
        pygame.display.update()

    #atualização da tela inicial
    def update(self):
        for event in pygame.event.get():
            self.TextBox.escreve(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left mouse button click
                mouse_x, mouse_y = event.pos
                #condições para checar se clicaram em algum botão, e se sim, para ativar o sons de clique
                if self.botaoPlay.collidepoint(mouse_x, mouse_y):
                    self.play = True
                    efeitos_sonoros['click_som'].play()
                elif self.botaoRanking.collidepoint(mouse_x, mouse_y):
                    self.ranking = True
                    efeitos_sonoros['click_som'].play()
                elif self.botaoOptions.collidepoint(mouse_x, mouse_y):
                    self.options = True 
                    efeitos_sonoros['click_som'].play()
                elif self.botaoTutorial.collidepoint(mouse_x, mouse_y):
                    self.tutorial = True
                    efeitos_sonoros['click_som'].play()
                elif self.botaoSair.collidepoint(mouse_x, mouse_y):
                    pygame.quit()
                    return False
        return True
    def troca_tela(self):
        # função para trocar as telas, utilizando as variaveis da função init
        if self.play:
            return TelaJogo(self.tela, self.TextBox.text)
        elif self.ranking:
            return TelaRanking(self.tela)
        elif self.options:
            return TelaOptions(self.tela)
        elif self.tutorial:
            return TelaTutorial(self.tela)
        else:
            return self

#criando classe da tela do jogo
class TelaJogo:
    def __init__(self, tela, nome='',opcoes= None):
        # chamando as sprites a serem utilizadas inicialmente
        sprites['grass'] = pygame.transform.scale(pygame.image.load('assets/sprites/grass.png'), (50, 50))
        sprites['rails'] = pygame.transform.scale(pygame.image.load('assets/sprites/rails.png'), (50, 50))
        sprites['water'] = pygame.transform.scale(pygame.image.load('assets/sprites/water.png'), (50, 50))
        sprites['boat'] = pygame.transform.scale(pygame.image.load('assets/sprites/boat.png'), (50, 50))
        # a variavel opções, é para caso o usuario tenha customizado o jogo na aba de opções no inicio
        # essa variavel agrupa um dicionario as utilidades escolhidades
        self.opcoes = opcoes
        if self.opcoes == None: # caso o usuario não tenha personalizado, ele jogara no modo clasico, com as opções padrões:
            self.opcoes = {'Vidas': 3,'speed': 2, 'NBarcos': 6, 'NMinecarts': 5, 'VB': 4, 'VM': 4, 'Efeitos': True, 'Musica': True}
        self.frame = 0
        self.tela = tela
        self.y = 0
        self.speedAnterior = 0
        self.speedAnteriorCart = 0
        self.clock = pygame.time.Clock()
        self.player = Player()
        self.fonte  = pygame.font.Font(None, 36)
        self.fonte2  = pygame.font.Font('assets/MinecraftTen-VGORe.ttf', 40)
        self.nome = nome
        self.speed = self.opcoes['speed']
        for i in range(17): #criando as fileiras de entities na tela do jogo
            self.nova_fileira(y=800-(i*50)) # preenchendo as fileiras com as sprites
    def nova_fileira(self, y=0):
        block = random.choice(['grass', 'water', 'rails', 'grass', 'rails', 'grass', 'water', 'rails']) #opções das sprites que podem ser escolhidas inicialmete, algumas possuem mais chances de serem escolhidas
        if y > 500 and y <850:  #condição para o jogador não nascer em cima de uma sprite de water ou rails, e sim sobre um bloco de grass
            block = 'grass'

        direction = random.choice([1, -1])    #escolhendo aleatoriamente a direção dos barcos e carrinhos
        speed = random.randint(1, 8)
        
        # garantir que ao menos um obstaculo/boat seja gerado
        gerouObstaculo = False
        for i in range(10):
            if block == 'water': Water(self.player, i * 50 + 25, y)
            if block == 'rails': Rails(self.player, i * 50 +25, y)
            elif block == 'grass': Grass(self.player, i * 50 +25, y)

        for i in range(10):
            if block == 'water' and random.random() < 0.25:
                Boat(self.player, i * 50 + 25, y, speed*direction)
                gerouObstaculo = True
            if block == 'rails' and random.random() < 0.25:
                Minecart(self.player, i * 50 + 25, y, speed*direction)
                gerouObstaculo = True
            if not gerouObstaculo and i == 5:
                if block == 'water':
                    Boat(self.player, i * 50 + 25, y, speed*direction)
                elif block == 'rails':
                    Minecart(self.player, i * 50 + 25, y, speed*direction)
    def salvar_highscore(self):     #salvando a pontuação do jogador
        if self.nome != '' and self.nome != 'escreva seu nome':
            string = '\n'+self.nome+','+str(self.player.score)
            with open('assets/scores.csv', 'a') as f:
                f.write(string)
                print(string)
    def update(self):       #função para atualizar a tela
        if self.y >= int(50/self.player.speed): # Gerar uma nova fileira em cima
            self.nova_fileira()
            self.y = 0
        self.y += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
        self.player.update()
        self.clock.tick(30)
        if self.player.score >= 100: # caso o jogador tenha mais de 200 pontos, as sprites mudam para o end
            sprites['grass'] = pygame.transform.scale(pygame.image.load('assets/sprites/endstone.png'), (50, 50))
            sprites['rails'] = pygame.transform.scale(pygame.image.load('assets/sprites/railsEnd.png'), (50, 50))
            sprites['water'] = pygame.transform.scale(pygame.image.load('assets/sprites/void.png'), (50, 50))
            sprites['boat'] = pygame.transform.scale(pygame.image.load('assets/sprites/elitra.png'), (50, 50))
        elif self.player.score >= 50: # caso o jogador tenha mais de 100 pontos, as sprites mudam para o nether
            sprites['grass'] = pygame.transform.scale(pygame.image.load('assets/sprites/netherack.png'), (50, 50))
            sprites['rails'] = pygame.transform.scale(pygame.image.load('assets/sprites/railsNether.png'), (50, 50))
            sprites['water'] = pygame.transform.scale(pygame.image.load('assets/sprites/lava.png'), (50, 50))
        return True
    
    def desenha(self):      #desenhando a pontuação e a quantidade de vidas do jogador
        self.tela.fill((255, 255, 255))
        for i in self.player.entities:
            self.tela.blit(i.image, i.rect)
        print(self.player.immunity)
        self.tela.blit(self.player.image, self.player.rect)
        t = "pontuacao: " + str(self.player.score)
        textoVidas = self.fonte2.render(str(self.player.vidas), True, (255, 255, 255))
        self.tela.blit(textoVidas, (20, 10))
        self.tela.blit(sprites['coracao'], (50, 10))
        text = self.fonte.render(t, True, (255, 255, 255))
        self.tela.blit(text, (300, 10))
        pygame.display.update()
    
    def troca_tela(self):
        if self.player.morreu:
            pygame.mixer_music.stop()
            self.salvar_highscore()
            return TelaMorte(self.tela)
        else:
            return self 
        
#criando classe da tela de ranking
class TelaRanking():
    def __init__(self, tela):
        self.ranking = {}
        self.tela = tela
        self.fundo = sprites['ranking']
        with open('assets/scores.csv', 'r') as scores: #lendo o arquivo de pontuações
            for line in scores:
                nome, score = line.split(',')
                self.ranking[nome] = int(score)
        self.ranking = sorted(self.ranking.items(), key=lambda x: x[1], reverse=True) #ordenando as pontuações
        self.fonte  = pygame.font.Font('assets/MinecraftTen-VGORe.ttf', 30) 
        self.botaoSair = pygame.Rect(0, 0, 100, 50)
        self.voltar = False
    def desenha(self): 
        self.tela.fill((0, 0, 0))
        self.tela.blit(self.fundo, (0,0))
        texto1 = self.fonte.render('voltar', True, (255, 255, 255))
        self.tela.blit(texto1, (0, 0))
        for i in range(len(self.ranking)): #escrevendo as pontuações na tela
            nome, score = self.ranking[i]
            text = self.fonte.render(str(i+1)+'. '+nome+' - '+str(score), True, (255, 255, 255))
            self.tela.blit(text, (100, 100+i*50))
        pygame.display.update()

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.botaoSair.collidepoint(event.pos) or (event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE): # Left mouse button click
                self.voltar = True 
                efeitos_sonoros['click_som'].play()
        return True
    def troca_tela(self):
        if self.voltar:
            return TelaInicial(self.tela)
        else:
            return self

# criando classe da tela de opções
class TelaOptions():
    def __init__(self, tela):
        #criando os botoes 
        self.tela, self.fundo, self.fonte, self.voltar, self.play = tela, sprites['ranking'], pygame.font.Font('assets/MinecraftTen-VGORe.ttf', 30), False, False
        self.botoes = {name: sprites[name].get_rect() for name in ['botaoVoltar', 'botaoJogar', 'botaospeed', 'botaoMusica', 'botaoEfeitos', 'botaoNBarcos', 'botaoNMinecarts', 'botaoVidas', 'botaoVB', 'botaoVM']}
        self.opcoes = {'Vidas': 1,'speed': 2, 'NBarcos': 3, 'NMinecarts': 3, 'VB': 2, 'VM': 2, 'Efeitos': True, 'Musica': True}
        #posiciona botoes
        for x, y, name in [(250, 300, 'botaoNBarcos'), (250, 350, 'botaoNMinecarts'), (250, 250, 'botaospeed'), (150, 500, 'botaoEfeitos'), (350, 500, 'botaoMusica'), (250, 400, 'botaoVB'), (250, 450, 'botaoVM'), (400, 640, 'botaoVoltar'), (250, 130, 'botaoJogar'), (250, 200, 'botaoVidas')]:
            for n in (name if isinstance(name, list) else [name]):
                self.botoes[n].centerx, self.botoes[n].centery = x, y

    def desenha(self):
        self.tela.fill((0,0,0)) 
        self.tela.blit(self.fundo, (0,0))   #colocando imgaem de fundo
        [self.tela.blit(sprites[name], self.botoes[name]) for name in self.botoes.keys()]   #colocando os botões
        for i in range(6):
            text = self.fonte.render(str(list(self.opcoes.values())[i]), True, (210, 210, 210))
            self.tela.blit(text, (400, 187+i*50))

        pygame.display.update()

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for name in self.botoes.keys():
                    if self.botoes[name].collidepoint(event.pos):
                        if name in ['botaospeed', 'botaoNBarcos', 'botaoNMinecarts', 'botaoVidas', 'botaoVB', 'botaoVM']:
                            efeitos_sonoros['click_som'].play()
                            self.opcoes[name[5:]] = self.opcoes[name[5:]] % 9 + 1   #aumentando a quantidade de cada categoria de opção
                        elif name == 'botaoEfeitos': #pausando ou não os efeitos sonoros
                            toggle_som()
                            efeitos_sonoros['click_som'].play()
                        elif name == 'botaoMusica':     #pausando ou não a musica
                            efeitos_sonoros['click_som'].play()
                            pygame.mixer.music.pause() if pygame.mixer.music.get_busy() else pygame.mixer.music.unpause()
                            
                        elif name == 'botaoVoltar': self.voltar = True, efeitos_sonoros['click_som'].play()
                        elif name == 'botaoJogar': self.play = True, efeitos_sonoros['click_som'].play()
            elif event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE:
                self.voltar = True
        return True
    
    def troca_tela(self):
        if self.voltar:
            return TelaInicial(self.tela)
        elif self.play:
            return TelaJogo(self.tela, opcoes = self.opcoes)
        else:
            return self
        
#criando classe da tela de tutorial
class TelaTutorial():
    def __init__(self, tela):
        self.tela = tela
        self.fundo = sprites['tutorial']
        self.fonte = pygame.font.Font('assets/MinecraftTen-VGORe.ttf', 30)
        self.botaoSair = pygame.Rect(200, 700, 105, 25)
        self.voltar = False
    
    def desenha(self):
        self.tela.blit(self.fundo, (0,0))   #colocando a sprite de fundo
        text = self.fonte.render('voltar', True, (255, 255, 255))
        self.tela.blit(text, (200, 700))   # colocando o botã de voltar

    def update(self):
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.botaoSair.collidepoint(event.pos) or (event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE): # Left mouse button click
                self.voltar = True
                efeitos_sonoros['click_som'].play()
        return True
    def troca_tela(self):
        if self.voltar:
            return TelaInicial(self.tela)
        else:
            return self
        
#criando classe da tela de morte
class TelaMorte:
    def __init__(self, tela):
        self.tela = tela
        self.fonte = pygame.font.Font('assets/MinecraftTen-VGORe.ttf', 60)
        self.fonte2 = pygame.font.Font('assets/MinecraftTen-VGORe.ttf', 36)
        efeitos_sonoros['wasted_som'].play()
        self.botaoVoltar = pygame.Rect(200, 700, 150, 40) #botão para voltar a tela inicial
        self.botaoVoltar.centerx, self.botaoVoltar.centery = 250, 700
        self.inicio = False
        for nome, som in efeitos_sonoros.items():
            if nome != 'wasted_som':
                som.stop()
    def grayscale(self, tela): #função para fazer a tela de jogo para de descer, e receber um filto que faz a tela receber uma lente cinza
        arr = pygame.surfarray.array3d(tela)
        # weights are from the "luma" color space
        luma = arr[:,:,0]*0.3 + arr[:,:,1]*0.59 + arr[:,:,2]*0.11
        arr[:,:,0] = luma
        arr[:,:,1] = luma
        arr[:,:,2] = luma
        return pygame.surfarray.make_surface(arr)

    def desenha(self):  #desenhando mensagem e botão de voltar
        text = self.fonte.render("WASTED", 1, (255,255,255))
        textoVoltar = self.fonte2.render('voltar', True, (255, 255, 255))
        textpos = text.get_rect(centerx=250, centery=400)

        # Convert screen to grayscale
        gray_tela = self.grayscale(self.tela)   #tranformando a tela em cinza

        # Draw gray-scaled image on the main screen
        self.tela.blit(gray_tela, (0,0))

        # Draw "WASTED" in the center of the screen
        self.tela.blit(text, textpos)
        self.tela.blit(textoVoltar, (190, 685))


        pygame.display.update()

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.botaoVoltar.collidepoint(event.pos) or (event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE): # Left mouse button click
                self.inicio = True
                efeitos_sonoros['wasted_som'].stop()
        return True

    def troca_tela(self):
        if self.inicio:
            pygame.mixer_music.play(-1)
            return TelaInicial(self.tela)
        return self