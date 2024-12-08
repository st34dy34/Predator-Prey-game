import pygame
import sys
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
from random import randint, uniform
from prey import Prey
from predator import Predator
from player import Player
from render import *
from ini import *

# //// HELPER FUNCTIONS ////

def calculate_average_speed(preys):
    """
    Calculate and return the average speed of all prey.
    """
    if not preys:  # Avoid division by zero
        return 0
    return sum(prey.speed for prey in preys) / len(preys)



def handle_events(player):
    """
    Handle game events and player movement.
    """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            print(f"Key pressed: {pygame.key.name(event.key)}")







# //// MAIN GAME LOOP ////

def main():
    screen, clock, preys, predators, player = initialize_game()

    while True:
        handle_events(player)  # Pass player to handle events
        update_preys(preys, predators,player)
        update_predators(predators, preys)
        update_player(player,preys)

        
        screen.fill((0, 0, 0))  # Clear screen
        draw_arena(screen)  # Draw arena boundary
        render_entities(screen, preys, predators,player)  # Render all entities

        # Display average prey speed
        average_speed = calculate_average_speed(preys)
        font = pygame.font.SysFont(None, 24)
        average_speed_text = font.render(f"Average Speed: {average_speed:.2f}", True, (255, 255, 255))
        screen.blit(average_speed_text, (10, 10))

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
