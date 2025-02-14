import json
import pygame
import requests
import sys
from io import BytesIO

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))

with open("pokemon.json", "r", encoding="utf-8") as file:
    pokemon_data = json.load(file)

value1 = input("pokemon : ")
# value2 = input("numero du 2eme pokemon : ")

if pokemon_data:
    pokemon1 = pokemon_data[value1]
    # pokemon2 = pokemon_data[value2]

    # print("Nom :", pokemon.get("name"))
    # print("Types :", ", ".join(pokemon.get("types", [])))
    # print("Faiblesses :", ", ".join(pokemon.get("weaknesses", [])))
    # print("Résistances :", ", ".join(pokemon.get("resistances", [])))
    # print("Immunités :", ", ".join(pokemon.get("immunities", [])))
    # print("Stats :", pokemon.get("stats").get('hp'))


# image_pokemon1 = pygame.image.load('https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/1.png')
# # image_pokemon2 = pygame.image.load(pokemon2.get("stats"))
    response1 = requests.get(pokemon1.get("sprites").get('front_normal'))
    # response1 = requests.get(pokemon1["sprite"]["front_normal"])

# response2
 
image_pokemon1 = pygame.image.load(BytesIO(response1.content))
# image_pokemon2 = pygame.image.load(BytesIO(response2.content))

running = True
while running:
    screen.fill((0, 0, 0))
    screen.blit(image_pokemon1, (400, 300))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.update()

pygame.quit()