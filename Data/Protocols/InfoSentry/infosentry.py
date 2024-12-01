import subprocess

import whois


def infosentry(url):
    data = whois.whois(url, quiet=True)
    #print(data)
    command = f'cmd /c "(echo {data}) & pause"'
    subprocess.Popen(['start', 'cmd', '/k', command], shell=True)


if __name__ == '__main__':
    entry = input()
    infosentry(entry)
