from predator import Predator
from prey import Prey
from player import Player
from config import (
    screen_width,
    screen_height,
    arena_center_x,
    arena_center_y,
    arena_radius,
    circle_radius,
    spawn_prey,
    spawn_predator,
)
import pygame
import sys

def update_preys(preys, predators, player):
    """
    Update prey behavior: evade predators, move, and reproduce.
    """
    for prey in preys:
        prey.evade_predator(predators, player)
        prey.move(preys)
        prey.reproduce(preys)

def update_predators(predators, preys):
    """
    Update predator behavior: move, hunt prey, and handle starvation.
    """
    for predator in predators[:]:  # Iterate over a copy to allow removal
        predator.move()
        Predator.predator_prey_collision(predator, preys)
        if predator.hunger <= 0:
            predators.remove(predator)

def update_player(player, preys):
    """
    Update player behavior: handle movement and collisions with prey.
    """
    keys = pygame.key.get_pressed()
    player.handle_movement(keys)
    player.player_prey_collision(preys)
    if player.hunger <= 0:
        print("Player has died of hunger. Game Over!")
        pygame.quit()
        sys.exit()

def render_entities(screen, preys, predators, player):
    """
    Render prey, predators, and their hunger bars.
    """
    for prey in preys:
        pygame.draw.circle(screen, prey.color, (int(prey.x), int(prey.y)), circle_radius)
        
    for predator in predators:
        # Draw predator outline (white)
        outline_radius = circle_radius + 3  # Thickness adjustment
        pygame.draw.circle(screen, (255, 255, 255), (int(predator.x), int(predator.y)), outline_radius)
        # Draw the predator itself
        pygame.draw.circle(screen, predator.color, (int(predator.x), int(predator.y)), circle_radius)
        draw_hunger_bar(screen, predator)
    
    # Draw player with yellow outline
    outline_radius = circle_radius + 3
    pygame.draw.circle(screen, (255, 240, 0), (int(player.x), int(player.y)), outline_radius)
    pygame.draw.circle(screen, player.color, (int(player.x), int(player.y)), circle_radius)
    draw_hunger_bar(screen, player)
        
def draw_hunger_bar(screen, predator):
    """
    Draw the predator's hunger bar above its position.
    """
    bar_width = circle_radius * 2
    bar_height = 5
    x = int(predator.x) - bar_width // 2
    y = int(predator.y) - circle_radius - 10

    hunger_percent = min(predator.hunger / 700, 1.0)  # Cap at 100%
    pygame.draw.rect(screen, (128, 128, 128), (x, y, bar_width, bar_height))  # Background
    pygame.draw.rect(screen, (0, 255, 0), (x, y, int(bar_width * hunger_percent), bar_height))  # Foreground

def draw_arena(screen):
    """
    Draw the circular arena boundary.
    """
    pygame.draw.circle(screen, (255, 255, 255), (arena_center_x, arena_center_y), arena_radius, 2)
