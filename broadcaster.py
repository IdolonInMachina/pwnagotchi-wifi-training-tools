import sys
import json
import subprocess
from flask import Flask
import random
import asyncio

app = Flask(__name__)


@app.route('/')
def base():
    return "Broadcaster Flask page"


@app.route('/switch')
def switch():
    new_details = get_random_details()
    loop = asyncio.get_event_loop()
    loop.call_later(10, perform_switch, new_details)
    return new_details


def perform_switch(details):
    stop_status = stop_hotspot()
    set_status = set_hostpot(details['ssid'], details['password'])
    if not set_status:
        print("Error. Could not set hospot")
        return
    print(
        f"Set hostpot to {details['ssid']} with password {details['password']}")
    start_status = start_hostpot()
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
        setup_hotspot()
    else:
        print("Not running with admin privelidges")
        exit()
