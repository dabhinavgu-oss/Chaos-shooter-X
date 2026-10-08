# CHAOS SHOOTER X

A fast-paced top-down survival shooter built with **Python + Pygame**.

Fight through increasingly difficult waves, unlock powerful weapons, defeat different enemy types, collect coins and XP, and survive as long as you can.

## 🎮 Features

- 🔫 **10 weapons** to unlock and use
- 👾 Multiple enemy types:
  - Normal
  - Fast
  - Tank
  - Elite
- 👹 **Boss battles** on every 10th wave
- 🌊 Increasingly difficult **wave-based gameplay**
- ⭐ XP and **level-up system**
- 🪙 Coins and an **upgrade shop**
- 💥 Rockets, grenades, explosions, and particle effects
- 📳 Screen shake and visual effects
- 🗺️ Large **7000 × 7000** game world
- 🧱 Randomly generated walls and obstacles
- 🧭 Minimap showing the player and enemies
- 🎯 Mouse aiming and shooting
- 🏃 Sprint movement
- ❤️ Health and shield progression
- 💀 Game-over system

## 🔫 Weapons

Weapons unlock as you level up through the waves:

| Unlock Wave | Weapon |
|---:|---|
| Start | Pistol |
| 3 | SMG |
| 6 | Burst |
| 9 | Shotgun |
| 12 | Sniper |
| 15 | Minigun |
| 18 | Plasma |
| 21 | Laser |
| 24 | Rocket |
| 27 | Chaos |

The **Chaos** weapon is the final unlock and fires a powerful spread of projectiles.

## 🕹️ Controls

| Control | Action |
|---|---|
| **W A S D** | Move |
| **Left Shift** | Sprint |
| **Left Mouse Button** | Shoot |
| **Right Mouse Button** | Throw grenade |
| **1–9** | Switch weapons |
| **TAB** | Open/close shop |

## 🛒 Shop

Use the shop between waves to spend coins on upgrades:

- **+20 Max Health** — 50 coins
- **+10 Shield** — 50 coins
- **+10% Damage** — 100 coins
- **+10% Fire Rate** — 120 coins
- **+1 Sprint Speed** — 150 coins

## 📈 Progression

Defeating enemies gives you:

- **XP** — used to level up
- **Coins** — used for upgrades
- **Score** — tracks your performance

As your level increases, your maximum health also increases.

## 💥 Combat

CHAOS SHOOTER X is designed around fast movement and constant combat. Different weapons have different damage, fire rates, projectile speeds, spreads, and projectile counts.

Explosions can damage multiple enemies at once, making rockets and grenades especially useful when you're surrounded.

## 🗺️ The World

The game takes place in a large **7000 × 7000** world with randomly generated obstacles.

The camera follows the player while the minimap gives you an overview of the battlefield.

Enemies also use separation behavior so they don't simply stack on top of each other.

## 🐍 Requirements

- Python 3
- Pygame

Install Pygame with:

```bash
python -m pip install pygame
```

If your system uses `python3`, use:

```bash
python3 -m pip install pygame
```

## ▶️ Run the Game

Clone the repository:

```bash
git clone https://github.com/dabhinavgu-oss/Chaos-shooter-X.git
cd Chaos-shooter-X
```

Then run:

```bash
python "My real real game.py"
```

On systems where Python is called `python3`:

```bash
python3 "My real real game.py"
```

## 🧪 Project Status

**Playable prototype / active development**

CHAOS SHOOTER X is an ongoing game project. New weapons, enemies, effects, mechanics, balancing changes, and other features may be added over time.

## 📁 Project Structure

```text
Chaos-shooter-X/
└── My real real game.py
```

## 🚀 Future Ideas

Possible future additions include:

- More bosses
- More enemy abilities
- More weapons
- Weapon ammo and reload systems
- More maps
- Better enemy AI
- More shop upgrades
- Sound effects and music
- Save/load progression
- Menus and settings
- Multiplayer
- Online/web version

## 📜 License

No license has currently been specified for this project.

---

**CHAOS SHOOTER X**  
*Survive the chaos. Keep shooting.*
