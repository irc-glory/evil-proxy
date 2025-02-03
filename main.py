#0.3
import random, string, sys
from proxy.server import *
from colorama import Fore, init
init()

argumentative = False
if len(sys.argv) != 4 and len(sys.argv) != 1:
    print "Usage: python main.py <target> <host> <port>"
    sys.exit(1)
elif len(sys.argv) == 1:
    pass
else:
    argumentative = True
    target = sys.argv[1]
    host = sys.argv[2]
    port = sys.argv[3]

print """{}▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄
██ ▄▄▄█▀███▀█▄██ █████ ▄▄ █ ▄▄▀█▀▄▄▀█ █ █ ██ ███
██ ▄▄▄██ ▀ ██ ██ █████ ▀▀ █ ▀▀▄█ ██ █▀▄▀█ ▀▀ ███
██ ▀▀▀███▄███▄██▄▄████ ████▄█▄▄██▄▄██▄█▄█▀▀▀▄███
▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀{} v0.3{}
""".format(Fore.RED, Fore.LIGHTBLACK_EX, Fore.RED, Fore.RESET)

if argumentative:
    print "{}[ {}Target {}] --> {}{}".format(Fore.WHITE, Fore.RED, Fore.WHITE, Fore.LIGHTBLACK_EX, target)
    print "{}[ {}Host {}] --> {}{}".format(Fore.WHITE, Fore.RED, Fore.WHITE, Fore.LIGHTBLACK_EX, host)
    print "{}[ {}Port {}] --> {}{}".format(Fore.WHITE, Fore.RED, Fore.WHITE, Fore.LIGHTBLACK_EX, port)

else:
    target = raw_input("{}[ {}Target {}] --> {}".format(Fore.WHITE, Fore.RED, Fore.WHITE, Fore.LIGHTBLACK_EX))
    host = raw_input("{}[ {}Host {}] --> {}".format(Fore.WHITE, Fore.RED, Fore.WHITE, Fore.LIGHTBLACK_EX))
    port = raw_input("{}[ {}Port {}] --> {}".format(Fore.WHITE, Fore.RED, Fore.WHITE, Fore.LIGHTBLACK_EX))

    for i, name, explanation in zip([target, host, port], ["target-domain-name", "host-ip", "port"], ["Please input the target that you want to proxy to.\nExample: www.google.com", "Please input the host IP address.\nExample: 0.0.0.0", "Please input the port.\nExample: 8080"]):
        if i == "":
            print "\n{}No default case for {}{}.\n{}".format(Fore.RESET, Fore.RED, name, explanation)
            sys.exit(1)

secret = ''.join(random.choice(string.ascii_letters + string.digits + "@$-_/") for _ in range(random.randint(32, 55)))
# secret = 'or_whatever_you_want-_but_make_sure_it_is_a_valid_path_and_is_secure'
print "\n{}Your panel is available at {}http://{}:{}/{}{}".format(Fore.RESET, Fore.RED, host, port, secret, Fore.RESET)

print Fore.RESET
start_proxy(target, host, port, secret)
