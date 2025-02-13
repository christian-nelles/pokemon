import pygame
import random   

pygame.init()

# Screen Settings
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("fight Pokémon")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

font = pygame.font.Font(None, 36)

class Pokemon:
    def __init__(self, name, hp, attack, defense):
        self.name = name
        self.max_hp = hp
        self.hp = hp
        self.attack = attack
        self.defense = defense

    def attack_pokemon(self, other):
        damage = max(1, self.attack - other.defense + random.randint(-3, 3))
        other.hp = max(0, other.hp - damage)
        return damage

player_pokemon = Pokemon("Pikachu", 50, 10, 3)
enemy_pokemon = Pokemon("Charmender", 45, 9, 2)

player_turn = True
running = True
player_text = font.render(f"{player_pokemon.name} HP: {player_pokemon.hp}/{player_pokemon.max_hp}", True, BLACK)
enemy_text = font.render(f"{enemy_pokemon.name} HP: {enemy_pokemon.hp}/{enemy_pokemon.max_hp}", True, BLACK)

screen.blit(player_text, (50, 400))
screen.blit(enemy_text, (50, 100))

while running:
    screen.fill(WHITE)

    screen.blit(player_text, (50, 400))
    screen.blit(enemy_text, (50, 100))

    # Health Bar
    pygame.draw.rect(screen, RED, (50, 450, 200, 20))
    pygame.draw.rect(screen, GREEN, (50, 450, 200 * (player_pokemon.hp / player_pokemon.max_hp), 20))

    pygame.draw.rect(screen, RED, (50, 150, 200, 20))
    pygame.draw.rect(screen, GREEN, (50, 150, 200 * (enemy_pokemon.hp / enemy_pokemon.max_hp), 20))

    # Show the Attacking options
    attack_text = font.render("Press Space to Attack", True, BLACK)
    screen.blit(attack_text, (50, 500))

    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            if player_turn:
                damage = player_pokemon.attack_pokemon(enemy_pokemon)
                print(f"{player_pokemon.name} deals {damage} damage to {enemy_pokemon.name}!")
                player_turn = False

            elif enemy_pokemon.hp > 0:
                pygame.time.delay(1000)
                damage = enemy_pokemon.attack_pokemon(player_pokemon)
                print(f"{enemy_pokemon.name} deals {damage} damage to {player_pokemon.name}!")
                player_turn = True

    # Verify if the fights ends
    if player_pokemon.hp == 0 or enemy_pokemon.hp == 0:
        running = False

pygame.quit()         
