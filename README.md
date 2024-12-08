**﻿Predator-Prey-game**

My first pygame project. This simple game showcases dynamic interactions in a simulated ecosystem where predators (incl. player), prey coexist. Predators hunt prey in hope of not dying from hunger. Prey evades threats in a circular arena and reproduces trying to stay alive.

![image](https://github.com/user-attachments/assets/9b4fc9d6-1c64-4f27-8e17-72992327f271)

## Features

- **Prey Behavior**: Prey reproduce, evade predators and players, and avoid walls.
- **Predator Behavior**: Predators chase and consume prey while managing their hunger levels.
- **Player Control**: Take control of a predator
- **Hunger Mechanic**: Predators starve if they don't consume prey within a certain time frame.
- **Reproduction**: Prey reproduce when conditions are met, inheriting traits like speed.

## Gameplay

- **Controls**:
  - Arrow keys: Move the player.
  - Your goal: Hunt down all prey before you die of hunger.

- **Simulation**:
  - Prey evade predators and the player.
  - Predators hunt prey while avoiding starvation.
  - Prey and predators remain constrained within the circular arena.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/predator-prey-simulation.git
   cd predator-prey-simulation
   python main.py
