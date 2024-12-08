from entity import Entity
from random import uniform
import math
from config import arena_center_x, arena_center_y, arena_radius, circle_radius

class Predator(Entity):
    def __init__(self, x=300, y=300, speed=2, color=(255, 69, 0)):
        super().__init__(x, y, speed, color)
        self.hunger = 700
        self.max_hunger = 700
        self.last_target = None
        self.avoid_target_timer = 0  # Timer to avoid the last target

    def move(self):
        """
        Update position, manage hunger, and randomize movement.
        """
        self.x += self.speed_x
        self.y += self.speed_y
        self._constrain_to_arena(arena_center_x, arena_center_y, arena_radius, circle_radius)
        self.hunger -= 1
        self._add_randomness()

        # Decrease avoid timer
        if self.avoid_target_timer > 0:
            self.avoid_target_timer -= 1

    def predator_prey_collision(self, preys):
        """
        Handle collisions with prey.
        """
        closest_prey = None
        closest_distance = float("inf")

        for prey in preys[:]:
            dx = prey.x - self.x
            dy = prey.y - self.y
            distance = math.sqrt(dx**2 + dy**2)

            if distance < 40:  # Consume prey
                preys.remove(prey)
                self.hunger = min(self.hunger + 300, self.max_hunger)
                self.last_target = None
                self.avoid_target_timer = 60  # Avoid targeting same prey for 1 second
                self._reset_direction()
                return

            # Skip last target during cooldown
            if prey != self.last_target or self.avoid_target_timer == 0:
                if distance < 100 and distance < closest_distance:
                    closest_prey = prey
                    closest_distance = distance

        if closest_prey:
            self._chase_prey(closest_prey)

    def _chase_prey(self, prey):
        """
        Adjust direction to chase prey.
        """
        self.color = (139, 0, 0)  # Chasing color
        dx = prey.x - self.x
        dy = prey.y - self.y
        distance = math.sqrt(dx**2 + dy**2)

        if distance > 0:
            normalized_dx = dx / distance
            normalized_dy = dy / distance
            self.speed_x = (normalized_dx * self.speed) + uniform(-0.1, 0.1)
            self.speed_y = (normalized_dy * self.speed) + uniform(-0.1, 0.1)

        self.last_target = prey  # Remember the target

        # Occasionally reset direction for unpredictability
        if uniform(0, 1) < 0.01:
            self._reset_direction()

    def _reset_direction(self):
        """
        Reset the predator's direction and appearance.
        """
        dx = uniform(-1, 1)
        dy = uniform(-1, 1)
        magnitude = math.sqrt(dx**2 + dy**2)

        if magnitude > 0:
            self.speed_x = (dx / magnitude) * self.speed
            self.speed_y = (dy / magnitude) * self.speed
        else:
            self.speed_x = self.speed
            self.speed_y = 0

        self.color = (255, 69, 0)  # Idle color

    def _add_randomness(self):
        """
        Introduce slight randomness to movement.
        """
        if uniform(0, 1) < 0.01:  # 1% chance each frame
            self.speed_x += uniform(-0.2, 0.2)
            self.speed_y += uniform(-0.2, 0.2)
