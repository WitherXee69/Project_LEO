import subprocess
from collections import namedtuple

NetworkDevice = namedtuple('NetworkDevice', ['ip_address', 'mac_address', 'device'])
devices = []
output = subprocess.check_output(['arp', '-a'])
output = output.decode('utf-8').split('\n')
for line in output:
    if '(' in line and ')' in line:
        ip_address = line.split('(')[1].split(')')[0]
        mac_address = line.split()[3]
        device = line.split(' ')[5].strip('()')
        devices.append(NetworkDevice(ip_address, mac_address, device))
print(devices)