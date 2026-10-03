import pygame
import random
import math
import sys

pygame.init()

# ============================================================
# SCREEN
# ============================================================

WIDTH = 1280
HEIGHT = 720

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("CHAOS SHOOTER X")

clock = pygame.time.Clock()

# ============================================================
# WORLD
# ============================================================

WORLD_WIDTH = 7000
WORLD_HEIGHT = 7000

# ============================================================
# COLORS
# ============================================================

WHITE = (255,255,255)
BLACK = (10,10,10)

RED = (255,60,60)
GREEN = (0,255,120)
BLUE = (50,120,255)

PURPLE = (190,80,255)
YELLOW = (255,230,0)
CYAN = (0,240,255)

ORANGE = (255,140,0)
GRAY = (90,90,90)

# ============================================================
# SHAKE
# ============================================================

shake = 0

# ============================================================
# PLAYER
# ============================================================

player = {

    "x": WORLD_WIDTH // 2,
    "y": WORLD_HEIGHT // 2,

    "size": 42,

    "speed": 5,
    "sprint": 9,

    "health": 100,
    "max_health": 100,

    "shield": 50,
    "max_shield": 50,

    "weapon": "pistol",

    "coins": 0,

    "xp": 0,
    "level": 1,

    "damage_bonus": 1.0,
    "fire_rate_bonus": 1.0
}

# ============================================================
# WEAPONS
# ============================================================

weapons = {

    "pistol": {
        "damage": 16,
        "rate": 300,
        "speed": 16,
        "spread": 0.03,
        "pellets": 1,
        "color": YELLOW
    },

    "smg": {
        "damage": 7,
        "rate": 70,
        "speed": 18,
        "spread": 0.08,
        "pellets": 1,
        "color": ORANGE
    },

    "burst": {
        "damage": 12,
        "rate": 180,
        "speed": 18,
        "spread": 0.07,
        "pellets": 3,
        "color": YELLOW
    },

    "shotgun": {
        "damage": 10,
        "rate": 650,
        "speed": 15,
        "spread": 0.35,
        "pellets": 8,
        "color": ORANGE
    },

    "sniper": {
        "damage": 120,
        "rate": 1200,
        "speed": 35,
        "spread": 0,
        "pellets": 1,
        "color": CYAN
    },

    "minigun": {
        "damage": 5,
        "rate": 35,
        "speed": 20,
        "spread": 0.12,
        "pellets": 1,
        "color": YELLOW
    },

    "plasma": {
        "damage": 35,
        "rate": 170,
        "speed": 22,
        "spread": 0.05,
        "pellets": 2,
        "color": PURPLE
    },

    "laser": {
        "damage": 6,
        "rate": 10,
        "speed": 45,
        "spread": 0,
        "pellets": 1,
        "color": CYAN
    },

    "rocket": {
        "damage": 0,
        "rate": 700,
        "speed": 11,
        "spread": 0,
        "pellets": 1,
        "color": RED
    },

    "chaos": {
        "damage": 40,
        "rate": 60,
        "speed": 25,
        "spread": 0.5,
        "pellets": 10,
        "color": PURPLE
    }
}

owned_weapons = ["pistol"]

weapon_unlocks = {

    3: "smg",
    6: "burst",
    9: "shotgun",
    12: "sniper",
    15: "minigun",
    18: "plasma",
    21: "laser",
    24: "rocket",
    27: "chaos"
}

# ============================================================
# GAME OBJECTS
# ============================================================

bullets = []
rockets = []
grenades = []
particles = []
explosions = []

enemies = []

boss = None

# ============================================================
# WALLS
# ============================================================

walls = []

for _ in range(120):

    walls.append(

        pygame.Rect(

            random.randint(0, WORLD_WIDTH - 500),
            random.randint(0, WORLD_HEIGHT - 500),

            random.randint(150, 400),
            random.randint(50, 100)
        )
    )

# ============================================================
# GAME STATE
# ============================================================

wave = 1
score = 0

between_waves = False

last_shot = 0
last_grenade = 0

# ============================================================
# FONTS
# ============================================================

