import time
import random
from src.kara import *
import src.kara as kara

kara.appearance.tile_size = 256
kara.appearance.line_width = 8
kara.appearance.action_duration = 0.5


async def main():
    world = World([5,3],Position(1,1),Rotation(270)) # Init a world of size (10x10) with Kara at (3,5) rotated by 90°
    kara.world = world
    world.prepare()

    bug = world.kara # setting the bug to kara

    index = 0

    bug.put_carpet("white")
    bug.move(1)
    bug.put_carpet("red")
    bug.move(1)
    bug.put_carpet("green")
    bug.move(1)

    while True:
        time.sleep(.1)
    print(random.randrange(0,10))

async def executeBoth():
    await asyncio.gather(asyncio.create_task(check_quit()), asyncio.create_task(main()))

asyncio.run(main())