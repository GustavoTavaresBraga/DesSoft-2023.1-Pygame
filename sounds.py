import pygame
from os import *

MORTE_ATROPELAMENTO_SOUND = 'morte_atropelamento_sound'
MORTE_AFOGAMENTO_SOUND = 'morte_afogamento_sound'
MOVIMENTACAO_JOGADOR_SOUND = 'movimentacao_jogador_sound'

def load_sounds():
    sounds = {}
    sounds[MORTE_ATROPELAMENTO_SOUND] = pygame.mixer.Sound(path.join())
    sounds[MORTE_AFOGAMENTO_SOUND] = pygame.mixer.Sound(path.join())
    sounds[MOVIMENTACAO_JOGADOR_SOUND] = pygame.mixer.Sound(path.join(movimento_player.mp3))
    return sounds