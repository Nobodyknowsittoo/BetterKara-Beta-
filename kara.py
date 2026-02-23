import math
import pygame
import sys

class Position:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __mul__(self, other):
        return Position(self.x * other, self.y * other)
    
    def __add__(self, other):
        return Position(self.x + other.x, self.y + other.y)
    
    def is_in_bound(self,min_x,max_x,min_y,max_y):  # Returns True if the character is in the given bound
        if self.x >= min_x:
            if self.x <= max_x:
                if self.y >= min_y:
                    if self.y <= max_y:
                        return True
        return False
    
    def is_in_worldborder(self, world): # Uses the is_in_bound function to check if the character is in the worldboarder
        return self.is_in_bound(0, world.size[0]-1, 0, world.size[1]-1)
    

class Rotation:
    
    degrees = 0

    def __init__(self, rotation):
        self.degrees = math.floor(rotation / 90) * 90
    
    def get_normal(self):
        
        if self.degrees % 360 == 0:
            return Position(0,-1)
        
        if self.degrees % 360 == 90:
            return Position(1,0)
        
        if self.degrees % 360 == 180:
            return Position(0,1)
        
        if self.degrees % 360 == 270:
            return Position(1,0)
        

class Kara:
    
    position = Position
    rotation = Rotation
    
    def __init__(self, position = Position, rotation = Rotation):
        self.position = position
        self.rotation = rotation
    
    def move(self,steps, world):
        
        new_pos = self.position + (self.rotation.get_normal() * steps)
        
        if not new_pos.is_in_worldborder(world):
            print("Kara ist gegen eine Wand gelaufen. (˘︹˘)")
            return
        
        self.position = new_pos

# MAIN PART

pygame.init()

screen_width, screen_height = 400, 300
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Better Kara")

WHITE = (155, 155, 155)
BLACK = (0, 0, 0)

clock = pygame.time.Clock()

while True:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill(WHITE)

    pygame.display.flip()

    clock.tick(40)