import pygame
import sys
import json
import random
import time
import requests
from io import BytesIO


def main_pokedex():
    pygame.init()

    WIDTH = 1280
    HEIGHT = 750
    speed = 0.5

    # Load Pokémon from the JSON file
    with open("pokemon.json", "r", encoding="utf-8") as file:
        data = json.load(file)
    with open("encounter.json", "r", encoding="utf-8") as file:
        count = json.load(file)

    # Check if `data` is a dictionary
    if not isinstance(data, dict):
        print("Error: The JSON file must contain a dictionary.")
        sys.exit()

    # Build the Pokédex by filtering Pokémon with IDs between 1 and 385
    pokedex = {
        p["name"]: p
        for key, p in data.items()
        if 1 <= int(key) <= 386  # Convert the key to an integer for comparison
    }

    background = pygame.image.load("images/8369.png")
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))

    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('pokemon')

    # List of available Pokémon names
    pokemon_names = list(pokedex.keys())

    # Select a random Pokémon at the start
    if not count:
        current_index = 0  # Takes the first Pokémon by default
    else:
        # Otherwise, choose a random ID that is in count
        current_index = random.randint(0, len(pokemon_names) - 1)
        while f"{current_index + 1}" not in count:
            current_index = random.randint(0, len(pokemon_names) - 1)
        

    def wrap_text(text, font, max_width):
        """Wrap text to fit within a given width."""
        words = text.split(' ')
        lines = []
        current_line = ''

        for word in words:
            # Check the width of the current line + the new word
            if font.size(current_line + word)[0] <= max_width:
                # If it fits, add the word to the current line
                current_line += (word + ' ')
            else:
                # If it doesn't fit, start a new line
                lines.append(current_line)
                current_line = word + ' '  # Start new line with the current word

        # Add the last line
        if current_line:
            lines.append(current_line)

        return lines

    def adjust_font_size(text, font, max_width, max_height):
        """Adjust font size to fit the text within the max width and max height."""
        # Start with the current font size
        font_size = font.get_height()

        # Loop to adjust the font size
        while True:
            # Wrap the text with the current font size
            wrapped_text = wrap_text(text, font, max_width)
            
            # Calculate the total height of the wrapped text
            total_height = len(wrapped_text) * font.size('A')[1]  # Height of the text
            
            # If the total height exceeds the max height, reduce the font size
            if total_height > max_height and font_size > 10:
                font_size -= 1
                font = pygame.font.Font(None, font_size)  # Update the font with new size
            else:
                break  # Exit the loop when text fits within the max height

        return font, wrapped_text

    def display_pokemon(index):
        font = pygame.font.Font(None, 50)
        """Displays the Pokémon information for the given index."""
        screen.blit(background, (0, 0))

        pokemon_name = pokemon_names[index]
        pokemon = pokedex[pokemon_name]

        # Store the Pokémon info as strings, not sets
        lines = {
            "Name": pokemon_name,
            "ID": str(pokemon['id']),
            "Type": ' '.join(pokemon['types']),
            "Color": pokemon['color'],
            "Pokedex": ', '.join(pokemon['pokedex_entries'])
        }

        if f"{index + 1}" in count:
            # Render the Pokémon name and blit it to the screen
            screen.blit(font.render(lines["Name"], True, (0, 0, 0)), (300, 95))
            response = requests.get(data[f"{current_index + 1}"].get("sprites").get('front_normal'))
            image = pygame.image.load(BytesIO(response.content))

            # Optionally, you can display more information like Type, ID, etc.
            screen.blit(font.render(lines['Color'], True, (0, 0, 0)), (300, 171))
            # Render First Type at a specific position
            if len(pokemon['types']) > 0:
                first_type = pokemon['types'][0]  # Get the first type
                screen.blit(font.render(first_type, True, (0, 0, 0)), (300, 244))  # Fixed position for first type

            # Render Second Type at a different specific position
            if len(pokemon['types']) > 1:
                second_type = pokemon['types'][1]  # Get the second type
                screen.blit(font.render(second_type, True, (0, 0, 0)), (520, 244))  # Fixed position for second type

            screen.blit(font.render(lines['ID'], True, (0, 0, 0)), (300, 320))
            max_width = 1000  # Adjust this based on the space available
            max_height = 150  # Maximum height for the text area (in pixels)
            pokedex_text = lines['Pokedex']
            # Adjust font size and wrap the text to fit within the space
            font, wrapped_text = adjust_font_size(pokedex_text, font, max_width, max_height)
            # Start blitting the wrapped text to the screen at the desired position
            y_offset = 570  # The starting y position for the Pokedex entry
            for line in wrapped_text:
                screen.blit(font.render(line, True, (0, 0, 0)), (120, y_offset))
                y_offset += font.get_height()  # Move down for the next line
            screen.blit(pygame.transform.scale(image, (300, 300)), (850, 150))
        else:
            screen.blit(font.render(f"{index + 1}", True, (0, 0, 0)), (300, 320))

        pygame.display.flip()


    # Display the random Pokémon at the start
    display_pokemon(current_index)

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
        if pygame.key.get_pressed()[pygame.K_RIGHT]:  
            # Move to the next Pokémon, wrapping between 0 and len(pokemon_names) - 1
            current_index = (current_index + 1) % len(pokemon_names)
            time.sleep(speed)
            speed = max(speed - 0.1, 0.05)
        elif pygame.key.get_pressed()[pygame.K_LEFT]:  
            # Move to the previous Pokémon, wrapping between 0 and len(pokemon_names) - 1
            current_index = (current_index - 1) % len(pokemon_names)
            time.sleep(speed)
            speed = max(speed - 0.1, 0.05)
        else:
            speed = 0.5
        display_pokemon(current_index)