font = pygame.font.SysFont(None, 28)
big_font = pygame.font.SysFont(None, 72)

pygame.mouse.set_visible(False)

# ============================================================
# FUNCTIONS
# ============================================================

def camera():

    cam_x = player["x"] - WIDTH // 2
    cam_y = player["y"] - HEIGHT // 2

    cam_x = max(0, min(cam_x, WORLD_WIDTH - WIDTH))
    cam_y = max(0, min(cam_y, WORLD_HEIGHT - HEIGHT))

    return cam_x, cam_y

def collide(rect):

    return any(rect.colliderect(w) for w in walls)

def make_particles(x, y, color, amount):

    for _ in range(amount):

        particles.append({

            "x": x,
            "y": y,

            "dx": random.uniform(-6,6),
            "dy": random.uniform(-6,6),

            "life": random.randint(15,45),

            "color": color,

            "size": random.randint(2,6)
        })

def explode(x, y, radius):

    global shake
    global score

    shake = 20

    explosions.append({

        "x": x,
        "y": y,

        "radius": radius,

        "life": 20
    })

    make_particles(x, y, ORANGE, 90)

    for e in enemies[:]:

        dist = math.hypot(
            e["x"] - x,
            e["y"] - y
        )

        if dist < radius:

            e["hp"] -= 200

            if e["hp"] <= 0:

                enemies.remove(e)

                player["coins"] += 8
                player["xp"] += 10

                score += 30

def spawn_enemy():

    while True:

        x = random.randint(0, WORLD_WIDTH)
        y = random.randint(0, WORLD_HEIGHT)

        if math.hypot(
            x - player["x"],
            y - player["y"]
        ) < 900:
            continue

        rect = pygame.Rect(x,y,40,40)

        if not collide(rect):

            enemy_type = random.choice([

                "normal",
                "normal",
                "normal",

                "fast",

                "tank",

                "elite"
            ])

            hp_scale = 1 + wave * 0.08

            if enemy_type == "normal":

                return {

                    "x": x,
                    "y": y,

                    "size": 40,

                    "speed": 2 + wave * 0.03,

                    "hp": 40 * hp_scale,

                    "color": RED
                }

            if enemy_type == "fast":

                return {

                    "x": x,
                    "y": y,

                    "size": 28,

                    "speed": 4 + wave * 0.05,

                    "hp": 25 * hp_scale,

                    "color": ORANGE
                }

            if enemy_type == "tank":

                return {

                    "x": x,
                    "y": y,

                    "size": 70,

                    "speed": 1.5,

                    "hp": 280 * hp_scale,

                    "color": PURPLE
                }

            if enemy_type == "elite":

                return {

                    "x": x,
                    "y": y,

                    "size": 52,

                    "speed": 3,

                    "hp": 120 * hp_scale,

                    "color": CYAN
                }

def spawn_boss():

    return {

        "x": WORLD_WIDTH // 2,
        "y": WORLD_HEIGHT // 2,

        "size": 220,

        "hp": 6000 + wave * 2000,

        "max_hp": 6000 + wave * 2000
    }

def spawn_wave():

    enemies.clear()

    amount = 10 + wave * 4

    for _ in range(amount):

        enemies.append(spawn_enemy())

# ============================================================
# START
# ============================================================

spawn_wave()

# ============================================================
# LOOP
# ============================================================

running = True

