#0.2
import random, string, sys
from proxy.server import *
from colorama import Fore, init
init()

argumentative = False
if len(sys.argv) != 4 and len(sys.argv) != 1:
    print("Usage: python main.py <target> <host> <port>")
    sys.exit(1)
elif len(sys.argv) == 1:
    pass
else:
    argumentative = True
    target = sys.argv[1]
    host = sys.argv[2]
    port = sys.argv[3]

print(f"""{Fore.RED}
▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄
██ ▄▄▄█▀███▀█▄██ █████ ▄▄ █ ▄▄▀█▀▄▄▀█ █ █ ██ ███
██ ▄▄▄██ ▀ ██ ██ █████ ▀▀ █ ▀▀▄█ ██ █▀▄▀█ ▀▀ ███
██ ▀▀▀███▄███▄██▄▄████ ████▄█▄▄██▄▄██▄█▄█▀▀▀▄███
▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀ {Fore.LIGHTBLACK_EX}v0.2{Fore.RED}
{Fore.RESET}""")

if argumentative:
    print(f"{Fore.WHITE}[ {Fore.RED}Target {Fore.WHITE}] --> {Fore.LIGHTBLACK_EX}{target}")
    print(f"{Fore.WHITE}[ {Fore.RED}Host {Fore.WHITE}] --> {Fore.LIGHTBLACK_EX}{host}")
    print(f"{Fore.WHITE}[ {Fore.RED}Port {Fore.WHITE}] --> {Fore.LIGHTBLACK_EX}{port}")

else:
    target = input(f"{Fore.WHITE}[ {Fore.RED}Target {Fore.WHITE}] --> {Fore.LIGHTBLACK_EX}")
    host = input(f"{Fore.WHITE}[ {Fore.RED}Host {Fore.WHITE}] --> {Fore.LIGHTBLACK_EX}")
    port = input(f"{Fore.WHITE}[ {Fore.RED}Port {Fore.WHITE}] --> {Fore.LIGHTBLACK_EX}")

    for x, n, e in zip([target, host, port], ["target-domain_name", "host-ip", "port"], ["Please input the target that you want to proxy to.\nExample: www.google.com", "Please input the host in which the server will be running in.\nExample: localhost", "Please insert the port in which the server will be running in.\nExample: 3000"]):
        if x == "":
            print(f"\n{Fore.RESET}No default case for {Fore.RED}{n}{Fore.RESET}.\n{e}") # unknown x, name, explanation
            sys.exit(1)

secret = ''.join(random.choice(string.ascii_letters + string.digits + '-' + '_' + '@') for _ in range(random.randint(32, 75)))
# secret = 'or whatever you want, but make sure it is a valid path and is secure'
print(f"\n{Fore.RESET}Your panel is available at {Fore.RED}http://{host}:{port}/{secret}{Fore.RESET}.")

print(Fore.RESET)
start_proxy(target, host, port, secret)
