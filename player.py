import pygame
import math
from entity import Entity
from config import arena_center_x, arena_center_y, arena_radius, circle_radius

class Player(Entity):
    def __init__(self, x=300, y=300, speed=2, color=(139, 0, 0)):
        super().__init__(x, y, speed, color)
        self.hunger = 700
        self.max_hunger = 700

    def handle_movement(self, keys):
        """
        Handle player movement with keyboard input.
        """
        if keys[pygame.K_UP]:
            self.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.y += self.speed
        if keys[pygame.K_LEFT]:
            self.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.x += self.speed
        
        self._constrain_to_arena(arena_center_x, arena_center_y, arena_radius, circle_radius)
        self.hunger -= 1

    def player_prey_collision(self, preys):
        """
        Handle collisions with prey.
        """
        for prey in preys[:]:
            dx = prey.x - self.x
            dy = prey.y - self.y
            distance = math.sqrt(dx**2 + dy**2)

            if distance < 40:  # Player collects prey
                preys.remove(prey)
                self.hunger = min(self.hunger + 300, self.max_hunger)
