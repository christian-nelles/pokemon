import pygame
import sys
import json

# Initializing Pygame
pygame.init()

# Window Settings
WIDTH, HEIGHT = 1280, 750
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('pokemon')

#  Loading images
intro_background = pygame.image.load('images/intro_background.png')
intro_bag = pygame.image.load('images/intro_bag.png')
intro_pokeball1 = pygame.image.load('images/intro_pokeball1.png')
intro_pokeball2 = pygame.image.load('images/intro_pokeball2.png')
intro_pokeball3 = pygame.image.load('images/intro_pokeball3.png')

# Resizing images
intro_background = pygame.transform.scale(intro_background, (WIDTH, HEIGHT))
intro_bag = pygame.transform.scale(intro_bag, (440, 256))
intro_pokeball1 = pygame.transform.scale(intro_pokeball1, (92, 80))
intro_pokeball2 = pygame.transform.scale(intro_pokeball2, (92, 80))
intro_pokeball3 = pygame.transform.scale(intro_pokeball3, (92, 80))

# Definition of positions and associated Pokémon
pokeballs = [
    {"image": intro_pokeball1, "pos": (300, 250), "name": "Arcko", "id": "252", "move1": "pound", "move2": "leer"},
    {"image": intro_pokeball2, "pos": (600, 360), "name": "Poussifeu", "id": "255", "move1": "scratch", "move2": "growl"},
    {"image": intro_pokeball3, "pos": (900, 220), "name": "Gobou", "id": "258", "move1": "tackle", "move2": "growl"}
]

font = pygame.font.Font(None, 40)
selected_pokemon = None

# Function to update `inventory.py`
def update_inventory(pokemon_id, pokemon_move1, pokemon_move2):
    inventory = {
        str(i): {
            "id": None,
            "exp": None,
            "level": None,
            "attack_list": {
                "first_attack": None,
                "second_attack": None,
                "third_attack": None,
                "fourth_attack": None
            }
        } for i in range(1, 7)
    }

    # Update the first slot with the chosen Pokémon
    inventory["1"]["id"] = pokemon_id
    inventory["1"]["exp"] = 0
    inventory["1"]["level"] = 1
    inventory["1"]["attack_list"]["first_attack"] = pokemon_move1
    inventory["1"]["attack_list"]["second_attack"] = pokemon_move2

    # Convert to JSON format
    inventory_json = json.dumps(inventory, indent=4)

    # Write to `inventory.py`
    with open("inventory.json", "w", encoding="utf-8") as file:
        file.write(f"{inventory_json}")

    existing_data = []

    with open("encounter.json", "w", encoding="utf-8") as file:
        json.dump(existing_data, file, indent=4)

    print(f"Inventaire mis à jour avec le Pokémon ID: {pokemon_id}")

def main_intro():
    running = True
    while running:
        screen.blit(intro_background, (0, 0))
        screen.blit(intro_bag, (450, 50))

        # Mouse position
        mouse_pos = pygame.mouse.get_pos()
        hovered_pokemon = None

        # Pokéball display and hover detection
        for pokeball in pokeballs:
            x, y = pokeball["pos"]
            rect = pygame.Rect(x, y, 92, 80)
            screen.blit(pokeball["image"], (x, y))

            if rect.collidepoint(mouse_pos):
                hovered_pokemon = pokeball["name"]

        # Name display on hover
        if hovered_pokemon:
            text_surface = font.render(hovered_pokemon, True, (255, 255, 255))
            screen.blit(text_surface, (mouse_pos[0] + 10, mouse_pos[1] - 20))

        # Event management
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for pokeball in pokeballs:
                    x, y = pokeball["pos"]
                    rect = pygame.Rect(x, y, 92, 80)
                    if rect.collidepoint(mouse_pos):  # If click on a Pokéball
                        selected_pokemon = pokeball["id"]
                        attack1 = pokeball["move1"]
                        attack2 = pokeball["move2"]
                        print(f"Vous avez sélectionné {pokeball['name']} (ID: {selected_pokemon}) !")
                        update_inventory(selected_pokemon, attack1, attack2)  # Updating the file
                    running = False

        pygame.display.update()
        pygame.time.Clock().tick(60)