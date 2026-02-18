import kara
import time
import random
world = kara.World([10,10],kara.Position(5,5),kara.Rotation(90))

for i in range(10):
    world.draw()
    bug = world.kara
    bug.move(1, world)
    time.sleep(1)
print(random.randrange(0,10))