while running:

    dt = clock.tick(60)

    current_time = pygame.time.get_ticks()

    # ========================================================
    # SHAKE
    # ========================================================

    if shake > 0:
        shake -= 1

    shake_x = random.randint(-shake, shake)
    shake_y = random.randint(-shake, shake)

    # ========================================================
    # CAMERA
    # ========================================================

    cam_x, cam_y = camera()

    # ========================================================
    # EVENTS
    # ========================================================

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_TAB:

                between_waves = not between_waves

            # weapon switching
            keys_list = list(owned_weapons)

            for i in range(min(len(keys_list), 9)):

                if event.key == getattr(pygame, f"K_{i+1}"):

                    player["weapon"] = keys_list[i]

    # ========================================================
    # SHOP
    # ========================================================

    if between_waves:

        screen.fill((20,20,30))

        title = big_font.render("SHOP", True, WHITE)

        screen.blit(title, (WIDTH//2 - 100, 50))

        shop_text = [

            "1 - +20 Max Health (50 coins)",
            "2 - +10 Shield (50 coins)",
            "3 - +10% Damage (100 coins)",
            "4 - +10% Fire Rate (120 coins)",
            "5 - +1 Sprint Speed (150 coins)",
            "",
            "TAB - Continue"
        ]

        for i, t in enumerate(shop_text):

            txt = font.render(t, True, WHITE)

            screen.blit(txt, (120, 180 + i * 45))

        coins_text = font.render(
            f"Coins: {player['coins']}",
            True,
            YELLOW
        )

        screen.blit(coins_text, (120, 500))

        keys = pygame.key.get_pressed()

        if keys[pygame.K_1] and player["coins"] >= 50:

            player["coins"] -= 50
            player["max_health"] += 20

            pygame.time.delay(150)

        if keys[pygame.K_2] and player["coins"] >= 50:

            player["coins"] -= 50
            player["max_shield"] += 10

            pygame.time.delay(150)

        if keys[pygame.K_3] and player["coins"] >= 100:

            player["coins"] -= 100
            player["damage_bonus"] *= 1.1

            pygame.time.delay(150)

        if keys[pygame.K_4] and player["coins"] >= 120:

            player["coins"] -= 120
            player["fire_rate_bonus"] *= 0.9

            pygame.time.delay(150)

        if keys[pygame.K_5] and player["coins"] >= 150:

            player["coins"] -= 150
            player["sprint"] += 1

            pygame.time.delay(150)

        pygame.display.flip()

        continue

    # ========================================================
    # BACKGROUND
    # ========================================================

    screen.fill((215,215,215))

    # grid
    for x in range(0, WORLD_WIDTH, 100):

        pygame.draw.line(

            screen,
            (195,195,195),

            (x - cam_x + shake_x, -cam_y + shake_y),
            (x - cam_x + shake_x, WORLD_HEIGHT - cam_y + shake_y)
        )

    for y in range(0, WORLD_HEIGHT, 100):

        pygame.draw.line(

            screen,
            (195,195,195),

            (-cam_x + shake_x, y - cam_y + shake_y),
            (WORLD_WIDTH - cam_x + shake_x, y - cam_y + shake_y)
        )

    # ========================================================
    # MOVEMENT
    # ========================================================

    keys = pygame.key.get_pressed()

    speed = player["speed"]

    if keys[pygame.K_LSHIFT]:
        speed = player["sprint"]

    move_x = 0
    move_y = 0

    if keys[pygame.K_w]:
        move_y -= 1

    if keys[pygame.K_s]:
        move_y += 1

    if keys[pygame.K_a]:
        move_x -= 1

    if keys[pygame.K_d]:
        move_x += 1

    length = math.hypot(move_x, move_y)

    if length > 0:

        move_x /= length
        move_y /= length

        move_x *= speed
        move_y *= speed

    nx = player["x"] + move_x
    ny = player["y"] + move_y

    rect_x = pygame.Rect(
        nx,
        player["y"],
        player["size"],
        player["size"]
    )

    if not collide(rect_x):
        player["x"] = nx

    rect_y = pygame.Rect(
        player["x"],
        ny,
        player["size"],
        player["size"]
    )

    if not collide(rect_y):
        player["y"] = ny

    # ========================================================
    # AIM
    # ========================================================

    mouse_x, mouse_y = pygame.mouse.get_pos()

    world_mouse_x = mouse_x + cam_x
    world_mouse_y = mouse_y + cam_y

    angle = math.atan2(
        world_mouse_y - player["y"],
        world_mouse_x - player["x"]
    )

    mouse_buttons = pygame.mouse.get_pressed()

    weapon = weapons[player["weapon"]]

    # ========================================================
    # SHOOT
    # ========================================================

    if mouse_buttons[0]:

        rate = weapon["rate"] * player["fire_rate_bonus"]

        if current_time - last_shot > rate:

            for _ in range(weapon["pellets"]):

                spread = random.uniform(
                    -weapon["spread"],
                    weapon["spread"]
                )

                shoot_angle = angle + spread

                if player["weapon"] == "rocket":

                    rockets.append({

                        "x": player["x"],
                        "y": player["y"],

                        "dx": math.cos(shoot_angle) * weapon["speed"],
                        "dy": math.sin(shoot_angle) * weapon["speed"]
                    })

                else:

                    bullets.append({

                        "x": player["x"],
                        "y": player["y"],

                        "dx": math.cos(shoot_angle) * weapon["speed"],
                        "dy": math.sin(shoot_angle) * weapon["speed"],

                        "damage": weapon["damage"] * player["damage_bonus"],

                        "color": weapon["color"]
                    })

            make_particles(
                player["x"],
                player["y"],
                weapon["color"],
                8
            )

            last_shot = current_time

    # ========================================================
    # GRENADE
    # ========================================================

    if mouse_buttons[2]:

        if current_time - last_grenade > 1200:

            grenades.append({

                "x": player["x"],
                "y": player["y"],

                "dx": math.cos(angle) * 7,
                "dy": math.sin(angle) * 7,

                "timer": current_time + 1400
            })

            last_grenade = current_time

    # ========================================================
    # BULLETS
    # ========================================================

    for b in bullets[:]:

        b["x"] += b["dx"]
        b["y"] += b["dy"]

        rect = pygame.Rect(
            b["x"],
            b["y"],
            6,
            6
        )

        if collide(rect):

            bullets.remove(b)
            continue

        for e in enemies[:]:

            er = pygame.Rect(
                e["x"],
                e["y"],
                e["size"],
                e["size"]
            )

            if rect.colliderect(er):

                e["hp"] -= b["damage"]

                make_particles(
                    e["x"],
                    e["y"],
                    RED,
                    12
                )

                if e["hp"] <= 0:

                    enemies.remove(e)

                    player["coins"] += 5
                    player["xp"] += 10

                    score += 20

                bullets.remove(b)
                break

    # ========================================================
    # ROCKETS
    # ========================================================

    for r in rockets[:]:

        r["x"] += r["dx"]
        r["y"] += r["dy"]

        rr = pygame.Rect(r["x"], r["y"], 12, 12)

        exploded = False

        if collide(rr):
            exploded = True

        for e in enemies:

            er = pygame.Rect(
                e["x"],
                e["y"],
                e["size"],
                e["size"]
            )

            if rr.colliderect(er):
                exploded = True

        if exploded:

            explode(r["x"], r["y"], 220)

            rockets.remove(r)

    # ========================================================
    # GRENADES
    # ========================================================

    for g in grenades[:]:

        g["x"] += g["dx"]
        g["y"] += g["dy"]

        g["dx"] *= 0.96
        g["dy"] *= 0.96

        if current_time > g["timer"]:

            explode(g["x"], g["y"], 170)

            grenades.remove(g)

    # ========================================================
    # ENEMIES
    # ========================================================

    for i, e in enumerate(enemies):

        move_x = 0
        move_y = 0

        dx = player["x"] - e["x"]
        dy = player["y"] - e["y"]

        dist = math.hypot(dx, dy)

        if dist != 0:

            move_x += (dx / dist) * e["speed"]
            move_y += (dy / dist) * e["speed"]

        # separation
        for j, o in enumerate(enemies):

            if i == j:
                continue

            dx2 = e["x"] - o["x"]
            dy2 = e["y"] - o["y"]

            d = math.hypot(dx2, dy2)

            if 0 < d < 90:

                push = (90 - d) / 90

                move_x += (dx2 / d) * push * 3
                move_y += (dy2 / d) * push * 3

        nx = e["x"] + move_x
        ny = e["y"] + move_y

        rect_x = pygame.Rect(
            nx,
            e["y"],
            e["size"],
            e["size"]
        )

        if not collide(rect_x):
            e["x"] = nx

        rect_y = pygame.Rect(
            e["x"],
            ny,
            e["size"],
            e["size"]
        )

        if not collide(rect_y):
            e["y"] = ny

        player_rect = pygame.Rect(
            player["x"],
            player["y"],
            player["size"],
            player["size"]
        )

        er = pygame.Rect(
            e["x"],
            e["y"],
            e["size"],
            e["size"]
        )

        if player_rect.colliderect(er):

            player["health"] -= 0.05

    # ========================================================
    # BOSS
    # ========================================================

    if wave % 10 == 0 and boss is None:

        boss = spawn_boss()

    if boss:

        dx = player["x"] - boss["x"]
        dy = player["y"] - boss["y"]

        dist = math.hypot(dx, dy)

        if dist != 0:

            boss["x"] += (dx / dist) * 1.2
            boss["y"] += (dy / dist) * 1.2

        br = pygame.Rect(
            boss["x"],
            boss["y"],
            boss["size"],
            boss["size"]
        )

        player_rect = pygame.Rect(
            player["x"],
            player["y"],
            player["size"],
            player["size"]
        )

        if player_rect.colliderect(br):

            player["health"] -= 0.2

    # ========================================================
    # LEVEL
    # ========================================================

    needed = player["level"] * 100

    if player["xp"] >= needed:

        player["xp"] = 0
        player["level"] += 1

        player["max_health"] += 10
        player["health"] = player["max_health"]

    # ========================================================
    # NEXT WAVE
    # ========================================================

    if len(enemies) == 0:

        wave += 1

        between_waves = True

        if wave in weapon_unlocks:

            w = weapon_unlocks[wave]

            if w not in owned_weapons:
                owned_weapons.append(w)

        spawn_wave()

    # ========================================================
    # PARTICLES
    # ========================================================

    for p in particles[:]:

        p["x"] += p["dx"]
        p["y"] += p["dy"]

        p["life"] -= 1

        if p["life"] <= 0:
            particles.remove(p)

    # ========================================================
    # EXPLOSIONS
    # ========================================================

    for ex in explosions[:]:

        ex["life"] -= 1

        if ex["life"] <= 0:
            explosions.remove(ex)

    # ========================================================
    # WALLS
    # ========================================================

    for w in walls:

        pygame.draw.rect(

            screen,
            BLACK,

            (
                w.x - cam_x + shake_x,
                w.y - cam_y + shake_y,
                w.width,
                w.height
            )
        )

    # ========================================================
    # PLAYER
    # ========================================================

    px = player["x"] - cam_x + shake_x
    py = player["y"] - cam_y + shake_y

    # glow
    pygame.draw.circle(
        screen,
        (100,150,255),
        (int(px), int(py)),
        36
    )

    pygame.draw.circle(
        screen,
        BLUE,
        (int(px), int(py)),
        player["size"] // 2
    )

    gun_x = px + math.cos(angle) * 35
    gun_y = py + math.sin(angle) * 35

    pygame.draw.line(
        screen,
        BLACK,
        (px, py),
        (gun_x, gun_y),
        8
    )

    # ========================================================
    # ENEMIES
    # ========================================================

    for e in enemies:

        ex = e["x"] - cam_x + shake_x
        ey = e["y"] - cam_y + shake_y

        pygame.draw.circle(
            screen,
            (40,40,40),
            (int(ex+5), int(ey+5)),
            e["size"] // 2
        )

        pygame.draw.circle(
            screen,
            e["color"],
            (int(ex), int(ey)),
            e["size"] // 2
        )

    # ========================================================
    # BOSS
    # ========================================================

    if boss:

        bx = boss["x"] - cam_x + shake_x
        by = boss["y"] - cam_y + shake_y

        pygame.draw.circle(
            screen,
            PURPLE,
            (int(bx), int(by)),
            boss["size"] // 2
        )

        # hp bar
        pygame.draw.rect(
            screen,
            BLACK,
            (350,20,600,30)
        )

        pygame.draw.rect(
            screen,
            PURPLE,
            (
                350,
                20,
                (boss["hp"] / boss["max_hp"]) * 600,
                30
            )
        )

    # ========================================================
    # BULLETS
    # ========================================================

    for b in bullets:

        bx = b["x"] - cam_x + shake_x
        by = b["y"] - cam_y + shake_y

        pygame.draw.circle(
            screen,
            b["color"],
            (int(bx), int(by)),
            7
        )

        pygame.draw.circle(
            screen,
            WHITE,
            (int(bx), int(by)),
            3
        )

    # ========================================================
    # ROCKETS
    # ========================================================

    for r in rockets:

        pygame.draw.circle(
            screen,
            RED,
            (
                int(r["x"] - cam_x + shake_x),
                int(r["y"] - cam_y + shake_y)
            ),
            10
        )

    # ========================================================
    # GRENADES
    # ========================================================

    for g in grenades:

        pygame.draw.circle(
            screen,
            GRAY,
            (
                int(g["x"] - cam_x + shake_x),
                int(g["y"] - cam_y + shake_y)
            ),
            7
        )

    # ========================================================
    # EXPLOSIONS
    # ========================================================

    for ex in explosions:

        pygame.draw.circle(
            screen,
            ORANGE,
            (
                int(ex["x"] - cam_x + shake_x),
                int(ex["y"] - cam_y + shake_y)
            ),
            ex["radius"],
            5
        )

    # ========================================================
    # PARTICLES
    # ========================================================

    for p in particles:

        pygame.draw.circle(
            screen,
            p["color"],
            (
                int(p["x"] - cam_x + shake_x),
                int(p["y"] - cam_y + shake_y)
            ),
            p["size"]
        )

    # ========================================================
    # MINIMAP
    # ========================================================

    minimap_x = WIDTH - 220
    minimap_y = 20

    pygame.draw.rect(
        screen,
        BLACK,
        (minimap_x, minimap_y, 200, 200)
    )

    # player dot
    px_map = minimap_x + (player["x"] / WORLD_WIDTH) * 200
    py_map = minimap_y + (player["y"] / WORLD_HEIGHT) * 200

    pygame.draw.circle(
        screen,
        BLUE,
        (int(px_map), int(py_map)),
        4
    )

    # enemy dots
    for e in enemies:

        ex_map = minimap_x + (e["x"] / WORLD_WIDTH) * 200
        ey_map = minimap_y + (e["y"] / WORLD_HEIGHT) * 200

        pygame.draw.circle(
            screen,
            RED,
            (int(ex_map), int(ey_map)),
            2
        )

    # ========================================================
    # CROSSHAIR
    # ========================================================

    pygame.draw.circle(
        screen,
        WHITE,
        (mouse_x, mouse_y),
        14,
        2
    )

    pygame.draw.line(
        screen,
        WHITE,
        (mouse_x - 20, mouse_y),
        (mouse_x + 20, mouse_y),
        2
    )

    pygame.draw.line(
        screen,
        WHITE,
        (mouse_x, mouse_y - 20),
        (mouse_x, mouse_y + 20),
        2
    )

    # ========================================================
    # UI
    # ========================================================

    # health
    pygame.draw.rect(
        screen,
        BLACK,
        (20,20,320,25)
    )

    pygame.draw.rect(
        screen,
        RED,
        (
            20,
            20,
            (player["health"] / player["max_health"]) * 320,
            25
        )
    )

    ui = font.render(

        f"Wave: {wave}   "
        f"Weapon: {player['weapon'].upper()}   "
        f"Coins: {player['coins']}   "
        f"Level: {player['level']}   "
        f"XP: {player['xp']}   "
        f"Score: {score}",

        True,
        WHITE
    )

    screen.blit(ui, (20, HEIGHT - 35))

    controls = font.render(

        "WASD Move | Shift Sprint | Left Click Shoot | Right Click Grenade | TAB Shop",

        True,
        WHITE
    )

    screen.blit(controls, (20, HEIGHT - 65))

    # ========================================================
    # GAME OVER
    # ========================================================

    if player["health"] <= 0:

        screen.fill(BLACK)

        text = big_font.render(
            "GAME OVER",
            True,
            RED
        )

        screen.blit(
            text,
            (
                WIDTH // 2 - 220,
                HEIGHT // 2 - 40
            )
        )

        pygame.display.flip()

        pygame.time.delay(5000)

        running = False

    pygame.display.flip()

pygame.quit()
sys.exit()