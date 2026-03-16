import time
import random
from src.kara import *
import src.kara as kara

kara.appearance.tile_size = 64
kara.appearance.line_width = 1

async def main():
    world = World([9,9],Position(2,1),Rotation(90)) # Init a world of size (10x10) with Kara at (3,5) rotated by 90°
    kara.world = world
    world.prepare()
    world.draw()

    for i in range(10):
        bug = world.kara # setting the bug to kara
        bug.move(1)
        world.draw()
        bug.put_leaf("sakura")
        time.sleep(1)
    

    print(random.randrange(0,10))

async def executeBoth():
    await asyncio.gather(asyncio.create_task(check_quit()), asyncio.create_task(main()))

asyncio.run(main())