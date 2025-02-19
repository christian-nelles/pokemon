import pygame
from intro import main_intro

# Initialisation de Pygame
pygame.init()

# Paramètres de la fenêtre
WIDTH, HEIGHT = 1280, 750
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Menu Principal")

# Couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Police d'écriture
font_title = pygame.font.Font(None, 80)
font_text = pygame.font.Font(None, 40)

# Texte du menu
press_text = font_text.render("Appuyez sur ENTREE pour continuer", True, WHITE)

# Position du texte
# title_rect = title_text.get_rect(center=(WIDTH // 2, HEIGHT // 3))
press_rect = press_text.get_rect(center=(WIDTH // 2, HEIGHT // 1.5))

# Boucle du menu
running = True
while running:
    screen.fill(BLACK)  # Fond noir

    # Afficher le texte
    # screen.blit(title_text, title_rect)
    screen.blit(press_text, press_rect)

    # Gérer les événements
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:  # Si on appuie sur Entrée
                main_intro()
                running = False  # Sort du menu
            if event.key == pygame.K_SPACE:  # Si on appuie sur Espace
                running = False  # Sort du menu

    pygame.display.update()
    pygame.time.Clock().tick(60)

print("Menu terminé, passage à la suite du jeu.")
