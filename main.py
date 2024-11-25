import random, string
from proxy.server import *
from colorama import Fore, init
init()

print(f"""{Fore.RED}
▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄
██ ▄▄▄█▀███▀█▄██ █████ ▄▄ █ ▄▄▀█▀▄▄▀█ █ █ ██ ███
██ ▄▄▄██ ▀ ██ ██ █████ ▀▀ █ ▀▀▄█ ██ █▀▄▀█ ▀▀ ███
██ ▀▀▀███▄███▄██▄▄████ ████▄█▄▄██▄▄██▄█▄█▀▀▀▄███
▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀ {Fore.LIGHTBLACK_EX}v0.1{Fore.RED}
{Fore.RESET}""")

target = input(f"{Fore.WHITE}[ {Fore.RED}Target {Fore.WHITE}] --> {Fore.LIGHTBLACK_EX}")
host = input(f"{Fore.WHITE}[ {Fore.RED}Host {Fore.WHITE}] --> {Fore.LIGHTBLACK_EX}")
port = input(f"{Fore.WHITE}[ {Fore.RED}Port {Fore.WHITE}] --> {Fore.LIGHTBLACK_EX}")

for x, n, e in zip([target, host, port], ["target-domain_name", "host-ip", "port"], ["Please input the target that you want to proxy to.\nExample: www.google.com", "Please input the host in which the server will be running in.\nExample: localhost", "Please insert the port in which the server will be running in.\nExample: 3000"]):
    if x == "":
        print(f"\n{Fore.RESET}No default case for {Fore.RED}{n}{Fore.RESET}.\n{e}") # unknown x, name, explanation
        exit(0)

secret = ''.join(random.choice(string.ascii_letters + string.digits + '-') for _ in range(random.randint(32, 64)))
print(f"\n{Fore.RESET}Your panel is available at {Fore.RED}http://{host}:{port}/{secret}{Fore.RESET}.")

print(Fore.RESET)
start_proxy(target, host, port, secret)
