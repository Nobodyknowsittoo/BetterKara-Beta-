import kara
import time
import random

world = kara.World([10,10],kara.Position(5,5),kara.Rotation(90))

for i in range(10):

    world.draw() # Draw the world
    
    bug = world.kara # setting the bug to kara
    
    bug.move(1, world) # setting kara to a position
    
    time.sleep(1) # 1 second delay

print(random.randrange(0,10))