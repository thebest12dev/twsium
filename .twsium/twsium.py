#!/usr/bin/env python3

# Imports go here
import urllib3
import os
import subprocess
import time
from dotenv import load_dotenv


load_dotenv(dotenv_path="~/twsium/.env")

# .ROBLOSECURITY and userId parameters for querying. Make sure
# to fill those up in .env
roblosecurity = os.getenv("ROBLOSECURITY", None)
userid= os.getenv("USER_ID", None)

# Configuration for max tries till system reboot and autoclicker functionality.
enable_reboot = True
times_till_reboot_max = 3
enable_rejoin_protection = True

http = urllib3.PoolManager()
times_till_reboot = times_till_reboot_max
while True:
    try:
        if times_till_reboot <= 0 and enable_reboot:
            subprocess.run("sudo reboot", shell=True, text=True)

        # query prescences API to see if we're really online
        response = http.request(
            "POST", 
            "https://presence.roblox.com/v1/presence/users", 
            headers={"Cookie": ".ROBLOSECURITY="+roblosecurity},
	        json={"userIds": [userid]}
        )
        json_decoded = response.json()

        # Actual logic for the player finding 
        found_player = False
        data = json_decoded["userPresences"][0]
        if data["userPresenceType"] == 2:
            found_player = True


        # However, if not found...
        if not found_player:
            times_till_reboot -= 1

            print("Player not found! Restarting client")
            # TODO: Add Sober/Windows support for Roblox

            # we restart Waydroid
            subprocess.run("sudo waydroid shell am force-stop com.roblox.client", shell=True, text=True)
            time.sleep(5)
            subprocess.run('waydroid app intent android.intent.action.VIEW "roblox://placeId=3327818733" > /dev/null 2>&1 &', shell=True, text=True)
            time.sleep(30)
            continue
        else:
            print("Player is online");

            if enable_rejoin_protection:
                #TODO: more robust 
                subprocess.run("sudo waydroid shell input tap 350 710", shell=True ,text=True);

            times_till_reboot = times_till_reboot_max
    except Exception as e:
        print("Exception occured during parse! Not restarting client, but decrementing reboot!")
        times_till_reboot -= 1
    time.sleep(5)