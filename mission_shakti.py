def run_gaame(screen, clock, explosion_sound, storm_sound, font, big_font, title_font):
    import pygame
    import random

    # ---------------- SCREEN ----------------
    WIDTH, HEIGHT = screen.get_size()

    SPACE = (5, 5, 25)
    STAR = (200, 200, 200)
    CME_COLOR = (255, 140, 0)
    BLAST_COLOR = (255, 60, 0)

    # ---------------- GAME STATE ----------------
    paused = False
    mission_failed = False
    mission_accomplished = False
    show_intro = True
    incoming_obstacle_warning = False
    camera_shake_timer = 0
    shake_offset = [0, 0]

    # ---------------- ROCKET ----------------
    def reset_rocket():
        return WIDTH // 2, HEIGHT - 120, 0, 0

    rocket_x, rocket_y, vel_x, vel_y = reset_rocket()
    THRUST = 400
    FRICTION = 0.995
    MAX_SPEED = 500

    # ---------------- SCORE ----------------
    score = 0
    high_score = 0
    last_score = 0
    new_high_score = False

    # ---------------- TIME & DIFFICULTY ----------------
    game_time = 0
    difficulty = 1.0
    obstacle_speed_timer = 0
    BASE_OBSTACLE_SPEED = 2.5
    MISSION_TIME = 900  # total run time

    # ---------------- STARS ----------------
    stars = [[random.randint(0, WIDTH), random.randint(0, HEIGHT)] for _ in range(40)]

    # ---------------- SOLAR CME ----------------

    CME_START_TIME = 10
    CME_ACTIVE_TIME = 8
    CME_COOLDOWN = 15
    cme_timer = 0
    cme_cooldown_timer = 0
    cme_active = False
    cme_wave = 1
    storm_particles = []
    cme_vx = 0
    cme_vy = 0


    def spawn_cme(intensity):
        for _ in range(int(3 * intensity)):
            storm_particles.append({
                "x": random.randint(-100, WIDTH),
                "y": random.randint(0, HEIGHT),
                "vx": cme_vx * intensity,
                "vy": cme_vy * intensity,
                "life": random.uniform(1.0, 1.8)
            })

    # ---------------- OBSTACLES ----------------
    def create_obstacle():
        return {
            "x": random.randint(40, WIDTH - 40),
            "y": random.randint(-600, -50),
            "r": random.randint(18, 26),
            "speed": BASE_OBSTACLE_SPEED + difficulty
        }

    def reset_obstacles(count=8):
        return [create_obstacle() for _ in range(count)]

    obstacles = reset_obstacles()

    # ---------------- DRAW ROCKET ----------------
    def draw_rocket(x, y):
        pygame.draw.rect(screen, (210, 210, 220), (x-12, y-25, 24, 50), border_radius=6)
        pygame.draw.polygon(screen, (190, 190, 200),
                            [(x-12, y-25), (x+12, y-25), (x, y-45)])
        pygame.draw.circle(screen, (80, 160, 255), (x, y-10), 6)
        pygame.draw.polygon(screen, (255, 200, 0),
                            [(x-6, y+25), (x+6, y+25), (x, y+38)])

    # ---------------- BLAST ----------------
    blast_particles = []

    def create_blast(x, y):
        for _ in range(30):
            blast_particles.append({
                "x": x,
                "y": y,
                "vx": random.uniform(-150, 150),
                "vy": random.uniform(-150, 150),
                "life": random.uniform(0.3, 0.7)
            })

    # ---------------- MOON ----------------
    MOON_Y = 100
    MOON_RADIUS = 60
    # Load Ghibli-style moon image
    try:
        moon_img = pygame.image.load("moon_ghibli.png").convert_alpha()
        moon_img = pygame.transform.scale(moon_img, (150, 150))
    except:
        moon_img = None

    def draw_moon():
        pygame.draw.circle(screen, (200, 200, 220), (WIDTH//2, MOON_Y), MOON_RADIUS)
        pygame.draw.circle(screen, (180, 180, 200), (WIDTH//2 - 20, MOON_Y - 10), 10)
        pygame.draw.circle(screen, (180, 180, 200), (WIDTH//2 + 25, MOON_Y + 5), 12)

    # ---------------- GAME LOOP ----------------
    running = True
    while running:
        dt = clock.tick(60)/1000

        # Camera shake
        if camera_shake_timer > 0:
            shake_offset[0] = random.randint(-5,5)
            shake_offset[1] = random.randint(-5,5)
            camera_shake_timer -= dt
        else:
            shake_offset = [0,0]

        screen.fill(SPACE)

        # -------- EVENTS --------
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
                if show_intro and event.key == pygame.K_SPACE:
                    show_intro = False
                if event.key == pygame.K_p and not mission_failed and not mission_accomplished:
                    paused = not paused
                if event.key == pygame.K_r and (mission_failed or mission_accomplished):
                    rocket_x, rocket_y, vel_x, vel_y = reset_rocket()
                    obstacles = reset_obstacles()
                    storm_particles.clear()
                    blast_particles.clear()
                    score = 0
                    game_time = 0
                    difficulty = 1.0
                    obstacle_speed_timer = 0
                    paused = False
                    mission_failed = False
                    mission_accomplished = False
                    new_high_score = False
                    cme_active = False
                    cme_wave = 1
                    cme_timer = 0
                    cme_cooldown_timer = 0

        # -------- INTRO SCREEN --------
        if show_intro:
            screen.blit(title_font.render("MISSION SHAKTI", True, (255,255,255)), (390, 140))
            screen.blit(font.render("Pilot: Sunita Williams", True, (200,200,255)), (415, 190))
            screen.blit(font.render("Objective: Navigate space hazards and reach the Moon.", True, (220,220,220)), (270, 240))
            screen.blit(font.render("Press SPACE to Launch Mission", True, (255,215,0)), (370, 330))
            pygame.display.flip()
            continue

        # -------- STARS --------
        for star in stars:
            star[1] += 40 * dt
            if star[1] > HEIGHT:
                star[1] = 0
                star[0] = random.randint(0, WIDTH)
            pygame.draw.circle(screen, STAR, star, 1)

        incoming_obstacle_warning = False

        if not paused and not mission_failed and not mission_accomplished:
            game_time += dt
            score += 1
            obstacle_speed_timer += dt

            # Mission time
            if game_time >= MISSION_TIME:
                mission_accomplished = True

            # -------- DIFFICULTY & OBSTACLES (SLIGHTLY HARDER) --------
            if obstacle_speed_timer >= 90:
                obstacle_speed_timer = 0
                difficulty += 0.25  # increased from 0.15 → 0.25
                for obs in obstacles:
                    obs["speed"] = BASE_OBSTACLE_SPEED + difficulty
                # Add 1 extra obstacle each difficulty increment
                obstacles.append(create_obstacle())

            # -------- PLAYER CONTROLS --------
            keys = pygame.key.get_pressed()
            if keys[pygame.K_a] or keys[pygame.K_LEFT]: vel_x -= THRUST * dt
            if keys[pygame.K_d] or keys[pygame.K_RIGHT]: vel_x += THRUST * dt
            if keys[pygame.K_w] or keys[pygame.K_UP]: vel_y -= THRUST * dt
            if keys[pygame.K_s] or keys[pygame.K_DOWN]: vel_y += THRUST * dt

            # -------- CME (SOLAR STORM) --------
            if game_time >= CME_START_TIME:
                if not cme_active:
                    cme_cooldown_timer += dt
                    if cme_cooldown_timer >= CME_COOLDOWN:
                        cme_active = True
                        cme_timer = 0
                        cme_cooldown_timer = 0
                        storm_sound.play(-1)   # loop storm sound
                        cme_vx = random.choice([-1,1]) * 100
                        cme_vy = random.choice([-0.5,0.5]) * 60
                else:
                    cme_timer += dt
                    rocket_x += cme_vx * dt
                    rocket_y += cme_vy * dt
                    spawn_cme(cme_wave)
                    vel_x += random.choice([-1, 1]) * 40 * dt * cme_wave
                    if cme_timer >= CME_ACTIVE_TIME:
                        cme_active = False
                        cme_wave += 1
                        storm_particles.clear()
                        storm_sound.stop()

            # Rocket movement
            vel_x = max(-MAX_SPEED, min(MAX_SPEED, vel_x))
            vel_y = max(-MAX_SPEED, min(MAX_SPEED, vel_y))
            rocket_x += vel_x * dt
            rocket_y += vel_y * dt
            vel_x *= FRICTION
            vel_y *= FRICTION
            rocket_x = max(20, min(WIDTH - 20, rocket_x))
            rocket_y = max(20, min(HEIGHT - 20, rocket_y))

            # CME draw
            for p in storm_particles[:]:
                p["x"] += p["vx"] * dt
                p["y"] += p["vy"] * dt
                p["life"] -= dt
                if p["life"] <= 0 or p["x"] > WIDTH + 100 or p["x"] < -100 or p["y"] < -50 or p["y"] > HEIGHT + 50:
                    storm_particles.remove(p)
                else:
                    pygame.draw.circle(screen, CME_COLOR, (int(p["x"]), int(p["y"])), 3)

            # Obstacles
            for obs in obstacles:
                obs["y"] += obs["speed"]
                if abs(obs["x"] - rocket_x) < obs["r"] * 1.5:
                    incoming_obstacle_warning = True
                pygame.draw.circle(screen, (170,110,70), (int(obs["x"]), int(obs["y"])), obs["r"])
                if abs(rocket_x - obs["x"]) < obs["r"] and abs(rocket_y - obs["y"]) < obs["r"]:
                    mission_failed = True
                    last_score = score
                    create_blast(rocket_x, rocket_y)
                    explosion_sound.play()
                    camera_shake_timer = 0.5
                    if score > high_score:
                        high_score = score
                        new_high_score = True
                    else:
                        new_high_score = False
                if obs["y"] > HEIGHT:
                    obs.update(create_obstacle())

            draw_rocket(int(rocket_x), int(rocket_y))

        # -------- BLAST DRAW --------
        for b in blast_particles[:]:
            b["x"] += b["vx"] * dt
            b["y"] += b["vy"] * dt
            b["life"] -= dt
            if b["life"] <= 0:
                blast_particles.remove(b)
            else:
                pygame.draw.circle(screen, BLAST_COLOR, (int(b["x"]), int(b["y"])), 4)

        # -------- UI --------
        offset_x, offset_y = shake_offset
        screen.blit(font.render(f"Score: {score}", True, (255,255,255)), (20+offset_x, 20+offset_y))
        if cme_active:
            screen.blit(font.render(" INCOMING SOLAR STORM", True, (255,140,0)), (230+offset_x, 40+offset_y))
        elif incoming_obstacle_warning:
            screen.blit(font.render(" INCOMING OBSTACLE", True, (255,180,80)), (260+offset_x, 70+offset_y))
        if paused:
            screen.blit(big_font.render("PAUSED", True, (255,255,0)), (WIDTH//2 - 80, HEIGHT//2 - 40))
            screen.blit(font.render("We need you to complete the mission. Press P to Resume.", True, (220,220,220)), (270, HEIGHT//2 + 10))

        # Mission accomplished
        if mission_accomplished:
            if moon_img:
                screen.blit(moon_img, (WIDTH//2 - 75, MOON_Y - 75))
            else:
                draw_moon()
            if rocket_y > MOON_Y + 30:
                rocket_y -= 80 * dt
                rocket_x += (WIDTH//2 - rocket_x) * 0.05
            draw_rocket(int(rocket_x), int(rocket_y))
            screen.blit(big_font.render("MISSION ACCOMPLISHED! ", True, (80,255,80)), (WIDTH//2 - 200, HEIGHT//2 - 60))
            screen.blit(font.render("BRAVO, PILOT! YOU DID IT! ", True, (180,255,180)), (WIDTH//2 - 150, HEIGHT//2 - 10))
            screen.blit(font.render(f"Score: {score}", True, (255,255,255)), (WIDTH//2 - 70, HEIGHT//2 + 30))
            if score > high_score:
                high_score = score
                screen.blit(font.render(" NEW HIGH SCORE!", True, (255,215,0)), (WIDTH//2 - 120, HEIGHT//2 + 60))
            screen.blit(font.render("Press R to Restart", True, (200,200,200)), (WIDTH//2 - 95, HEIGHT//2 + 100))

        # Mission failed
        if mission_failed:
            screen.blit(big_font.render("MISSION ABORT", True, (255,80,80)), (WIDTH//2 - 160, HEIGHT//2 - 90))
            screen.blit(font.render(f"Score: {last_score}", True, (255,255,255)), (WIDTH//2 - 70, HEIGHT//2 - 25))
            screen.blit(font.render(f"High Score: {high_score}", True, (255,215,0)), (WIDTH//2 - 95, HEIGHT//2 + 5))
            if new_high_score:
                screen.blit(font.render(" NEW HIGH SCORE!", True, (255,215,0)), (WIDTH//2 - 120, HEIGHT//2 + 35))
            screen.blit(font.render("Press R to Restart", True, (200,200,200)), (WIDTH//2 - 95, HEIGHT//2 + 70))

        pygame.display.flip()
