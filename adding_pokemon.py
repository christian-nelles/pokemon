import pygame
import json
import sys
import requests
from io import BytesIO


def main_add():
    # Configuration
    WIDTH, HEIGHT = 1280, 750
    GRID_SIZE = 80
    SCROLL_SPEED = 20  # More visible scroll speed

    # Loading Pokémon data
    with open("pokemon.json", "r", encoding="utf-8") as file:
        pokemon_data = json.load(file)

    background = pygame.image.load("images/menu/frame_5.gif")
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))

    # Initializing Pygame
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('pokemon')

    # Cache to store downloaded images
    sprite_cache = {}
    selected_pokemon = set()  # Stores the IDs of selected Pokémon
    scroll_y = 0  # Scroll position

    # Load saved selections
    try:
        with open("selected.json", "r") as f:
            selected_pokemon = set(json.load(f))
    except FileNotFoundError:
        pass  # If the file does not exist yet, no problem

    def save_selected():
        """Sauvegarde les Pokémon sélectionnés dans selected.json"""
        with open("selected.json", "w") as f:
            json.dump(list(selected_pokemon), f)

    def load_sprites():
        """Télécharge toutes les images des Pokémon avec une barre de chargement."""
        total_pokemon = len(pokemon_data)
        loaded = 0  # Charged Pokémon

        font = pygame.font.Font(None, 36)  # Font to display text

        for poke_id, data in pokemon_data.items():
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            
            url = data["sprites"]["front_normal"]

            if url not in sprite_cache:
                try:
                    response = requests.get(url)
                    sprite = pygame.image.load(BytesIO(response.content))
                    sprite_cache[url] = sprite.copy()
                    # Grayed out version of the sprite
                    sprite_cache[url + "_gray"] = pygame.transform.grayscale(sprite)
                except:
                    sprite_cache[url] = None  # If the image does not load

            # Update loading bar
            loaded += 1
            progress = loaded / total_pokemon  # Progress ratio

            # Clear screen
            screen.blit(background, (0, 0))
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((255, 255, 255, 75))
            screen.blit(overlay, (0, 0))

            # Draw the loading bar
            bar_width = 400
            bar_height = 30
            bar_x = (WIDTH - bar_width) // 2
            bar_y = (HEIGHT - bar_height) // 2

            pygame.draw.rect(screen, (100, 100, 100), (bar_x, bar_y, bar_width, bar_height))  # Gray background
            pygame.draw.rect(screen, (255, 255, 255), (bar_x, bar_y, bar_width * progress, bar_height))  # White bar

            # Show percentage
            text = font.render(f"Chargement... {int(progress * 100)}%", True, (255, 255, 255))
            screen.blit(text, (bar_x + 120, bar_y - 40))

            pygame.display.flip()  # Update display

    def draw_pokemon_grid():
        """Affiche les Pokémon sous forme de mosaïque avec scroll."""
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        screen.blit(background, (0, 0))
        overlay.fill((255, 255, 255, 75))
        screen.blit(overlay, (0, 0))

        col, row = 0, 0

        for poke_id, data in pokemon_data.items():
            sprite = sprite_cache.get(data["sprites"]["front_normal"])
            if sprite:
                x, y = col * GRID_SIZE, scroll_y + row * GRID_SIZE

                # Check if the Pokémon is selected
                if poke_id in selected_pokemon:
                    sprite = sprite_cache.get(data["sprites"]["front_normal"] + "_gray")  # Grayed out version

                screen.blit(sprite, (x + 5, y + 5))

            col += 1
            if col * GRID_SIZE >= WIDTH:
                col = 0
                row += 1

    # Load sprites before displaying
    load_sprites()

    # Calculation of the total height for scrolling
    max_scroll = -(len(pokemon_data) // (WIDTH // GRID_SIZE)) * GRID_SIZE + HEIGHT

    # Main loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:  # Scroll up
                    scroll_y = min(scroll_y + SCROLL_SPEED, 0)
                elif event.button == 5:  # Scroll down
                    scroll_y = max(scroll_y - SCROLL_SPEED, max_scroll)
                elif event.button == 1:  # Left click to select/deselect
                    mouse_x, mouse_y = event.pos
                    col = mouse_x // GRID_SIZE
                    row = (mouse_y - scroll_y) // GRID_SIZE  # Adjust with scroll
                    index = row * 16 + col

                    if 0 <= index < len(pokemon_data):
                        poke_id = list(pokemon_data.keys())[index]

                        if poke_id in selected_pokemon:
                            selected_pokemon.remove(poke_id)  # Deselect
                        else:
                            selected_pokemon.add(poke_id)  # Select
                        
                        save_selected()  # Save changes

        draw_pokemon_grid()
        pygame.display.flip()
