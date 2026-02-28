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
            return Position(-1,0)
        
        if self.degrees % 360 == 180:
            return Position(0,1)
        
        if self.degrees % 360 == 270:
            return Position(1,0)
    
    def __add__(self, amount):
        if amount % 90 != 0:
            print("Error: '", amount, "' ist keine erlaube Drehung und kann nicht mit '+' verwendet werden. Kara kann sich nur um 90-Grad Intervalle drehen." )
            return self
        self.degrees = (self.degrees + amount) % 360
        return self

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
    
    def rotate(self, by_degrees):
        if by_degrees % 90 != 0:
            print("Error: '", by_degrees, "' ist keine erlaubte Drehung. Kara kann sich nur um 90-Grad Intervalle drehen." )
            return self
        self.rotation += by_degrees
    
    

class World:

    #content = {}
    size = None
    kara = Kara(Position, Rotation)

    def __init__(self, world_size = size, kara_pos = Position, kara_rot = Rotation):
        self.kara = Kara(kara_pos, kara_rot)
        self.size = world_size    

    def draw(self):

        self.karaImage = None

        if self.karaImage == None:
            self.karaImage = pygame.image.load("kara.png").convert_alpha()

        self.draw_grid(screen)
        self.draw_kara(screen)

        pygame.display.flip()

    def draw_grid(self, surface):

        surface.fill((120, 140, 110))

        for y in range(1,self.size[1]):
            line_poses = [[0,y*64],[self.size[0]*64,y*64]]
            pygame.draw.line(surface,pygame.Color(0, 0, 0),pygame.Vector2(line_poses[0][0],line_poses[0][1]),pygame.Vector2(line_poses[1][0],line_poses[1][1]),2)
        
        for x in range(1,self.size[0]):
            line_poses = [[x*64,0],[x*64,self.size[1]*64]]
            pygame.draw.line(surface,pygame.Color(0, 0, 0),pygame.Vector2(line_poses[0][0],line_poses[0][1]),pygame.Vector2(line_poses[1][0],line_poses[1][1]),2)

    def draw_kara(self, surface):
        kara_real_pos = (self.kara.position.x * 64,self.kara.position.y * 64)
        new_image = World.rot_center(self.karaImage,self.kara.rotation.degrees,32,32)[0]
        
        surface.blit(new_image,kara_real_pos)

    def rot_center(image, angle, x, y):
        
        rotated_image = pygame.transform.rotate(image, angle)
        new_rect = rotated_image.get_rect(center = image.get_rect(center = (x, y)).center)

        return rotated_image, new_rect


# MAIN PART

pygame.init()

tile_size = 64
world_size = [10, 10]

screen_width = world_size[0] * tile_size
screen_height = world_size[1] * tile_size

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Better Kara")

world = World([10,10], Position(3, 2), Rotation(0))

clock = pygame.time.Clock()
fps = 60

while True:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    world.draw()

    pygame.display.flip()

    clock.tick(fps)