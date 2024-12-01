import base64
import datetime
import getpass
import json
import os.path
import shutil
import time
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES
import winreg as reg
import maskpass
from colorama import Fore, Style
from tqdm import tqdm
from cryptography.fernet import Fernet

from Data.Imports.local_imports import *

username = r"Data\UserData\user.king"
password = r"Data\UserData\pass.king"
bkdir = r"Data\UserData\Backup"

KEY_PATH = r"SOFTWARE\LEO\KEY"

log_loc = "Data\\Logs"
logfile = open(f"{log_loc}\\log-{datetime.now().strftime('%Y_%m_%d~%H_%M_%S')}", "w")

hostname = socket.gethostname()
ip = socket.gethostbyname(hostname)

REG_PATH = r"SOFTWARE\LEO\USERDATA"

login_times = 0


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


def logs(indata):
    logfile.write(f"{indata}\n")


def login():
    global login_times, user, username
    try:
        # reg_key = reg.OpenKey(reg.HKEY_CURRENT_USER, REG_PATH, 0, reg.KEY_READ)
        print("$>Please enter your login credentials #>>>")
        usern = input("@>Username:- ")
        passw = maskpass.advpass("@>Password:- ")

        # username, _ = reg.QueryValueEx(reg_key, "Username")
        # password, _ = reg.QueryValueEx(reg_key, "Password")

        userfile = open(username, 'r')
        user = userfile.read()
        with open(password, 'rb') as passfile:
            passwr = passfile.read()

        decopwd = base64.b64decode(passwr)
        #print(decopwd.decode())
        if usern == user and passw == decopwd.decode():
            for i in tqdm(range(100),
                          desc=Style.BRIGHT + Fore.GREEN + "#>Checking User Credentials >>>>",
                          ascii=False, ncols=100):
                time.sleep(0.1)
            logs(f"{datetime.now().strftime('%H_%M_%S')}>>>{user} logged in")
            time.sleep(2)
            print("$>Completed!")
            time.sleep(1)
            print(f"$>Welcome {user}!\n")

            while True:
                mainTerminal(user)
    except (KeyboardInterrupt, EOFError):
        for i in tqdm(range(100),
                      desc=Style.BRIGHT + Fore.LIGHTRED_EX + "#>Shutting Down all systems >>>>",
                      ascii=False, ncols=100):
            time.sleep(0.1)
        time.sleep(1)
        print("$>Good Bye!")
        logs(f"{datetime.now().strftime('%H_%M_%S')}>>>{username} shutted down the system")
        logfile.close()
        time.sleep(2)
        os.system('cls||clear')
        sys.exit()


def check_key_exists(path):
    try:
        reg_key = reg.OpenKey(reg.HKEY_CURRENT_USER, path, 0, reg.KEY_READ)
        reg.CloseKey(reg_key)
        return True
    except FileNotFoundError:
        return False
    except Exception as e:
        print(f"An error occurred: {e}")
        return False


def signIN():
    username = r"Data\UserData\user.king"
    password = r"Data\UserData\pass.king"

    userfile = open(username, 'w')
    passfile = open(password, 'wb')

    print("$>Please enter your SignIN credentials #>>>")
    username = input("@>Username:- ")
    passwordin = maskpass.advpass("@>Password:- ")
    #reg_key = reg.CreateKey(reg.HKEY_CURRENT_USER, REG_PATH)

    encpwd = base64.b64encode(passwordin)
    userfile.write(username)
    passfile.write(encpwd)
    #ciper = Fernet(fernet_key.encode())
    #encpwd = ciper.encrypt(pwd)

    #reg.SetValueEx(reg_key, "Username", 0, reg.REG_SZ, username)
    #reg.SetValueEx(reg_key, "Password", 0, reg.REG_SZ, encpwd.decode())

    #reg.CloseKey(reg_key)
    print("Credentials stored successfully!")
    while True:
        mainTerminal(username)


