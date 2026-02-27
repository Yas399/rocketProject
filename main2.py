import pygame
import sys
import random
import os
from simulation_mode import run_simulation
from mission_shakti import  run_gaame
# ================== INIT (ONLY ONCE) ==================
pygame.init()

WIDTH, HEIGHT = 1000, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mission Viksit Bharat 🚀")
clock = pygame.time.Clock()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def sound_path(filename):
    return os.path.join(BASE_DIR, filename)

# Load audio ONCE
    # Background Space Ambience (loops forever)
pygame.mixer.music.load(sound_path("space_ambience.mp3"))
pygame.mixer.music.set_volume(0.7)
pygame.mixer.music.play(-1)

    # Sound Effects
rocket_sound = pygame.mixer.Sound(sound_path("rocket_engine.wav"))
rocket_sound.set_volume(10.5)

explosion_sound = pygame.mixer.Sound(sound_path("explosion.wav"))
explosion_sound.set_volume(0.9)

storm_sound = pygame.mixer.Sound(sound_path("storm_sound.wav"))
storm_sound.set_volume(0.8)


# Fonts ONCE
font = pygame.font.SysFont("arial", 22)
big_font = pygame.font.SysFont("arial", 40)
title_font = pygame.font.SysFont("arial", 32)

SPACE = (5, 5, 25)
STAR = (200, 200, 200)

# ======================================================
# ================== MAIN MENU =========================
# ======================================================

def main_menu():

    menu_options = ["Game Mode", "Simulation Mode", "Quit"]
    selected = 0

    stars = [[random.randint(0, WIDTH), random.randint(0, HEIGHT)] for _ in range(100)]

    while True:
        dt = clock.tick(60) / 1000
        screen.fill(SPACE)

        # Star background
        for star in stars:
            star[1] += 40 * dt
            if star[1] > HEIGHT:
                star[1] = 0
                star[0] = random.randint(0, WIDTH)
            pygame.draw.circle(screen, STAR, star, 1)

        # Title
        screen.blit(title_font.render("MISSION VIKSIT BHARAT 🚀", True, (255,255,255)), (345,120))
        screen.blit(font.render("Women Leading Space Navigation Technology", True, (255,215,0)), (320,170))

        # Menu
        for i, option in enumerate(menu_options):
            color = (0,255,200) if i == selected else (255,255,255)
            text = big_font.render(option, True, color)
            screen.blit(text, (WIDTH//2 - text.get_width()//2, 260 + i*70))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(menu_options)
                if event.key == pygame.K_UP:
                    selected = (selected - 1) % len(menu_options)
                if event.key == pygame.K_RETURN:

                    if menu_options[selected] == "Game Mode":
                        run_gaame(screen, clock, explosion_sound, storm_sound, font, big_font, title_font)

                    elif menu_options[selected] == "Simulation Mode":
                        run_simulation()

                    elif menu_options[selected] == "Quit":
                        pygame.quit()
                        sys.exit()


if __name__ == "__main__":
    main_menu()