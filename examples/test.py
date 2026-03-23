import time
import random
from src.kara import *
import src.kara as kara

kara.appearance.tile_size = 64
kara.appearance.line_width = 1

async def main():
    world = World([15,15],Position(12,1),Rotation(90)) # Init a world of size (10x10) with Kara at (3,5) rotated by 90°
    kara.world = world
    world.prepare()
    world.draw()

    bug = world.kara # setting the bug to kara
    for i in range(5):
        bug.put_leaf("sakura")
        world.draw()

        time.sleep(.5)
        bug.move(1)
        
        world.draw()

        time.sleep(.5)

    
    print(random.randrange(0,10))

async def executeBoth():
    await asyncio.gather(asyncio.create_task(check_quit()), asyncio.create_task(main()))

asyncio.run(main())