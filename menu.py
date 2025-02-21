import pygame
import sys
import time
from intro import main_intro
from pokedex import main_pokedex
from adding_pokemon import main_add

pygame.init()

WIDTH, HEIGHT = 1280, 750
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('pokemon')

value = "pos"
state = 1
background1 = pygame.image.load('images/menu/frame_0.gif')
background1 = pygame.transform.scale(background1, (WIDTH, HEIGHT))
background2 = pygame.image.load('images/menu/frame_1.gif')
background2 = pygame.transform.scale(background2, (WIDTH, HEIGHT))
background3 = pygame.image.load('images/menu/frame_2.gif')
background3 = pygame.transform.scale(background3, (WIDTH, HEIGHT))
background4 = pygame.image.load('images/menu/frame_3.gif')
background4 = pygame.transform.scale(background4, (WIDTH, HEIGHT))
background5 = pygame.image.load('images/menu/frame_4.gif')
background5 = pygame.transform.scale(background5, (WIDTH, HEIGHT))
background6 = pygame.image.load('images/menu/frame_5.gif')
background6 = pygame.transform.scale(background6, (WIDTH, HEIGHT))

def background(value, state):
    if value == "pos":
        if state == 6:
            value = "neg"
        if state == 1:
            screen.blit(background1, (0, 0))
        elif state == 2:
            screen.blit(background2, (0, 0))
        elif state == 3:
            screen.blit(background3, (0, 0))
        elif state == 4:
            screen.blit(background4, (0, 0))
        elif state == 5:
            screen.blit(background5, (0, 0))
        elif state == 6:
            screen.blit(background6, (0, 0))
        state += 1
    elif value == "neg":
        if state == 1:
            value = "pos"
        if state == 1:
            screen.blit(background1, (0, 0))
        elif state == 2:
            screen.blit(background2, (0, 0))
        elif state == 3:
            screen.blit(background3, (0, 0))
        elif state == 4:
            screen.blit(background4, (0, 0))
        elif state == 5:
            screen.blit(background5, (0, 0))
        elif state == 6:
            time.sleep(0.5)
            screen.blit(background6, (0, 0))
        state -= 1
    return value, state


font_text = pygame.font.Font(None, 40)

button_new_game = pygame.Rect(490, 40, 300, 50)
button_continue = pygame.Rect(490, 120, 300, 50)
button_pokedex = pygame.Rect(490, 200, 300, 50)
button_config = pygame.Rect(490, 280, 300, 50)
button_quit = pygame.Rect(490, 360, 300, 50)

def draw_buttons():
    pygame.draw.rect(screen, (255, 255, 255), button_new_game, 2)
    screen.blit(font_text.render('New Games', True, (255, 255, 255)), (560, 50))

    pygame.draw.rect(screen, (255, 255, 255), button_continue, 2)
    screen.blit(font_text.render('Continue', True, (255, 255, 255)), (575, 130))

    pygame.draw.rect(screen, (255, 255, 255), button_pokedex, 2)
    screen.blit(font_text.render('Pokedex', True, (255, 255, 255)), (585, 210))

    pygame.draw.rect(screen, (255, 255, 255), button_config, 2)
    screen.blit(font_text.render('Config', True, (255, 255, 255)), (595, 290))

    pygame.draw.rect(screen, (255, 255, 255), button_quit, 2)
    screen.blit(font_text.render('Quit', True, (255, 255, 255)), (610, 370))

def button_click(pos, running):
    if button_new_game.collidepoint(pos):
        main_intro()
        running = False
    elif button_continue.collidepoint(pos):
        running = False
    elif button_pokedex.collidepoint(pos):
        main_pokedex()
    elif button_config.collidepoint(pos):
        main_add()
    elif button_quit.collidepoint(pos):
        pygame.quit()
        sys.exit()
    return running

running = True
while running:
    value, state = background(value, state)
    draw_buttons()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            running = button_click(event.pos, running)

    pygame.time.Clock().tick(15)

    pygame.display.update()