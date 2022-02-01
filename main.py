#!/usr/bin/python

# Modified by james lewis (@baldengineer)
# MIT License
# 2020
# Script to connect to Multicomp Pro MP730026 by BLE with the Bleak Module
# Based on bleak example
# Requires mpp730026_decode_bytearray.py to be in the same directory

import logging
import asyncio
from sys import platform 
from ap_90epd import decode_data

from bleak import BleakClient, discover
from bleak import _logger as logger

# Change this to your meter's address, use bleak_scan.py to find out
address = ("00:00:00:00:00:00") # for Windows and Linux, my Device is called something like "FS9721-LP3"
#address = ("4DA7C422-D3DE-4AE5-AF14-CFEBDD3B85D1") # format for macOS -  this is unique per client+peripheral though.

if (platform != "darwin") and address == ("00:00:00:00:00:00"):
    raise ValueError("Invalid bluetooth mac address. Use BLE scanner app or bleak_scan.py to find out yours.")

# This characteristic UUID is for the BDM / MP730026 BLE message
# use Android App "BLE Scanner" and click the "N" badge to see which BLE item streams data, if this is not working for you
CHARACTERISTIC_UUID = "0000ffb2-0000-1000-8000-00805f9b34fb"

def notification_handler(sender, data, debug=False):
    """Simple notification handler which prints the data received."""
    #print("{0}: {1}".format(sender, data))
    if (debug): print("Handling...")
    if (debug): print("Data is " + str(type(data)))
    

    array = bytearray(data)
    
    if (debug): print(str(sender) + " : ", end="")
    if (debug): 
        for arr in array:
            print(hex(arr))
        print("")
    if (debug): print("... done handling")
    #print_DMM_packet(array)
    decode_data(data)

async def run(address, loop, debug=False):
    if debug:
        import sys

        # loop.set_debug(True)
        l = logging.getLogger("asyncio")
        l.setLevel(logging.DEBUG)
        h = logging.StreamHandler(sys.stdout)
        h.setLevel(logging.DEBUG)
        l.addHandler(h)
        logger.addHandler(h)


    # due to some quirks specific to CoreBluetooth, a service UUID must be supplied to
    # discover(), and we cannot connect directly to a given address: only a "device UUID"
    # which is specific to *both the client and server*. (i.e. the computer and the multimeter)
    # @see https://github.com/hbldh/bleak/issues/140
    if platform == "darwin":
        devices = await discover(service_uuids=["0000ffb0-0000-1000-8000-00805f9b34fb"])
        if not devices:
            raise Exception("unable to discover device with required service uuid.")
        address = devices[0]

    async with BleakClient(address, timeout=20.0) as client:
        if not client.is_connected:
            raise Exception("failed to connect to multimeter")

        logger.info("Connected to device: {0}".format(address))

        await client.start_notify(CHARACTERISTIC_UUID, notification_handler)
        await asyncio.sleep(460.0)
        await client.stop_notify(CHARACTERISTIC_UUID)


if __name__ == "__main__":
    import os
    # comment-in this if you have trouble in python debugging mode
    # os.environ["PYTHONASYNCIODEBUG"] = str(1)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(run(address, loop, False))
