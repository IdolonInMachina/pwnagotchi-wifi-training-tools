import json
import random
import string


def generate_networks():
    generated = {}
    for num in range(0, 500):
        ssid = f"Pwnable network #{num}"
        password = ''.join(random.choice(string.ascii_uppercase +
                                         string.ascii_lowercase + string.digits) for _ in range(12))
        generated[ssid] = password

    with open('details.json', 'w') as f:
        json.dump(generated, f, indent=4)


if __name__ == '__main__':
    generate_networks()
