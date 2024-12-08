import pygame
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
from random import randint,uniform
from prey import Prey
from predator import Predator
from player import Player
# //// GAME INITIALIZATION ////

def initialize_game():
    """
    Initialize the game components, including Pygame, prey, and predators.
    """
    pygame.init()
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Predator-Prey Simulation")
    clock = pygame.time.Clock()

    preys = [
        Prey(randint(50, screen_width - 50), randint(50, screen_height - 50), uniform(1.0, 2.5))
        for _ in range(spawn_prey)
    ]
    predators = [
        Predator(randint(50, screen_width - 50), randint(50, screen_height - 50), uniform(1.0, 2.5))
        for _ in range(spawn_predator)
    ]
    
    player = Player(screen_width/2,screen_height/2,2)

    return screen, clock, preys, predators, player