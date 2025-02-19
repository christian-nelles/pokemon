import pygame
import random
import json
import requests
import sys
from io import BytesIO
from evolution import gain_experience

pygame.init()

# Screen Settings
WIDTH, HEIGHT = 1280, 750
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("fight Pokémon")

battle_grass = pygame.image.load("images/battle_grass-resize (2).png")
clock = pygame.time.Clock()

def save_inventory(data):
    with open("inventaire.json", "w") as f:
        json.dump(data, f, indent=4)

def main_fight():
    with open("pokemon.json", "r", encoding="utf-8") as file:
        pokemon_data = json.load(file)
    with open("inventaire.json", "r", encoding="utf-8") as file:
        inventaire_data = json.load(file)
    def load_inventory():
        with open("inventaire.json", "r") as f:
            return json.load(f)


    value1 = "1"
    intvalue2 = random.randint(19, 19)
    value2 = f"{intvalue2}"
    pokemon01 = inventaire_data[value1]
    value1 = pokemon01.get("id")

    if pokemon_data:
        pokemon1 = pokemon_data[value1]
        pokemon2 = pokemon_data[value2]



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
    response2 = requests.get(pokemon2.get("sprites").get('front_normal'))
    image_pokemon2 = pygame.image.load(BytesIO(response2.content))
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
            print(power)
            if power == None:
                damage = 0
                return damage
            else:
                type_multiplier = other.calculate_type_multiplier(attack_type)
                critical = 2 if random.random() < 0.04167 else 1
                print(power)
                if power == None:
                    power = 0
                damage = max(1, ((((((2 * self.level * critical) / 5) + 2) * power * (self.attack / other.defense))/50)+2) * random.uniform(0.85, 1) * type_multiplier)
                other.hp = max(0, other.hp - damage)
                return damage

    player_pokemon = Pokemon(
        pokemon1.get("name"),
        pokemon1.get("stats").get('hp'),
        pokemon1.get("stats").get("attack"),
        pokemon1.get("stats").get("defense"),
        5,
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
        player_text = font.render(f"{player_pokemon.name} HP: {int(player_pokemon.hp)}/{player_pokemon.max_hp}", True, BLACK)
        enemy_text = font.render(f"{enemy_pokemon.name} HP: {int(enemy_pokemon.hp)}/{enemy_pokemon.max_hp}", True, BLACK)
        screen.blit(battle_grass, (0, 0))

        screen.blit(player_text, (700, 550))
        screen.blit(enemy_text, (500, 100))
        screen.blit(pygame.font.Font(None, 40).render(f"{moves}", True, WHITE), (500, 200))

        # Health Bar
        pygame.draw.rect(screen, RED, (700, 600, 200, 20))
        pygame.draw.rect(screen, GREEN, (700, 600, 200 * (player_pokemon.hp / player_pokemon.max_hp), 20))

        pygame.draw.rect(screen, RED, (500, 150, 200, 20))
        pygame.draw.rect(screen, GREEN, (500, 150, 200 * (enemy_pokemon.hp / enemy_pokemon.max_hp), 20))

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
                elif event.key == pygame.K_RETURN and player_turn:
                    # Use the selected move
                    selected_move = moves
                    power = pokemon1.get("moves").get(selected_move).get("power")
                    attack_type = pokemon1.get("moves").get(selected_move).get("type")
                    damage = player_pokemon.attack_pokemon(enemy_pokemon, power, attack_type)
                    print(f"{player_pokemon.name} deals {damage} damage to {enemy_pokemon.name}!")
                    player_turn = False

                elif event.key == pygame.K_RETURN and enemy_pokemon.hp > 0.9:
                    available_moves = list(pokemon2.get("moves").keys())  # Liste des noms des attaques
                    selected_move = random.choice(available_moves)
                    power = pokemon2.get("moves").get(selected_move).get("power")
                    attack_type = pokemon2.get("moves").get(selected_move).get("type")
                    damage = enemy_pokemon.attack_pokemon(player_pokemon, power, attack_type)
                    print(f"{enemy_pokemon.name} deals {damage} damage to {player_pokemon.name}!")
                    player_turn = True

        response1 = requests.get(pokemon1.get("sprites").get('back_normal'))
        response2 = requests.get(pokemon2.get("sprites").get('front_normal'))
        
        image_pokemon1 = pygame.image.load(BytesIO(response1.content))
        image_pokemon2 = pygame.image.load(BytesIO(response2.content))

        screen.blit(pygame.transform.scale(image_pokemon1, (900, 900)), (-200, 200))
        screen.blit(pygame.transform.scale(image_pokemon2, (500, 500)), (730, 0))
        # Verify if the fight ends
        if player_pokemon.hp < 1 or enemy_pokemon.hp < 1:
            running = False
            if enemy_pokemon.hp < 1:
                print(f"{player_pokemon.name} a gagné le combat !")
                inventory = load_inventory()
                
                # Appel de la fonction pour gérer l'expérience et l'évolution
                gain_experience(inventory, player_pokemon, pokemon2.get("base_experience"), pokemon1.get("id"))
                
                save_inventory(inventory)

        pygame.display.flip()
        pygame.time.Clock().tick(60)