import json
import pygame
import requests
import sys
import random
from io import BytesIO

pygame.init()

WIDTH, HEIGHT = 1280, 750
screen = pygame.display.set_mode((WIDTH, HEIGHT))

with open("pokemon.json", "r", encoding="utf-8") as file:
    pokemon_data = json.load(file)
with open("inventaire.json", "r", encoding="utf-8") as file:
    inventaire_data = json.load(file)

    i = 0
    intvalue2 = random.randint(1, 649)
    value2 = f"{intvalue2}"
    
running = True
while running:
    value1 = inventaire_data[i]
 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN: 
            if event.key == pygame.K_RIGHT:
                i = (i + 1) % len(inventaire_data)
            elif event.key == pygame.K_LEFT:
                i = (i - 1) % len(inventaire_data)

    if pokemon_data:
        pokemon1 = pokemon_data[value1]
        pokemon2 = pokemon_data[value2]

        # print("Nom :", pokemon.get("name"))
        # print("Types :", ", ".join(pokemon.get("types", [])))
        # print("Faiblesses :", ", ".join(pokemon.get("weaknesses", [])))
        # print("Résistances :", ", ".join(pokemon.get("resistances", [])))
        # print("Immunités :", ", ".join(pokemon.get("immunities", [])))
        # print("Stats :", pokemon.get("stats").get('hp'))


        response1 = requests.get(pokemon1.get("sprites").get('back_normal'))
        response2 = requests.get(pokemon2.get("sprites").get('front_normal'))
    
    image_pokemon1 = pygame.image.load(BytesIO(response1.content))
    image_pokemon2 = pygame.image.load(BytesIO(response2.content))

    screen.fill((0, 0, 0))
    screen.blit(pygame.transform.scale(image_pokemon1, (700, 700)), (0, 100))
    screen.blit(pygame.transform.scale(image_pokemon2, (350, 350)), (800, 100))

    pygame.display.update()
    pygame.time.Clock().tick(60)

pygame.quit()