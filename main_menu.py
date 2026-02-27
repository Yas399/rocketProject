import pygame
import sys
import random
import math
from mission_shakti import run_gaame
from simulation_mode import run_simulation

pygame.init()

# ---------------- WINDOW SETUP ----------------
WIDTH, HEIGHT = 1000, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mission Viksit Bharat 🚀")
clock = pygame.time.Clock()

# ---------------- FONTS ----------------
title_font = pygame.font.SysFont("arial", 48, bold=True)
subtitle_font = pygame.font.SysFont("arial", 24)
menu_font = pygame.font.SysFont("arial", 36)

# ---------------- COLORS ----------------
WHITE = (255, 255, 255)
YELLOW = (255, 215, 0)
HIGHLIGHT = (0, 255, 200)
BACKGROUND = (5, 5, 25)

# ---------------- MENU OPTIONS ----------------
menu_options = ["Game Mode", "Simulation Mode", "Quit"]
selected_index = 0

# ---------------- STARFIELD ----------------
stars = [
    {
        "x": random.randint(0, WIDTH),
        "y": random.randint(0, HEIGHT),
        "size": random.randint(1, 3),
        "speed": random.uniform(20, 80),
        "angle": random.uniform(-math.pi/4, math.pi/4),  # diagonal
        "twinkle": random.randint(1, 30)
    } for _ in range(150)
]

# ---------------- DRAW FUNCTIONS ----------------
def draw_starfield(dt):
    for star in stars:
        # Move star diagonally
        star["x"] += math.cos(star["angle"]) * star["speed"] * dt
        star["y"] += math.sin(star["angle"]) * star["speed"] * dt

        # Wrap around edges
        if star["y"] > HEIGHT:
            star["y"] = 0
            star["x"] = random.randint(0, WIDTH)
        if star["x"] > WIDTH:
            star["x"] = 0
            star["y"] = random.randint(0, HEIGHT)
        if star["x"] < 0:
            star["x"] = WIDTH
            star["y"] = random.randint(0, HEIGHT)

        # Twinkle effect
        star["twinkle"] += 1
        if star["twinkle"] > 30:
            star["size"] = random.randint(1, 3)
            star["twinkle"] = 0

        pygame.draw.circle(screen, WHITE, (int(star["x"]), int(star["y"])), star["size"])

def draw_menu():
    screen.fill(BACKGROUND)
    draw_starfield(1/60)

    # Title
    screen.blit(title_font.render("Mission Viksit Bharat 🚀", True, WHITE), (180, 120))
    screen.blit(subtitle_font.render("Women Leading Space Navigation Technology", True, YELLOW), (160, 200))

    # Menu Options
    mouse_x, mouse_y = pygame.mouse.get_pos()
    for i, option in enumerate(menu_options):
        text_surface = menu_font.render(option, True, HIGHLIGHT if i == selected_index else WHITE)
        text_rect = text_surface.get_rect(center=(WIDTH//2, 320 + i*70))

        # Hover effect with mouse
        if text_rect.collidepoint(mouse_x, mouse_y):
            selected_index_hovered = i
            text_surface = menu_font.render(option, True, HIGHLIGHT)
            screen.blit(text_surface, text_rect)
        else:
            screen.blit(text_surface, text_rect)

# ---------------- MAIN MENU LOOP ----------------
def main_menu():
    global selected_index
    while True:
        draw_menu()
        pygame.display.update()
        dt = clock.tick(60) / 1000  # frame time

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    selected_index = (selected_index + 1) % len(menu_options)
                if event.key == pygame.K_UP:
                    selected_index = (selected_index - 1) % len(menu_options)
                if event.key == pygame.K_RETURN:
                    choose_option()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # left click
                    choose_option(mouse_click=True)

def choose_option(mouse_click=False):
    global selected_index
    if mouse_click:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        for i, option in enumerate(menu_options):
            text_surface = menu_font.render(option, True, WHITE)
            text_rect = text_surface.get_rect(center=(WIDTH//2, 320 + i*70))
            if text_rect.collidepoint(mouse_x, mouse_y):
                selected_index = i
                break

    if menu_options[selected_index] == "Game Mode":
        result = run_gaame()
    elif menu_options[selected_index] == "Simulation Mode":
        result = run_simulation()
    elif menu_options[selected_index] == "Quit":
        pygame.quit()
        sys.exit()

    if result == "menu":
        selected_index = 0

# ---------------- RUN MAIN MENU ----------------
if __name__ == "__main__":
    main_menu()