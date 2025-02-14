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

    # Function to get the Pokédex data
    def get_pokedex():
        return {
            "Pikachu": {"Type": "Electric", "Attack": 55, "Defense": 40, "HP": 35},
            "Bulbasaur": {"Type": "Grass", "Attack": 49, "Defense": 49, "HP": 45},
            "Charmander": {"Type": "Fire", "Attack": 52, "Defense": 43, "HP": 39},
            "Squirtle": {"Type": "Water", "Attack": 48, "Defense": 65, "HP": 44},
        }

    # Initialize the Pokédex
    pokedex = get_pokedex()


pygame.quit()
sys.exit()