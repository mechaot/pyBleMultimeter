import asyncio
from bleak import discover
import time
from sys import platform

# Your meter's MAC will probably start with A5:B3:C2...
# and have the name "BDM"
# A5:B3:C2:22:14:D2: BDM

async def run():
    kwargs = {} if platform != "darwin" else {
        "service_uuids": ["0000ffb0-0000-1000-8000-00805f9b34fb"]
    }

    devices = await discover(**kwargs)
    for d in devices:
        print(d)

while(1):
	loop = asyncio.get_event_loop()
	loop.run_until_complete(run())
	time.sleep(1)