def locked():
    print(Fore.LIGHTYELLOW_EX + """
-----------------------------------------------------------------------------------------------""")
    ab_poem = Fore.LIGHTRED_EX + """
        I was bright like a star in dawn
        Then I've been kicked from my home
        They say I'm EVIL
        But still I'm the WORST
        Who am I?....."""
    typewriter_effect(ab_poem, 0.21)
    name = input(Fore.RED + """
        \nAnswer---> """)
    if not (name == "Devil" or name == "Lucifer" or name == "Satan"):
        print(Style.RESET_ALL + "!>Sorry wrong answer!!!")
        for i in tqdm(range(100),
                      desc=Fore.RED + "#>Shutting Down all systems >>>>",
                      ascii=False, ncols=100):
            time.sleep(0.1)
        time.sleep(1)
        print(Style.RESET_ALL + "$>Good Bye!")
        logs(f"{datetime.now().strftime('%H_%M_%S')}>>>{user} shutted down the system")
        logfile.close()
        time.sleep(2)
        os.system('cls||clear')
        sys.exit()
    else:
        input(Style.RESET_ALL + "\nPress Enter to continue.....")
        paths = rf"{os.getcwd()}\Data\UserData\lock\Answer\noAnswer.hell"
        os.remove(paths)
        os.system('cls||clear')
        topic()
        while True:
            login()


def cmdinner(user):
    try:
        os.system('cls||clear')
        print(Style.BRIGHT + Fore.YELLOW + """
██╗     ███████╗ ██████╗     ████████╗███████╗██████╗ ███╗   ███╗██╗███╗   ██╗ █████╗ ██╗
██║     ██╔════╝██╔═══██╗    ╚══██╔══╝██╔════╝██╔══██╗████╗ ████║██║████╗  ██║██╔══██╗██║
██║     █████╗  ██║   ██║       ██║   █████╗  ██████╔╝██╔████╔██║██║██╔██╗ ██║███████║██║
██║     ██╔══╝  ██║   ██║       ██║   ██╔══╝  ██╔══██╗██║╚██╔╝██║██║██║╚██╗██║██╔══██║██║
███████╗███████╗╚██████╔╝       ██║   ███████╗██║  ██║██║ ╚═╝ ██║██║██║ ╚████║██║  ██║███████╗
╚══════╝╚══════╝ ╚═════╝        ╚═╝   ╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝╚══════╝
""")
        print(Fore.LIGHTYELLOW_EX + """
-----------------------------------------------------------------------------------------------""")
        print(Style.RESET_ALL + """
        1.Menu
        2.Settings
        3.Shutdown
        4.Restart
        5.Log Off
        6.About ME
        """)
        print(Fore.LIGHTYELLOW_EX + """
-----------------------------------------------------------------------------------------------""")
        query = input(Style.RESET_ALL + f"\n<{user}@{ip}><{os.getcwd()}>>>")
    except (KeyboardInterrupt, EOFError):
        for i in tqdm(range(100),
                      desc=Style.BRIGHT + Fore.LIGHTRED_EX + "#>Shutting Down all systems >>>>",
                      ascii=False, ncols=100):
            time.sleep(0.1)
        time.sleep(1)
        print("$>Good Bye!")
        logs(f"{datetime.now().strftime('%H_%M_%S')}>>>{user} shut down the system")
        logfile.close()
        time.sleep(2)
        os.system('cls||clear')
        sys.exit()
    return query


