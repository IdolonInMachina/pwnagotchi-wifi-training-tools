import sys
import json
import subprocess
from quart import Quart
import random
import asyncio

app = Quart(__name__)


@app.route('/')
async def base():
    return "Broadcaster Quart page"


@app.route('/switch')
async def switch():
    new_details = get_random_details()
    #loop = asyncio.get_event_loop()
    #loop.call_soon(perform_switch, new_details)
    # asyncio.run(perform_switch(new_details))
    task = asyncio.create_task(perform_switch(new_details))
    return new_details


async def perform_switch(details):
    print("Performing switch")
    await asyncio.sleep(10)
    print("Stopping hotspot")
    stop_status = stop_hotspot()
    print("Hotspot stopped with message: {}".format(stop_status))
    set_status = set_hotspot(details['ssid'], details['password'])
    if not set_status:
        print("Error. Could not set hospot")
        return
    print(
        f"Set hostpot to {details['ssid']} with password {details['password']}")
    start_status = start_hotspot()
    if not start_status:
        print("Error. Could not start hotspot")
        return
    print("Started hotspot")


def setup_hotspot():
    details = get_random_details()
    set_hotspot(details['ssid'], details['password'])
    start_hotspot()


def get_random_details():
    num = random.randint(0, 499)
    with open('details.json', 'r') as f:
        data = json.load(f)

    ssid = f"Pwnable network #{num}"
    return {'ssid': ssid, 'password': data[ssid]}


def check_admin_priv():
    try:
        output = subprocess.check_output(
            "whoami /groups | find \"S-1-16-12288\"", shell=True)
    except:
        return False
    if 'S-1-16-12288' in str(output):
        return True
    return False


def check_supported_drivers():
    output = subprocess.check_output("netsh wlan show drivers", shell=True)
    return "Hosted network supported  : Yes" in str(output)


def set_hotspot(ssid, password):
    output = subprocess.check_output(
        f"netsh wlan set hostednetwork mode=allow ssid=\"{ssid}\" key=\"{password}\"", shell=True)
    return "successfully changed" in str(output)


def start_hotspot():
    output = subprocess.check_output(
        "netsh wlan start hostednetwork", shell=True)
    return "started" in str(output)


def stop_hotspot():
    output = subprocess.check_output(
        "netsh wlan stop hostednetwork", shell=True)
    print(output)


if __name__ == '__main__':
    if check_admin_priv():
        if check_supported_drivers():
            setup_hotspot()
            app.run(host='0.0.0.0', threaded=False)
        else:
            print("You do not have the required drivers to run the hostednetwork")
            exit()
    else:
        print("Not running with admin privelidges")
        exit()
