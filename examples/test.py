import time
import random

import kara
from kara import Position, Rotation, World

world = World([10,10],Position(3,5),Rotation(90))

for i in range(10):

    world.draw() # Draw the world
    
    bug = world.kara # setting the bug to kara
    
    world.draw()
    bug.position = Position(random.randrange(1,4),random.randrange(1,4))
    
    time.sleep(1) # 1 second delay

print(random.randrange(0,10))