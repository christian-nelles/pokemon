import pygame
import sys

# Initialize Pygame
pygame.init()

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Create the window
display_width = 600
display_height = 400
screen = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption("Pokédex")

# Define the font
font = pygame.font.Font(None, 30)

# Pokémon data
pokedex = {
    "Pikachu": {"Type": "Electric", "Attack": 55, "Defense": 40, "HP": 35},
    "Bulbasaur": {"Type": "Grass", "Attack": 49, "Defense": 49, "HP": 45},
    "Charmander": {"Type": "Fire", "Attack": 52, "Defense": 43, "HP": 39},
    "Squirtle": {"Type": "Water", "Attack": 48, "Defense": 65, "HP": 44},
}

# Function to display Pokémon information
def display_pokemon(pokemon_name):
    screen.fill(WHITE)
    
    if pokemon_name in pokedex:
        pokemon = pokedex[pokemon_name]
        lines = [
            f"Name: {pokemon_name}",
            f"Type: {pokemon['Type']}",
            f"Attack: {pokemon['Attack']}",
            f"Defense: {pokemon['Defense']}",
            f"HP: {pokemon['HP']}"
        ]
        
        y = 50
        for line in lines:
            text = font.render(line, True, BLACK)
            screen.blit(text, (50, y))
            y += 40
    else:
        text = font.render("Pokémon not found", True, RED)
        screen.blit(text, (50, 50))
    
    pygame.display.flip()

# Main loop
running = True
selected_pokemon = "Pikachu"
display_pokemon(selected_pokemon)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                selected_pokemon = "Pikachu"
            elif event.key == pygame.K_2:
                selected_pokemon = "Bulbasaur"
            elif event.key == pygame.K_3:
                selected_pokemon = "Charmander"
            elif event.key == pygame.K_4:
                selected_pokemon = "Squirtle"
            display_pokemon(selected_pokemon)

pygame.quit()

sys.exit()
