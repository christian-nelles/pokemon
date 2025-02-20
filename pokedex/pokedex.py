import pygame
import sys
import json
import random

# Load Pokémon from the JSON file
with open("pokemon.json", "r", encoding="utf-8") as file:
    data = json.load(file)

# Check if `data` is a dictionary
if not isinstance(data, dict):
    print("Error: The JSON file must contain a dictionary.")
    sys.exit()

# Build the Pokédex by filtering Pokémon with IDs between 1 and 385
pokedex = {
    p["name"]: p
    for key, p in data.items()
    if 1 <= int(key) <= 385  # Convert the key to an integer for comparison
}

pygame.init()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

display_width = 600
display_height = 400
screen = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption("Pokédex")


font = pygame.font.Font(None, 30)

# List of available Pokémon names
pokemon_names = list(pokedex.keys())

# Select a random Pokémon at the start
current_index = random.randint(0, len(pokemon_names) - 1)

def display_pokemon(index):
    """Displays the Pokémon information for the given index."""
    screen.fill(WHITE)

    pokemon_name = pokemon_names[index]
    pokemon = pokedex[pokemon_name]

    lines = [
        f"Name: {pokemon_name}",
        f"ID: {pokemon['id']}",
        f"Type: {', '.join(pokemon['types'])}",  # Fixed key
        f"Attack: {pokemon['stats']['attack']}",  # Fixed key
        f"Defense: {pokemon['stats']['defense']}",  # Fixed key
        f"HP: {pokemon['stats']['hp']}"  # Fixed key
    ]

    y = 50
    for line in lines:
        text = font.render(line, True, BLACK)
        screen.blit(text, (50, y))
        y += 40

    pygame.display.flip()

# Display the random Pokémon at the start
display_pokemon(current_index)

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:  
                current_index = (current_index + 1) % len(pokemon_names)
            elif event.key == pygame.K_LEFT:  
                current_index = (current_index - 1) % len(pokemon_names)
            display_pokemon(current_index)

pygame.quit()
sys.exit()
