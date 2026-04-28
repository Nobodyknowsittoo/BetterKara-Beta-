import math
import pygame
import sys
import threading
import asyncio

class Position:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __mul__(self, other):
        return Position(self.x * other, self.y * other)
    
    def __add__(self, other):
        return Position(self.x + other.x, self.y + other.y)
    
    def __str__(self):
        return "(" + str(self.x) + ";" + str(self.y) + ")" 

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

class Thing:
    position = Position

    def __init__(self, position = Position):
        self.position = Position

class Leaf(Thing):
    leaf_type = "sakura" #basil, apple, plum, grape

    def __init__(self, leaf_type = "sakura"):
        self.leaf_type = leaf_type


class Kara:
    
    position = Position
    rotation = Rotation
    world = None
    
    def __init__(self, position = Position, rotation = Rotation, world = None):
        self.position = position
        self.rotation = rotation
        self.world = world
    
    def move(self,steps):
        
        new_pos = self.position + (self.rotation.get_normal() * steps)
        
        if self.world:
            if not new_pos.is_in_worldborder(self.world):
                print("Kara ist gegen eine Wand gelaufen. (˘︹˘)")
                return
        
        self.position = new_pos
    
    def put_leaf(self,type):
        if not self.world.is_space_free(self.position):
            print("Error: Kara kann an " + str(self.position) + " kein ",type,"-Blatt platzieren!")
            return self
        
        leaf = Leaf(type)
        leaf.position = self.position

        self.world.content.append(leaf)
        
    
    def rotate(self, by_degrees):
        if by_degrees % 90 != 0:
            print("Error: '", by_degrees, "' ist keine erlaubte Drehung. Kara kann sich nur um 90-Grad Intervalle drehen." )
            return self
        self.rotation += by_degrees
    
class World:
    global screen
    content = []
    size = None
    kara = Kara(Position, Rotation, None)

    def __init__(self, world_size = size, kara_pos = Position, kara_rot = Rotation):
        self.kara = Kara(kara_pos, kara_rot,self)
        self.size = world_size

    def is_space_free(self, position):
        for thing in self.content:
            if thing.position == position:
                return False
        return True

    def prepare(self):
        global screen

        screen_width = self.size[0] * appearance.tile_size
        screen_height = self.size[1] * appearance.tile_size

        screen = pygame.display.set_mode((screen_width, screen_height))

        self.karaImage = pygame.image.load("assets/kara.png").convert_alpha()
        self.karaImage = pygame.transform.scale(self.karaImage, [appearance.tile_size, appearance.tile_size])

        pygame.display.set_caption("Better Kara")

    def draw(self):

        self.draw_grid(screen)
        self.draw_leafs(screen)
        self.draw_kara(screen)

        pygame.display.flip()

    def draw_leafs(self, surface):
        for thing in self.content:
            if isinstance(thing, Leaf):
                if not thing.leaf_type in appearance.leaf_cache.keys():
                    leafImage = pygame.image.load("assets/leafs/" + thing.leaf_type + ".png").convert_alpha()
                    leafImage = pygame.transform.scale(leafImage, [appearance.tile_size, appearance.tile_size])
                    appearance.leaf_cache[thing.leaf_type] = leafImage
                leafImage = appearance.leaf_cache[thing.leaf_type]
                leafPos = (thing.position.x * appearance.tile_size,thing.position.y * appearance.tile_size)
                surface.blit(leafImage,leafPos)


    def draw_grid(self, surface):

        surface.fill((120, 140, 110))

        for y in range(1,self.size[1]):
            line_poses = [[0,y*appearance.tile_size],[self.size[0]*appearance.tile_size,y*appearance.tile_size]]
            pygame.draw.line(surface,pygame.Color(0, 0, 0),pygame.Vector2(line_poses[0][0],line_poses[0][1]),pygame.Vector2(line_poses[1][0],line_poses[1][1]),appearance.line_width)
        
        for x in range(1,self.size[0]):
            line_poses = [[x*appearance.tile_size,0],[x*appearance.tile_size,self.size[1]*appearance.tile_size]]
            pygame.draw.line(surface,pygame.Color(0, 0, 0),pygame.Vector2(line_poses[0][0],line_poses[0][1]),pygame.Vector2(line_poses[1][0],line_poses[1][1]),appearance.line_width)

    def draw_kara(self, surface):
        kara_real_pos = (self.kara.position.x * appearance.tile_size,self.kara.position.y * appearance.tile_size)
        new_image = World.rot_center(self.karaImage,self.kara.rotation.degrees,appearance.tile_size / 2,appearance.tile_size / 2)[0]
        
        surface.blit(new_image,kara_real_pos)

    def rot_center(image, angle, x, y):
        
        rotated_image = pygame.transform.rotate(image, angle)
        new_rect = rotated_image.get_rect(center = image.get_rect(center = (x, y)).center)

        return rotated_image, new_rect

class Appearance:
    tile_size = 64
    line_width = 4

    leaf_cache = {

    }

    def __init__(self, tile_size = 64):
        self.tile_size = tile_size

# MAIN PART

pygame.init()

appearance = Appearance(64)

world_size = [10, 10]

screen = None

world = World([10,10], Position(3, 2), Rotation(0))

clock = pygame.time.Clock()
fps = 60

async def check_quit():
    while True:
        print("test")
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        world.draw()

        pygame.display.flip()

        #clock.tick(fps)