import math
import pygame

class Position:
    
    x = 0
    y = 0

    def __init__(self, x = 0, y = 0):
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

class World:
    #content = {}
    size = [10,10]
    kara = Kara(Position,Rotation)

    #Cached
    karaImage = None

    def __init__(self, world_size = [10,10], kara_pos = Position, kara_rot = Rotation):
        self.kara = Kara(kara_pos, kara_rot)
        self.size = world_size
    
    fpsClock = pygame.time.Clock()
    fps = 60

    def draw(self):

        if self.karaImage == None:
            self.karaImage = pygame.image.load("kara.png").convert_alpha()

        self.draw_grid(screen)
        self.draw_kara(screen)

        pygame.display.flip()
        self.fpsClock.tick(self.fps)
    
    def draw_grid(self,surface):
        for y in range(1,self.size[1]):
            line_poses = [[0,y*64],[self.size[0]*64,y*64]]
            pygame.draw.line(surface,pygame.Color(2, 62, 138),pygame.Vector2(line_poses[0][0],line_poses[0][1]),pygame.Vector2(line_poses[1][0],line_poses[1][1]),2)
        
        for x in range(1,self.size[0]):
            line_poses = [[x*64,0],[x*64,self.size[1]*64]]
            pygame.draw.line(surface,pygame.Color(2, 62, 138),pygame.Vector2(line_poses[0][0],line_poses[0][1]),pygame.Vector2(line_poses[1][0],line_poses[1][1]),2)

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

screen_size = (64*World.size[0], 64*World.size[1])
screen = pygame.display.set_mode((screen_size[0],screen_size[1]))
screen.fill((0,29,61))

pygame.display.set_caption("Better Kara 🫥")

world = World([10,10], Position(0,0), Rotation(0))

running = True
while running:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()

    world.draw()

    pygame.display.flip()