import pygame
import random
import sys

def damage():
    pass

class Combat:
    def __init__(self, player_pokemon, enemy_pokemon):
        self.player_pokemon = player_pokemon
        self.enemy_pokemon = enemy_pokemon
        self.player_turn = True
        self.running = True

    
    def damage(self, attacker, defender):
        return attacker.attack_pokemon(defender)


    def get_pokedex():
        pass

class Menu:
    def __init__(self):
        self = self

    def start_game():
        pass

    def add_pokemon():
        pass

    def get_pokedex():
        pass

pygame.quit()
sys.exit()