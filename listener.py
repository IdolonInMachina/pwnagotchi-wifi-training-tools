import requests
import subprocess
import time
import os
import tempfile
import xml.etree.ElementTree as ET

broadcaster_ip = input('What is the ip of the broadcaster?: ')
broadcaster_port = input('What is the port of the broadcaster?: ')


def trigger_new_network():
    r = requests.get(f'http://{broadcaster_ip}:{broadcaster_port}/switch')
    return r.data()


def main():
    # Trigger new network
    details = trigger_new_network()
    # Disconnect from current network
    netsh(['wlan', 'disconnect'])
    # Wait for new network to be up
    time.sleep(20)
    # Connect to new network

    # Wait set amount of time


def netsh(args):
    return subprocess.run(['netsh'] + args)


def create_profile(profile):
    fd, path = tempfile.mkstemp()
    os.write(fd, profile.encode())
    netsh(['wlan', 'add', 'profile', f'filename=\"{path}\"'])
    os.close(fd)
    os.remove(path)


def generate_profile(ssid, passwd, remember=False):
    tree = ET.parse('profile-template.xml')
    profile = ET.tostring(tree.getroot()).decode()
    profile = profile.replace('{ssid}', ssid)
    profile = profile.replace('{passwd}', passwd)
    profile = profile.replace('{connmode}', 'auto' if remember else 'manual')
    return profile


def connect(ssid, password):
    create_profile(generate_profile(ssid, password))
    netsh(['wlan', 'connect', ssid])