def mainTerminal(user):
    query = cmdinner(user)
    query = query.lower()

    menu_stack = []
    current_menu = cmdinner

    try:
        # settings
        if query == "2":
            os.system('cls||clear')
            logs(f"{datetime.now().strftime('%H_%M_%S')}>>>{user} entered to menu")
            print(Fore.LIGHTYELLOW_EX + """
██╗     ███████╗ ██████╗     ████████╗███████╗██████╗ ███╗   ███╗██╗███╗   ██╗ █████╗ ██╗
██║     ██╔════╝██╔═══██╗    ╚══██╔══╝██╔════╝██╔══██╗████╗ ████║██║████╗  ██║██╔══██╗██║
██║     █████╗  ██║   ██║       ██║   █████╗  ██████╔╝██╔████╔██║██║██╔██╗ ██║███████║██║
██║     ██╔══╝  ██║   ██║       ██║   ██╔══╝  ██╔══██╗██║╚██╔╝██║██║██║╚██╗██║██╔══██║██║
███████╗███████╗╚██████╔╝       ██║   ███████╗██║  ██║██║ ╚═╝ ██║██║██║ ╚████║██║  ██║███████╗
╚══════╝╚══════╝ ╚═════╝        ╚═╝   ╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝╚══════╝
""")
            print(Fore.LIGHTYELLOW_EX + """
-----------------------------------------------------------------------------------------------""")
            print(Style.RESET_ALL + """
        1.Change Username
        2.Change Password
        3.Change Root Path
        4.Clear Logs
        99.Back
        """)
            print(Fore.LIGHTYELLOW_EX + """
-----------------------------------------------------------------------------------------------""")
            query_sett = input(Style.RESET_ALL + f"\n<{user}@{ip}><{os.getcwd()}>>>")

            # change username
            if query_sett == "1":
                while not os.path.exists(bkdir):
                    os.mkdir(bkdir)
                bk = "Data\\UserData\\Backup\\user.king"
                while os.path.exists(bk):
                    os.remove(bk)
                shutil.move("Data\\UserData\\user.king", "Data\\UserData\\Backup")
                userpath = "Data\\UserData\\Backup\\user.king"
                # userpath = "Data\\UserData\\user_old.king"
                # os.rename(username, userpath)
                newname = input("#>Enter new username:-")
                newusern = open(username, 'w')
                newusern.write(newname)
                logs(f"{datetime.now().strftime('%H_%M_%S')}>>>{user} changed username to {newname}")
                os.remove(userpath)

            # change password
            elif query_sett == "2":
                while not os.path.exists(bkdir):
                    os.mkdir(bkdir)
                bk = "Data\\UserData\\Backup\\pass.king"
                while os.path.exists(bk):
                    os.remove(bk)
                shutil.move("Data\\UserData\\pass.king", "Data\\UserData\\Backup")
                passpath = "Data\\UserData\\Backup\\pass.king"
                # os.rename(password, passpath)
                oldpassfile = open(passpath, 'rb')
                oldpass = oldpassfile.read()
                decopwd = base64.b64decode(oldpass).decode("utf-8")
                newpass = maskpass.advpass("\n#>Enter new password:-")
                newpass2 = maskpass.advpass("#>Confirm new password:-")
                if not newpass == newpass2:
                    print("\n!!!>Passwords not same!")
                    return newpass
                else:
                    extpass = maskpass.advpass("#>Enter previous password:-")
                    if not extpass == decopwd:
                        print("!!!>Please enter correct previous password")
                        input("Press enter to continue....")
                        return extpass
                    else:
                        encopwd = base64.b64encode(newpass.encode("utf-8"))
                        with open(password, 'wb') as newpasswrd:
                            newpasswrd.write(encopwd)
                        logs(f"{datetime.now().strftime('%H_%M_%S')}>>>{user} changed password")
                        oldpassfile.close()
                        os.remove(passpath)

            # Change Root path
            elif query_sett == "3":
                # change root path
                cdpath = input("#>Enter Path:-")
                os.chdir(cdpath)

            # clear logs
            elif query_sett == "4":
                for i in tqdm(range(100),
                              desc=Style.BRIGHT + Fore.LIGHTRED_EX + "#>Clearing all Logs >>>>",
                              ascii=False, ncols=100):
                    time.sleep(0.1)
                    dirs = "Data\\Logs\\"
                    list_of_files = glob('Data\\Logs\\*')
                    latest_file = max(list_of_files, key=os.path.getctime)
                    # print(latest_file)
                    for clean_up in glob('Data\\Logs\\*'):
                        # print(clean_up)
                        if not clean_up.endswith(latest_file):
                            os.remove(clean_up)

            elif query_sett == "99":
                return query

        # Menu
        elif query == "1":
            os.system('cls||clear')
            logs(f"{datetime.now().strftime('%H_%M_%S')}>>>{user} entered to menu")
            topic()
            menu_stack.append(current_menu)
            current_menu = "protocol_menu"
            print(Fore.LIGHTYELLOW_EX + """
-----------------------------------------------------------------------------------------------""")
            print(Style.RESET_ALL + """
        1.Reconnaissance Protocols
        2.Network Analysis Protocols
        3.Exploitation Protocols
        98.TunnelChat ---> Hidden Chat System
        99.Back
                """)
            print(Fore.LIGHTYELLOW_EX + """
-----------------------------------------------------------------------------------------------""")
            query_menu = input(Style.RESET_ALL + f"\n<{user}@{ip}><{os.getcwd()}>>>")

            if query_menu == "1":
                os.system('cls||clear')
                logs(f"{datetime.now().strftime('%H_%M_%S')}>>>{user} entered to menu_recon")
                topic()
                menu_stack.append(current_menu)
                current_menu = "recon_menu"
                print(Fore.LIGHTYELLOW_EX + """
-----------------------------------------------------------------------------------------------""")
                print(Style.RESET_ALL + """
        1.Sherlock ---> Search every social media networks for specific username/usernames
        2.Sfuzzer ---> A tool to list down all subdomains of a domain.
        3.SiteCoreX ---> A tool to list down all software of a domain.
        4.InfoSentry ---> A Whois protocol for gathering domain registration information
        5.ÆtherMap ---> A Protocol for scan devices in a local network (same network that you in)
        99.Back
                                """)
                print(Fore.LIGHTYELLOW_EX + """
-----------------------------------------------------------------------------------------------""")
                query_menu_recon = input(Style.RESET_ALL + f"\n<{user}@{ip}><{os.getcwd()}>>>")

                #Sherlock
                if query_menu_recon == "1":
                    os.system('cls||clear')
                    logs(f"{datetime.now().strftime('%H_%M_%S')}>>>{user} entered to Sherlock Module")
                    print(Fore.LIGHTYELLOW_EX + """
                ███████╗██╗  ██╗███████╗██████╗ ██╗      ██████╗  ██████╗██╗  ██╗
                ██╔════╝██║  ██║██╔════╝██╔══██╗██║     ██╔═══██╗██╔════╝██║ ██╔╝
                ███████╗███████║█████╗  ██████╔╝██║     ██║   ██║██║     █████╔╝
                ╚════██║██╔══██║██╔══╝  ██╔══██╗██║     ██║   ██║██║     ██╔═██╗
                ███████║██║  ██║███████╗██║  ██║███████╗╚██████╔╝╚██████╗██║  ██╗
                ╚══════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚══════╝ ╚═════╝  ╚═════╝╚═╝  ╚═╝
                """)
                    # print("@>Do you need Tor system(Make requests over Tor; increases runtime; requires Tor to be installed "
                    # "and in system path.)")
                    # sherltor = input(f"\n<{user}@localhost><sherlock>>>")
                    print("Creator ----> Siddharth Dushantha")
                    print(Style.RESET_ALL)
                    print(
                        Style.BRIGHT + Fore.LIGHTGREEN_EX + "@" + Fore.LIGHTYELLOW_EX + ">" + Fore.WHITE + "Enter username you want to search")
                    sherluname = input(f"\n<{user}@{ip}><sherlock>>>")
                    print(
                        Style.BRIGHT + Fore.LIGHTGREEN_EX + "@" + Fore.LIGHTYELLOW_EX + ">" + Fore.WHITE + "File output type. Eg: .txt .csv etc.")
                    sherlftype = input(f"\n<{user}@{ip}><sherlock>>>")
                    print(
                        Style.BRIGHT + Fore.LIGHTGREEN_EX + "@" + Fore.LIGHTYELLOW_EX + ">" + Fore.WHITE + "Add a proxy to request over. Eg: socks5://127.0.0.1:1080")
                    sherlproxy = input(f"\n<{user}@{ip}><sherlock>>>")
                    print(
                        Style.BRIGHT + Fore.LIGHTGREEN_EX + "@" + Fore.LIGHTYELLOW_EX + ">" + Fore.WHITE + "Show only founded data.(true or false)")
                    sherlprint = input(f"\n<{user}@{ip}><sherlock>>>")
                    print(
                        Style.BRIGHT + Fore.LIGHTGREEN_EX + "@" + Fore.LIGHTYELLOW_EX + ">" + Fore.WHITE + "How many seconds do you need before timeout a request?(Default None)")
                    sherltime = int(input(f"\n<{user}@{ip}><sherlock>>>"))

                    if sherlprint == "true":
                        data = "Data\\Protocols\\Sherlock\\resources\\data.json"
                        datajson = open(data)
                        jsond = json.load(datajson)
                        query_notify = QueryNotifyPrint(result=None,
                                                        verbose=False,
                                                        print_all=False)
                        results = sherlock(sherluname, site_data=jsond, query_notify=query_notify, tor=False,
                                           unique_tor=False,
                                           proxy=sherlproxy, timeout=sherltime)

                        if sherlftype == ".txt":
                            result_file = f"C:\\Users\\{getpass.getuser()}\\Desktop\\{sherluname}.txt"
                            with open(result_file, "w", encoding="utf-8") as file:
                                exists_counter = 0
                                for website_name in results:
                                    dictionary = results[website_name]
                                    if dictionary.get("status").status == QueryStatus.CLAIMED:
                                        exists_counter += 1
                                        file.write(dictionary["url_user"] + "\n")
                                file.write(f"Total Websites Username Detected On : {exists_counter}")

                        elif sherlftype == ".csv":
                            with open(f"C:\\Users\\{getpass.getuser()}\\Desktop\\{sherluname}.csv", "w", newline='',
                                      encoding="utf-8") as csv_report:
                                writer = csv.writer(csv_report)
                                writer.writerow(['username',
                                                 'name',
                                                 'url_main',
                                                 'url_user',
                                                 'exists',
                                                 'http_status',
                                                 'response_time_s'
                                                 ]
                                                )
                                for site in results:
                                    response_time_s = results[site]['status'].query_time
                                    if response_time_s is None:
                                        response_time_s = ""
                                    writer.writerow([sherluname,
                                                     site,
                                                     results[site]['url_main'],
                                                     results[site]['url_user'],
                                                     str(results[site]['status'].status),
                                                     results[site]['http_status'],
                                                     response_time_s
                                                     ]
                                                    )
                    else:
                        data = "Data\\Protocols\\Sherlock\\resources\\data.json"
                        datajson = open(data)
                        jsond = json.load(datajson)
                        query_notify = QueryNotifyPrint(result=None,
                                                        verbose=False,
                                                        print_all=True)
                        results = sherlock(sherluname, site_data=jsond, query_notify=query_notify, tor=False,
                                           unique_tor=False,
                                           proxy=sherlproxy, timeout=sherltime)
                        if sherlftype == ".txt":
                            result_file = f"C:\\Users\\{getpass.getuser()}\\Desktop\\{sherluname}.txt"
                            with open(result_file, "w", encoding="utf-8") as file:
                                exists_counter = 0
                                for website_name in results:
                                    dictionary = results[website_name]
                                    if dictionary.get("status").status == QueryStatus.CLAIMED:
                                        exists_counter += 1
                                        file.write(dictionary["url_user"] + "\n")
                                file.write(f"Total Websites Username Detected On : {exists_counter}")

                        elif sherlftype == ".csv":
                            with open(f"C:\\Users\\{getpass.getuser()}\\Desktop\\{sherluname}.csv", "w", newline='',
                                      encoding="utf-8") as csv_report:
                                writer = csv.writer(csv_report)
                                writer.writerow(['username',
                                                 'name',
                                                 'url_main',
                                                 'url_user',
                                                 'exists',
                                                 'http_status',
                                                 'response_time_s'
                                                 ]
                                                )
                                for site in results:
                                    response_time_s = results[site]['status'].query_time
                                    if response_time_s is None:
                                        response_time_s = ""
                                    writer.writerow([sherluname,
                                                     site,
                                                     results[site]['url_main'],
                                                     results[site]['url_user'],
                                                     str(results[site]['status'].status),
                                                     results[site]['http_status'],
                                                     response_time_s
                                                     ]
                                                    )

                #Sfuzzer
                elif query_menu_recon == "2":
                    os.system('cls||clear')
                    topic()
                    print(Fore.LIGHTYELLOW_EX + """
-----------------------------------------------------------------------------------------------""")
                    resultpath = f"C:\\User\\{getpass.getuser()}\\Desktop"
                    print("@>Enter Domain name: (Ex:google.com)")
                    domain = input(f"\n<{user}@{ip}><SFUZZER>>>")
                    print("@>No. of threads: (If you dont know this enter 40)")
                    threads = input(f"\n<{user}@{ip}><SFUZZER>>>")
                    print("@>Do you need to show result realtime? (true or false)")
                    verbose = input(f"\n<{user}@{ip}><SFUZZER>>>")
                    if verbose == "True" or "true":
                        txtfile = f"{resultpath}\\{domain}.txt"
                        results = sublister(domain, threads, txtfile, verbose=True)
                        print(results)
                    else:
                        txtfile = f"{resultpath}\\{domain}.txt"
                        sublister(domain, threads, txtfile, verbose=False)

                #SiteCoreX
                elif query_menu_recon == "3":
                    os.system('cls||clear')
                    topic()
                    print(Fore.LIGHTYELLOW_EX + """
-----------------------------------------------------------------------------------------------""")
                    print("@>Enter Domain name: (Ex:google.com)")
                    domain = input(f"\n<{user}@{ip}><SITECOREX>>>")
                    try:
                        pass
                    except UserWarning:
                        sitecorex(domain)

                #InfoSentry
                elif query_menu_recon == "4":
                    os.system('cls||clear')
                    topic()
                    print(Fore.LIGHTYELLOW_EX + """
-----------------------------------------------------------------------------------------------""")
                    print("@>Enter Domain name: (Ex:google.com)")
                    domain = input(f"\n<{user}@{ip}><INFOSENTRY>>>")
                    infosentry(domain)

                #ÆtherMap
                elif query_menu_recon == "5":
                    def list_netifaces():
                        interfaces = psutil.net_if_addrs()
                        print("Interfaces available in this PC: ")
                        for interface_name in interfaces:
                            print(f"    {interface_name}")

                    os.system('cls||clear')
                    topic()
                    print(Fore.LIGHTYELLOW_EX + """
-----------------------------------------------------------------------------------------------""")
                    list_netifaces()
                    print("")
                    print("@>Enter Network Interface name")
                    NI_name = input(f"\n<{user}@{ip}><ÆTHERMAP>>>")
                    aethermap(NI_name)

                elif query_menu_recon == "99":
                    if menu_stack:
                        current_menu = menu_stack.pop()

            elif query_menu == "2":
                os.system('cls||clear')
                topic()
                menu_stack.append(current_menu)
                current_menu = "net_menu"
                print(Fore.LIGHTYELLOW_EX + """
-----------------------------------------------------------------------------------------------""")
                print(Style.RESET_ALL + """
        1.Portscanner ---> Search and detect every port in target system(for now works only in Linux based OS)
        99.Back""")
                print(Fore.LIGHTYELLOW_EX + """
-----------------------------------------------------------------------------------------------""")
                query_net = input(Style.RESET_ALL + f"\n<{user}@{ip}><{os.getcwd()}>>>")

                if query_net == "1":
                    logs(f"{datetime.now().strftime('%H_%M_%S')}>>>{user} entered to PortScanner Module")
                    print("@>Please enter target IP address")
                    target_ip = input(f"<{user}@{ip}><PortHunter>>>")
                    print("@>Enter number of ports you want to scan")
                    ports = int(input(f"<{user}@{ip}><PortHunter>>>"))
                    hunter(target_ip, ports)

                elif query_net == "99":
                    if menu_stack:
                        current_menu = menu_stack.pop()

            elif query_menu == "3":
                os.system('cls||clear')
                topic()
                menu_stack.append(current_menu)
                current_menu = "exploit_menu"
                print(Fore.LIGHTYELLOW_EX + """
-----------------------------------------------------------------------------------------------""")
                print(Style.RESET_ALL + """
        1.ARP Spoofer ---> Intercept communication between two parties (Man in the Middle (MitM) attack)
        2.Password Sniffer ---> Intercept packets to get passwords and usernames
        3.Access Point Cracking ---> For breaking into wireless access points
        99.Back""")

                print(Fore.LIGHTYELLOW_EX + """
-----------------------------------------------------------------------------------------------""")
                query_menu_exploit = input(Style.RESET_ALL + f"\n<{user}@{ip}><{os.getcwd()}>>>")

                # ARP Spoofer
                if query_menu_exploit == "1":
                    print("@>Please enter target IP")
                    target_ip = str(input(f"\n<{user}@{ip}><ARPS>>>"))
                    print("@>Please enter router IP")
                    router_ip = str(input(f"\n<{user}@{ip}><ARPS>>>"))
                    target_mac = str(get_mac_address(target_ip))
                    router_mac = str(get_mac_address(router_ip))
                    try:
                        while True:
                            spoof(router_ip, target_ip, router_mac, target_mac)
                            time.sleep(2)
                    except KeyboardInterrupt:
                        print('Closing ARP Spoofer.')

                # pwdsniffer
                elif query_menu_exploit == "2":
                    print("@>Please enter Network interface type to work with(example:eth0)")
                    iface = input(f"\n<{user}@{ip}><PWD_Sniffer>>>")
                    try:
                        return iface  # sniff(iface=iface, prn=pkt_parser, store=0)
                    except KeyboardInterrupt:
                        print('Exiting')

                # ACpoint
                elif query_menu_exploit == "3":
                    os.system('cls||clear')
                    topic()
                    print(Style.RESET_ALL + """
-----------------------------------------------------------------------------------------------""")
                    print("""
            1.Check AccessPoint PMKID status
            2.PMKID Cracker""")
                    print(Style.RESET_ALL + """
-----------------------------------------------------------------------------------------------""")
                    query_ap = input(f"\n<{user}@{ip}><{os.getcwd()}>>>")

                    if query_ap == "1":
                        print("@>Please enter your Network interface")
                        interface = str(input(f"\n<{user}@{ip}><PMKIDS>>>"))
                        print("@>Please enter target SSID")
                        essid = str(input(f"\n<{user}@{ip}><PMKIDS>>>"))

                        rawSocket = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.htons(0x0003))
                        rawSocket.bind((interface, 0x0003))

                        detector(rawSocket, essid)
                        input("\n$>Press enter to continue.....")

                elif query_menu_exploit == "99":
                    if menu_stack:
                        current_menu = menu_stack.pop()

            elif query_menu == "98":
                os.system('cls||clear')
                topic()
                print(Fore.LIGHTYELLOW_EX + """
-----------------------------------------------------------------------------------------------""")
                print(Style.RESET_ALL + """
        1.Make new chat room
        2.Join existing chat room
        99.Back
        """)
                print(Fore.LIGHTYELLOW_EX + """
-----------------------------------------------------------------------------------------------""")
                query_chat = input(Style.RESET_ALL + f"\n<{user}@{ip}><{os.getcwd()}>>>")

                if query_chat == "1":
                    inputip = input("\nEnter IP to start the room(enter 'localhost' if you want launch on localhost): ")
                    inputport = int(input("Enter port to broadcast the room: "))
                    server(inputip, inputport)
                    client_main(inputip, inputport)

                elif query_chat == "2":
                    inputip = input("\nEnter IP to enter the room: ")
                    inputport = int(input("Enter port to enter the room: "))
                    client_main(inputip, inputport)

                elif query_chat == "99":
                    return query_menu

                else:
                    print(Fore.LIGHTRED_EX + "!>Enter correct input...")
                    time.sleep(3)
                    return query_chat

            elif query_menu == "99":
                if menu_stack:
                    current_menu = menu_stack.pop()

        # Shutdown
        elif query == "3":
            for i in tqdm(range(100),
                          desc=Style.BRIGHT + Fore.LIGHTRED_EX + "#>Shutting Down all systems >>>>",
                          ascii=False, ncols=100):
                time.sleep(0.1)
            time.sleep(1)
            print("$>Good Bye!")
            logs(f"{datetime.now().strftime('%H_%M_%S')}>>>{user} shutted down the system")
            logfile.close()
            time.sleep(2)
            os.system('cls||clear')
            sys.exit()

        # Restart
        elif query == "4":
            enterput = input("#>Press enter to restart.....")
            if enterput == "" or enterput != "":
                for i in tqdm(range(100),
                              desc=Style.BRIGHT + Fore.CYAN + "#>Restarting all systems >>>>",
                              ascii=False, ncols=100):
                    time.sleep(0.1)
                time.sleep(1)
                logs(f"{datetime.now().strftime('%H_%M_%S')}>>>{user} restarted the system")
                os.system('cls||clear')
                topic()
                print(Style.RESET_ALL)
                while True:
                    login()

        # AboutME
        elif query == "6":
            os.system('cls||clear')
            topic()
            ans = open(rf"{os.getcwd()}\Data\UserData\lock\Answer\noAnswer.hell", 'w')
            ans.write("YOU ARE WRONG! FOOL!")
            ans.close()
            print("""
-----------------------------------------------------------------------------------------------""")
            typewriter_effect(Fore.LIGHTRED_EX + """
    'We work in the dark to serve the light'""", 0.21)
            typewriter_effect(Fore.LIGHTRED_EX + """
    'Facilitate the faith of those who deserve to die'""", 0.21)
            typewriter_effect(Fore.LIGHTRED_EX + """
    'Commit to the Creed which we are submitted'""", 0.21)
            typewriter_effect(Fore.RED + """
    'NOTHING IS TRUE, EVERYTHING IS PERMITTED'""", 0.21)
            print(Fore.LIGHTYELLOW_EX + """\n
-----------------------------------------------------------------------------------------------""")
            ab_poem = Fore.LIGHTRED_EX + """\n
    I was bright like a star in dawn
    Then I've been kicked from my home
    They say I'm EVIL
    But still I'm the WORST
    Who am I?....."""
            typewriter_effect(ab_poem, 0.21)
            name = input(Fore.RED + """
    \nAnswer---> """)
            if not (name == "Devil" or name == "Lucifer" or name == "Satan"):
                print(Fore.LIGHTYELLOW_EX + """\n
-----------------------------------------------------------------------------------------------""")
                print("!>Sorry wrong answer!!!")
                for i in tqdm(range(100),
                              desc=Fore.RED + "#>Shutting Down all systems >>>>",
                              ascii=False, ncols=100):
                    time.sleep(0.1)
                time.sleep(1)
                print("$>Good Bye!")
                ans = open(rf"{os.getcwd()}\Data\UserData\lock\Answer\noAnswer.hell", 'w')
                ans.write("YOU ARE WRONG! FOOL!")
                ans.close()
                logs(f"{datetime.now().strftime('%H_%M_%S')}>>>{user} gave wrong answer!!!")
                logfile.close()
                time.sleep(2)
                os.system('cls||clear')
                sys.exit()
            else:
                print(Fore.LIGHTYELLOW_EX + """\n
-----------------------------------------------------------------------------------------------""")
                input(Style.RESET_ALL + "\nPress Enter to continue.....")
                paths = rf"{os.getcwd()}\Data\UserData\lock\Answer\noAnswer.hell"
                os.remove(paths)

    except (KeyboardInterrupt, EOFError) as e:
        for i in tqdm(range(100),
                      desc=Fore.RED + "#>Shutting Down all systems >>>>",
                      ascii=False, ncols=100):
            time.sleep(0.1)
        time.sleep(1)
        print("$>Good Bye!")
        logs(f"{datetime.now().strftime('%H_%M_%S')}>>>{e}")
        logs(f"{datetime.now().strftime('%H_%M_%S')}>>>{user} shutted down the system")
        logfile.close()
        time.sleep(2)
        os.system('cls||clear')
        sys.exit()


if __name__ == '__main__':
    os.system('cls||clear')
    # os.system('mode con: cols=115 lines=20')
    topic()
    print(Style.RESET_ALL)
    hellpath = rf"{os.getcwd()}\Data\UserData\lock\Answer\noAnswer.hell"
    while True:
        if os.path.exists(hellpath):
            locked()
        else:
            if os.path.exists(username) and os.path.exists(password):
                print("fucked")
                login()
            else:
                print("not fucked")
                signIN()
