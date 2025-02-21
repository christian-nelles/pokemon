import pygame
import random
import math
import time
import json
import requests
from io import BytesIO
from evolution import gain_experience

pygame.init()

# Screen Settings
WIDTH, HEIGHT = 1280, 750
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('pokemon')

battle_grass = pygame.image.load("images/battle_grass-resize (2).png")
clock = pygame.time.Clock()

def save_inventory(data):
    try:
        requests.get("http://clients3.google.com/generate_204", timeout=5)
        with open("inventory.json", "w") as f:
            json.dump(data, f, indent=4)
    except:
        with open("inventory_noco.json", "w") as f:
            json.dump(data, f, indent=4)

def main_fight():
    with open("pokemon.json", "r", encoding="utf-8") as file:
        pokemon_data = json.load(file)
    try :
        requests.get("http://clients3.google.com/generate_204", timeout=5)
        with open("inventory.json", "r", encoding="utf-8") as file:
            inventory_data = json.load(file)
    except:
        with open("inventory_noco.json", "r", encoding="utf-8") as file:
            inventory_data = json.load(file)
    def load_inventory():
        try:
            requests.get("http://clients3.google.com/generate_204", timeout=5)
            with open("inventory.json", "r") as f:
                return json.load(f)
        except:
            with open("inventory_noco.json", "r") as f:
                return json.load(f)

    try:
        requests.get("http://clients3.google.com/generate_204", timeout=5)
        with open("selected.json", "r") as file:
            excluded_values = json.load(file)  

        # Generate a number that is not in excluded_values
        possible_values = []
        for i in range(1, 387):
            if f"{i}" not in excluded_values:
                possible_values.append(f"{i}")

        if possible_values:  # Check that there are still numbers available
            intvalue2 = random.choice(possible_values)
        else:
            print("Erreur : Tous les nombres possibles sont exclus.")
        value2 = f"{intvalue2}"
    except:
        intvalue2 = random.randint(387, 389)
        value2 = f"{intvalue2}"

    value1 = "1"

    pokemon01 = inventory_data[value1]
    value1 = pokemon01.get("id")

    if pokemon_data:
        pokemon1 = pokemon_data[value1]
        pokemon2 = pokemon_data[value2]



    # Start the animation
    image2 = pygame.image.load("images/noir.png")
    battle_scene = pygame.image.load("images/battle_grass-resize (2).png")
    grass = pygame.image.load("images/grass.png")
    image2 = pygame.transform.scale(image2, (WIDTH, HEIGHT))
    battle_scene = pygame.transform.scale(battle_scene, (WIDTH, HEIGHT))
    grass = pygame.transform.scale(grass, (WIDTH, HEIGHT))
    y_top, y_bottom = 0, HEIGHT // 2
    grass_x, grass_y = 0, 10
    running = True
    while running:
        clock.tick(60)
        screen.blit(battle_scene, (0, 0))
        grass_x -= 75
        screen.blit(grass, (grass_x, grass_y))
        screen.blit(grass, (grass_x + WIDTH, grass_y))
        y_top -= 30
        y_bottom += 30
        if y_top <= -HEIGHT // 2:
            running = False
        screen.blit(image2, (0, y_top), (0, 0, WIDTH, HEIGHT // 2))
        screen.blit(image2, (0, y_bottom), (0, HEIGHT // 2, WIDTH, HEIGHT // 2))
        pygame.display.update()
    grass_x, grass_y = 0, 7
    x_exp, y_exp = 75, 1
    pokemon2 = pokemon_data[value2]
    try:
        response2 = requests.get(pokemon2.get("sprites").get('front_normal'))
        image_pokemon2 = pygame.image.load(BytesIO(response2.content))
    except:
        image_pokemon2 = pygame.image.load(f"{pokemon2.get("sprites").get('front_normal')}")
    for _ in range(0, 100):
        clock.tick(60)
        screen.blit(battle_scene, (0, 0))
        image_pokemon2.set_alpha(2 * _ + _ / 2)
        screen.blit(pygame.transform.scale(image_pokemon2, (500, 500)), (730, 0))
        grass_x -= x_exp
        x_exp -= 0.5
        grass_y += y_exp
        y_exp *= 1.035
        if grass_x <= -WIDTH:
            grass_x = 0
        screen.blit(grass, (grass_x, grass_y))
        screen.blit(grass, (grass_x + WIDTH, grass_y))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)

    font = pygame.font.Font(None, 36)

    class Pokemon:
        def __init__(self, name, hp, attack, defense, level, weaknesses, resistances, immunities, id):
            self.name = name
            self.max_hp = hp
            self.hp = hp
            self.attack = attack
            self.defense = defense
            self.level = level
            self.weaknesses = weaknesses
            self.resistances = resistances
            self.immunities = immunities
            self.id = id
        
        def calculate_type_multiplier(self, attack_type):
            multiplier = 1
            if attack_type in self.weaknesses:
                multiplier *= 2
            if attack_type in self.resistances:
                multiplier *= 0.5
            if attack_type in self.immunities:
                multiplier = 0
            
            return multiplier
            
        def attack_pokemon(self, other, power, attack_type):
            if power == None or random.random() < 0.05:
                damage = 0
                return damage
            else:
                type_multiplier = other.calculate_type_multiplier(attack_type)
                critical = 2 if random.random() < 0.04167 else 1
                if power == None:
                    power = 0
                damage = max(1, ((((((2 * self.level * critical) / 5) + 2) * power * (self.attack / other.defense))/50)+2) * random.uniform(0.85, 1) * type_multiplier)
                other.hp = max(0, other.hp - damage)
                return damage

    def save_encountered_pokemon(pokemon_data):
        try:
            # Load existing data if file exists
            try:
                with open("encounter.json", "r", encoding="utf-8") as file:
                    existing_data = json.load(file)
            except (FileNotFoundError, json.JSONDecodeError):
                existing_data = []

            # Check if the Pokémon ID is already in the data
            for pokemon in existing_data:
                if pokemon == pokemon_data:
                    print(f"Le Pokémon avec l'ID {pokemon_data} est déjà enregistré.")
                    return  # Do not add the Pokémon if it already exists

            # Add the Pokémon to existing data
            existing_data.append(pokemon_data)

            # Save updated data to file
            with open("encounter.json", "w", encoding="utf-8") as file:
                json.dump(existing_data, file, indent=4)

            print(f"Le Pokémon avec l'ID {pokemon_data} a été enregistré.")
        except Exception as e:
            print(f"Erreur lors de l'enregistrement du Pokémon rencontré: {e}")


    button_run = pygame.Rect(1120,710,100,100)
    button_attack = pygame.Rect(810,660,100,100)
    def rect():
        pygame.draw.rect(screen,(255, 255, 255),(720,700, 280,50),)
        pygame.draw.rect(screen,(0, 0, 0),(720,700, 280,50), 2)
        screen.blit(font.render('Pokemon', True, (255, 255, 255)),(800,710,100,100))
        pygame.draw.rect(screen,(255, 255, 255),(1000,700, 280,50))
        pygame.draw.rect(screen,(0, 0, 0),(1000,700, 280,50), 2)
        screen.blit(font.render('Run', True, (0, 0, 0)),button_run)
        pygame.draw.rect(screen,(255, 255, 255),(1000,650, 280,50))
        pygame.draw.rect(screen,(0, 0, 0),(1000,650, 280,50), 2)
        screen.blit(font.render('Bag', True, (255, 255, 255)),(1120,660,100,100))
        pygame.draw.rect(screen,(255, 255, 255),(720,650, 280,50))
        pygame.draw.rect(screen,(0, 0, 0),(720,650, 280,50), 2)
        screen.blit(font.render('lllllllll', True, (255, 255, 255)),button_attack)
        pygame.draw.rect(screen,(57, 58, 58),(0,650, 720,100))
        pygame.draw.rect(screen,(255, 255, 255),(0,650, 720,100), 4)



    player_pokemon = Pokemon(
        pokemon1.get("name"),
        pokemon1.get("stats").get('hp'),
        pokemon1.get("stats").get("attack"),
        pokemon1.get("stats").get("defense"),
        pokemon01.get("level"),
        pokemon1.get("weaknesses"),
        pokemon1.get("resistances"),
        pokemon1.get("immunities"),
        pokemon1.get("id")
    )

    moves = pokemon01.get("attack_list").get("first_attack")
    selected_move_index = "first_attack"

    enemy_pokemon = Pokemon(
        pokemon2.get("name"),
        pokemon2.get("stats").get('hp'),
        pokemon2.get("stats").get("attack"),
        pokemon2.get("stats").get("defense"),
        random.randint(1, 5),
        pokemon2.get("weaknesses"),
        pokemon2.get("resistances"),
        pokemon2.get("immunities"),
        None
    )

    player_turn = True
    running = True

    while running:
        pokemon1 = pokemon_data[value1]
        pokemon2 = pokemon_data[value2]
        player_text = font.render(f"{player_pokemon.name} HP: {int(player_pokemon.hp)}/{player_pokemon.max_hp}", True, WHITE)
        enemy_text = font.render(f"{enemy_pokemon.name} HP: {int(enemy_pokemon.hp)}/{enemy_pokemon.max_hp}", True, WHITE)
        screen.blit(battle_grass, (0, 0))

        pygame.draw.rect(screen,(57, 58, 58),(490, 90, 280, 70),)
        screen.blit(enemy_text, (510, 100))

        # Health Bar

        pygame.draw.rect(screen, RED, (510, 125, 200, 20))
        pygame.draw.rect(screen, GREEN, (510, 125, 200 * (enemy_pokemon.hp / enemy_pokemon.max_hp), 20))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    if selected_move_index == "first_attack":
                        selected_move_index = "second_attack"
                        moves = pokemon01.get("attack_list").get("second_attack")
                    elif selected_move_index == "second_attack":
                        selected_move_index = "third_attack"
                        moves = pokemon01.get("attack_list").get("third_attack")
                    elif selected_move_index == "third_attack":
                        selected_move_index = "fourth_attack"
                        moves = pokemon01.get("attack_list").get("fourth_attack")
                    elif selected_move_index == "fourth_attack":
                        selected_move_index = "first_attack"
                        moves = pokemon01.get("attack_list").get("first_attack")
                elif event.key == pygame.K_LEFT:
                    if selected_move_index == "first_attack":
                        selected_move_index = "fourth_attack"
                        moves = pokemon01.get("attack_list").get("fourth_attack")
                    elif selected_move_index == "fourth_attack":
                        selected_move_index = "third_attack"
                        moves = pokemon01.get("attack_list").get("third_attack")
                    elif selected_move_index == "third_attack":
                        selected_move_index = "second_attack"
                        moves = pokemon01.get("attack_list").get("second_attack")
                    elif selected_move_index == "second_attack":
                        selected_move_index = "first_attack"
                        moves = pokemon01.get("attack_list").get("first_attack")
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if player_turn:
                    if button_run.collidepoint(event.pos):
                        if random.random() < 0.5:  # 50% chance of fleeing
                            text = font.render(f"{player_pokemon.name} managed to escape !", True, (255, 255, 255))
                            screen.blit(pygame.transform.scale(image_pokemon1, (900, 900)), (-200, 200))
                            screen.blit(pygame.transform.scale(image_pokemon2, (500, 500)), (730, 0))
                            rect()
                            screen.blit(pygame.font.Font(None, 40).render(f"{moves}", True, BLACK), (810, 660))
                            screen.blit(text, (30, 675))
                            pygame.draw.rect(screen, RED, (30, 700, 200, 20))
                            pygame.draw.rect(screen, GREEN, (30, 700, 200 * (player_pokemon.hp / player_pokemon.max_hp), 20))
                            pygame.display.flip()
                            time.sleep(1)
                            running = False  # Ends the fight
                            break
                        else:
                            text = font.render(f"{player_pokemon.name} failed to escape.", True, (255, 255, 255))
                            screen.blit(pygame.transform.scale(image_pokemon1, (900, 900)), (-200, 200))
                            screen.blit(pygame.transform.scale(image_pokemon2, (500, 500)), (730, 0))
                            rect()
                            screen.blit(pygame.font.Font(None, 40).render(f"{moves}", True, BLACK), (810, 660))
                            screen.blit(text, (30, 675))
                            pygame.draw.rect(screen, RED, (30, 700, 200, 20))
                            pygame.draw.rect(screen, GREEN, (30, 700, 200 * (player_pokemon.hp / player_pokemon.max_hp), 20))
                            pygame.display.flip()
                            time.sleep(1)
                            player_turn = False  # Continue the fight

                    elif button_attack.collidepoint(event.pos):
                        # Use the selected move
                        selected_move = moves
                        power = pokemon1.get("moves").get(selected_move).get("power")
                        attack_type = pokemon1.get("moves").get(selected_move).get("type")
                        damage = player_pokemon.attack_pokemon(enemy_pokemon, power, attack_type)
                        damage = math.floor(damage)
                        text = font.render(f"{player_pokemon.name} deals {damage} damage to {enemy_pokemon.name}!", True, (255, 255, 255))
                        screen.blit(pygame.transform.scale(image_pokemon1, (900, 900)), (-200, 200))
                        screen.blit(pygame.transform.scale(image_pokemon2, (500, 500)), (730, 0))
                        rect()
                        screen.blit(pygame.font.Font(None, 40).render(f"{moves}", True, BLACK), (810, 660))
                        screen.blit(text, (30, 675))
                        pygame.draw.rect(screen, RED, (30, 700, 200, 20))
                        pygame.draw.rect(screen, GREEN, (30, 700, 200 * (player_pokemon.hp / player_pokemon.max_hp), 20))
                        pygame.display.flip()
                        time.sleep(1)
                        player_turn = False

                    if enemy_pokemon.hp > 0.9:
                        time.sleep(1)
                        available_moves = list(pokemon2.get("moves").keys())  # List of attack names
                        selected_move = random.choice(available_moves)
                        power = pokemon2.get("moves").get(selected_move).get("power")
                        attack_type = pokemon2.get("moves").get(selected_move).get("type")
                        damage = enemy_pokemon.attack_pokemon(player_pokemon, power, attack_type)
                        damage = math.floor(damage)
                        text = font.render(f"{enemy_pokemon.name} deals {damage} damage to {player_pokemon.name}!", True, (255, 255, 255))
                        screen.blit(pygame.transform.scale(image_pokemon1, (900, 900)), (-200, 200))
                        screen.blit(pygame.transform.scale(image_pokemon2, (500, 500)), (730, 0))
                        rect()
                        screen.blit(pygame.font.Font(None, 40).render(f"{moves}", True, BLACK), (810, 660))
                        screen.blit(text, (30, 675))
                        pygame.draw.rect(screen, RED, (30, 700, 200, 20))
                        pygame.draw.rect(screen, GREEN, (30, 700, 200 * (player_pokemon.hp / player_pokemon.max_hp), 20))
                        pygame.display.flip()
                        time.sleep(1)
                        player_turn = True
        try:
            response1 = requests.get(pokemon1.get("sprites").get('back_normal'))
            image_pokemon1 = pygame.image.load(BytesIO(response1.content))
        except:
            image_pokemon1 = pygame.image.load(f"{pokemon1.get("sprites").get('back_normal')}")
        try:
            response2 = requests.get(pokemon2.get("sprites").get('front_normal'))
            image_pokemon2 = pygame.image.load(BytesIO(response2.content))
        except:
            image_pokemon2 = pygame.image.load(f"{pokemon2.get("sprites").get('front_normal')}")

        screen.blit(pygame.transform.scale(image_pokemon1, (900, 900)), (-200, 200))
        screen.blit(pygame.transform.scale(image_pokemon2, (500, 500)), (730, 0))
        rect()
        screen.blit(pygame.font.Font(None, 40).render(f"{moves}", True, BLACK), (810, 660))
        # Verify if the fight ends
        screen.blit(player_text, (30, 675))
        pygame.draw.rect(screen, RED, (30, 700, 200, 20))
        pygame.draw.rect(screen, GREEN, (30, 700, 200 * (player_pokemon.hp / player_pokemon.max_hp), 20))
        if player_pokemon.hp < 1 or enemy_pokemon.hp < 1:
            running = False
        if enemy_pokemon.hp < 1:
            text = font.render(f"{player_pokemon.name} win the fight.", True, (255, 255, 255))
            rect()
            screen.blit(text, (30, 675))
            pygame.display.flip()
            time.sleep(1)
            inventory = load_inventory()
            
            # Save the Pokémon encountered
            save_encountered_pokemon(f"{pokemon2.get('id')}")
            
            # Calling the function to manage experience and evolution
            gain_experience(inventory, player_pokemon, pokemon2.get("base_experience"), enemy_pokemon.level)
            
            save_inventory(inventory)
        elif player_pokemon.hp < 1:
            text = font.render(f"{player_pokemon.name} loose the fight.", True, (255, 255, 255))
            rect()
            screen.blit(text, (30, 675))
            pygame.display.flip()
            time.sleep(1)


        pygame.display.flip()
        pygame.time.Clock().tick(60)