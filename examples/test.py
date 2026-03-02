import time
import random
from kara import *

world = World([10,10],Position(3,5),Rotation(90))

async def main():
    for i in range(10): # <- Hier kommt man nicht hin (wegen while block)

        world.draw() # Draw the world
    
        bug = world.kara # setting the bug to kara
    
        world.draw()
        bug.position = Position(random.randrange(1,4),random.randrange(1,4))
        time.sleep(1)
    

    print(random.randrange(0,10))

async def executeBoth():
    await asyncio.gather(asyncio.create_task(check_quit()), asyncio.create_task(main()))

asyncio.run(main())