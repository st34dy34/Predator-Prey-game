from entity import Entity
from random import uniform, choice, randint
import math
from config import arena_center_x, arena_center_y, arena_radius, circle_radius, max_prey

class Prey(Entity):
    def __init__(self, x=300, y=300, speed=2):
        super().__init__(x, y, speed, color=(randint(100, 255), randint(100, 255), randint(100, 255)))
        self.reproduction_cooldown = 300
        self.hunted = False

    def move(self, preys):
        """
        Update the prey's position, avoiding clustering and walls, and keep it within bounds.
        """
        if self.hunted:
            self._avoid_other_preys(preys)  # Avoid nearby preys if hunted
        self.x += self.speed_x
        self.y += self.speed_y
        # Ensure _constrain_to_arena is called with correct arguments
        self._constrain_to_arena(
            arena_center_x=arena_center_x,
            arena_center_y=arena_center_y,
            arena_radius=arena_radius,
            circle_radius=circle_radius,
        )
        self._decrease_cooldown()  # Reduce reproduction cooldown

        
    def evade_predator(self, predators,player):
        """
        Adjust speed and state to evade nearby predators while staying in the arena.
        """
        combined_dx, combined_dy = 0, 0
        threat_nearby = False
        #Check for predator
        for predator in predators:
            dx = self.x - predator.x
            dy = self.y - predator.y
            distance = math.sqrt(dx**2 + dy**2)

            if distance < 100:  # Predator threat detected
                threat_nearby = True
                if distance > 0:  # Avoid division by zero
                    combined_dx += dx / distance
                    combined_dy += dy / distance
        # Check for player
        if player:
            dx = self.x - player.x
            dy = self.y - player.y
            distance = math.sqrt(dx**2 + dy**2)

            if distance < 100:  # Player threat detected
                threat_nearby = True
                if distance > 0:
                    combined_dx += dx / distance
                    combined_dy += dy / distance 
        # finish
        if threat_nearby:
            # Update speed to evade the combined threats
            self._update_speed(combined_dx, combined_dy)
            self.hunted = True
        else:
            # No threats nearby; default wandering behavior
            self.hunted = False
            self._add_random_speed()

        # Ensure motion even when idle
        if not threat_nearby and self.speed_x == 0 and self.speed_y == 0:
            self._add_random_speed()
            
    def _can_reproduce_with(self, other):
        """
        Check if this prey can reproduce with another prey.
        """
        distance = math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)
        return (
            distance < 40  # Reproduction range
            and self.reproduction_cooldown == 0
            and other.reproduction_cooldown == 0
        )
    
    def reproduce(self, preys):
        """
        Handle reproduction with nearby prey.
        """
        for other in preys:
            if other is not self and self._can_reproduce_with(other):
                # Randomly choose one parent's speed for the child
                child_speed = choice([self.speed, other.speed])
                if len(preys) < max_prey:  # Check population limit
                    new_prey = Prey(
                        x=(self.x + other.x) / 2,
                        y=(self.y + other.y) / 2,
                        speed=child_speed,
                    )
                    preys.append(new_prey)
                # Reset reproduction cooldowns for both parents
                self.reproduction_cooldown = 60
                other.reproduction_cooldown = 60
                
    def _update_speed(self, combined_dx, combined_dy):
        """
        Update the prey's speed based on a combined escape vector.
        """
        magnitude = math.sqrt(combined_dx**2 + combined_dy**2)
        if magnitude > 0:  # Avoid division by zero
            self.speed_x = (combined_dx / magnitude) * self.speed
            self.speed_y = (combined_dy / magnitude) * self.speed
            
    def _add_random_speed(self):
        """
        Add slight random adjustments to the prey's speed to ensure wandering behavior.
        """
        self.speed_x += uniform(-0.1, 0.1)
        self.speed_y += uniform(-0.1, 0.1)

        # Ensure the total speed remains within acceptable bounds
        magnitude = math.sqrt(self.speed_x**2 + self.speed_y**2)
        if magnitude > self.speed:  # Normalize to the maximum speed
            self.speed_x = (self.speed_x / magnitude) * self.speed
            self.speed_y = (self.speed_y / magnitude) * self.speed
            
    def _decrease_cooldown(self):
        """
        Reduce reproduction cooldown over time.
        """
        if self.reproduction_cooldown > 0:
            self.reproduction_cooldown -= 1
            
    def _avoid_other_preys(self, preys):
        """
        Adjust speed to avoid clustering with nearby preys.
        """
        combined_dx, combined_dy = 0, 0
        for other in preys:
            if other is not self:  # Avoid self-comparison
                dx = self.x - other.x
                dy = self.y - other.y
                distance = math.sqrt(dx**2 + dy**2)

                if distance < 30:  # Avoid too close neighbors
                    if distance > 0:  # Avoid division by zero
                        combined_dx += dx / distance
                        combined_dy += dy / distance

        # Apply avoidance adjustment
        magnitude = math.sqrt(combined_dx**2 + combined_dy**2)
        if magnitude > 0:
            self.speed_x += (combined_dx / magnitude) * 0.1  # Scale adjustment factor
            self.speed_y += (combined_dy / magnitude) * 0.1

