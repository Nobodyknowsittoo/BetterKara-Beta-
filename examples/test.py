import time
import random
from src.kara import *
import src.kara as kara
import threading
import asyncio
import sys

test_output()

kara.appearance.tile_size = 64
kara.appearance.line_width = 1

async def main():
    global should_quit
    quit_check()
    world = World([15,15],Position(12,1),Rotation(90)) # Init a world of size (10x10) with Kara at (3,5) rotated by 90°
    kara.world = world
    world.prepare()
    world.draw()

    bug = world.kara # setting the bug to kara
    for i in range(5):
        if should_quit == True:
            sys.exit()
        bug.put_leaf("apple")
        world.draw()

        time.sleep(.5)
        bug.move(1)
        
        world.draw()

        time.sleep(.5)

    await check_quit()

    
    print(random.randrange(0,10))


#threading.Thread(target= main).start()
#threading.Thread(target= check_quit).start()

#async def executeBoth():
    #await asyncio.gather(asyncio.create_task(main()), asyncio.create_task(check_quit()))

#asyncio.run(executeBoth())
#asyncio.run(kara.check_quit())
asyncio.run(main())