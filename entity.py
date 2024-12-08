import math
from random import uniform

class Entity:
    def __init__(self, x=300, y=300, speed=2, color=(255, 255, 255)):
        self.x = x
        self.y = y
        self.color = color
        self.speed = speed
        self.speed_x = uniform(-speed, speed)
        self.speed_y = uniform(-speed, speed)

    def _constrain_to_arena(self, arena_center_x, arena_center_y, arena_radius, circle_radius):
        """
        Keep the prey inside the circular arena and adjust speed to avoid walls.
        """
        dx = self.x - arena_center_x
        dy = self.y - arena_center_y
        distance_from_center = math.sqrt(dx**2 + dy**2)

        # Check if near or outside the boundary
        if distance_from_center >= arena_radius - circle_radius:
            normalized_dx = dx / distance_from_center
            normalized_dy = dy / distance_from_center

            # Push back inside the arena
            self.x = arena_center_x + normalized_dx * (arena_radius - circle_radius - 1)
            self.y = arena_center_y + normalized_dy * (arena_radius - circle_radius - 1)

            # Adjust speed to avoid walls
            self.speed_x += -normalized_dx * 0.2
            self.speed_y += -normalized_dy * 0.2

            # Normalize speed to prevent excessive acceleration
            magnitude = math.sqrt(self.speed_x**2 + self.speed_y**2)
            if magnitude > self.speed:
                self.speed_x = (self.speed_x / magnitude) * self.speed
                self.speed_y = (self.speed_y / magnitude) * self.speed

