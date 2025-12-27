import datetime
import os
import sys
import time
from colorama import Fore, Style
from tqdm import tqdm

from leo import logs, logfile


def typewriter_effect(sentence, type_delay):
    for char in sentence:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(type_delay)


def topic():
    print(Fore.LIGHTYELLOW_EX + """
██╗     ███████╗ ██████╗     ████████╗███████╗██████╗ ███╗   ███╗██╗███╗   ██╗ █████╗ ██╗
██║     ██╔════╝██╔═══██╗    ╚══██╔══╝██╔════╝██╔══██╗████╗ ████║██║████╗  ██║██╔══██╗██║
██║     █████╗  ██║   ██║       ██║   █████╗  ██████╔╝██╔████╔██║██║██╔██╗ ██║███████║██║
██║     ██╔══╝  ██║   ██║       ██║   ██╔══╝  ██╔══██╗██║╚██╔╝██║██║██║╚██╗██║██╔══██║██║
███████╗███████╗╚██████╔╝       ██║   ███████╗██║  ██║██║ ╚═╝ ██║██║██║ ╚████║██║  ██║███████╗
╚══════╝╚══════╝ ╚═════╝        ╚═╝   ╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝╚══════╝
""")


def shut_down_VIS(username):
    for i in tqdm(range(100),
                  desc=Style.BRIGHT + Fore.LIGHTRED_EX + "#>Shutting Down all systems >>>>",
                  ascii=False, ncols=100):
        time.sleep(0.1)
    time.sleep(1)
    print("$>Good Bye!")
    logs(f"{datetime.now().strftime('%H_%M_%S')}>>>{username} shut down the system")
    logfile.close()
    time.sleep(2)
    os.system('cls||clear')
    sys.exit()