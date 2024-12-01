import ipaddress
from scapy.layers.l2 import *
import platform
import psutil
import re
import subprocess
import socket
import matplotlib.pyplot as plt
import networkx as nx
import plotly.graph_objects as go


def aethermap(infacename):
    def get_network_info_windows(iface_name):
        global ip_address, netmask, gatewayIPs
        addrs = psutil.net_if_addrs()
        if iface_name in addrs:
            addrs_list = addrs[iface_name]
            # print(f"\nInterface: {iface_name}")
            for addr in addrs_list:
                if addr.family == socket.AF_INET:
                    # print(f"  IP Address: {addr.address}")
                    ip_address = addr.address
                    # print(f"  Netmask: {addr.netmask}")
                    netmask = addr.netmask

        ps_command = 'Get-NetRoute -DestinationPrefix "0.0.0.0/0" | Select-Object -ExpandProperty NextHop'
        process = subprocess.Popen(["powershell", "-Command", ps_command], stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()

        if process.returncode != 0:
            print("Error:", stderr.decode())
            return None

        output = stdout.decode().strip()
        gatewayIPs = output.split('\n')
        return ip_address, netmask, gatewayIPs

    def get_network_info_linux(iface_name):
        global ip_address, netmask, gateways
        addrs = psutil.net_if_addrs()
        if iface_name in addrs:
            interface_addrs = addrs[iface_name]
            for addr in interface_addrs:
                if addr.family == socket.AF_INET:
                    ip_address = addr.address
                    netmask = addr.netmask
                    print(f"IP Address: {ip_address}")
                    print(f"Subnet Mask: {netmask}")

        # Get default gateways
        result = subprocess.run(['ip', 'route'], capture_output=True, text=True)
        output = result.stdout
        gateways = re.findall(r"default via ([^\s]+)", output)

        print("\nDefault Gateways:")
        for gateway in gateways:
            print(f"  {gateway}")
        return ip_address, netmask, gateways

    def get_network_info_mac(iface_name):
        global ip_address, netmask, gateways
        addrs = psutil.net_if_addrs()
        if iface_name in addrs:
            interface_addrs = addrs[iface_name]
            for addr in interface_addrs:
                if addr.family == socket.AF_INET:
                    ip_address = addr.address
                    netmask = addr.netmask
                    print(f"IP Address: {ip_address}")
                    print(f"Subnet Mask: {netmask}")

        result = subprocess.run(['netstat', '-rn'], stdout=subprocess.PIPE, text=True)

        # Split the output into lines
        lines = result.stdout.splitlines()

        # Filter for the line that contains the default route
        for line in lines:
            if 'default' in line and iface_name in line:
                # The default gateway address is usually the second column
                parts = line.split()
                if len(parts) > 1:
                    gateways = parts[1]

        return ip_address, netmask, gateways

    def list_netifaces():
        interfaces = psutil.net_if_addrs()
        print("Interfaces available in this PC: \n")
        for interface_name in interfaces:
            print(f"    {interface_name}")

    def get_network_info(iface_name):
        global ip_address, netmask, interface_stats
        addrs = psutil.net_if_addrs()
        gateways = psutil.net_if_stats()

        if iface_name in addrs:
            interface_addrs = addrs[iface_name]
            for addr in interface_addrs:
                if addr.family == socket.AF_INET:
                    ip_address = addr.address
                    netmask = addr.netmask
                    print(f"IP Address: {ip_address}")
                    print(f"Subnet Mask: {netmask}")

        if iface_name in gateways:
            interface_stats = gateways[iface_name]
            print(f"Default Gateway: {interface_stats.gateway}")

        return ip_address, netmask, interface_stats.gateway

    def get_network_range(gateway_ip, subnet_mask):
        network = ipaddress.ip_network(f'{gateway_ip}/{subnet_mask}', strict=False)
        return network

    def arp_scan_new(network):
        try:
            ip_network = ipaddress.ip_network(network, strict=False)
            ip_list = [str(ip) for ip in ip_network.hosts()]
        except ValueError as e:
            print(f"Invalid IP range: {e}")
            return []

        devices = []
        for ip in ip_list:
            arp_request = ARP(pdst=ip)
            broadcast = Ether(dst="ff:ff:ff:ff:ff:ff")
            arp_request_broadcast = broadcast / arp_request
            answered_list = srp(arp_request_broadcast, timeout=1, verbose=False)[0]

            for element in answered_list:
                device_info = {
                    "ip": element[1].psrc,
                    "mac": element[1].hwsrc
                }
                devices.append(device_info)
                print(f"Found device: IP: {device_info['ip']}, MAC: {device_info['mac']}")

        return devices

    def visualize_network_with_colors(devices):
        G = nx.Graph()
        ap = "AP"
        G.add_node(ap, label="AP")

        for device in devices:
            label = f"{device['ip']}\n{device['mac']}"
            G.add_node(device['ip'], label=label)
            G.add_edge(ap, device["ip"])

        labels = nx.get_node_attributes(G, 'label')

        pos = nx.spring_layout(G)
        nx.draw(G, pos, with_labels=True, node_color="skyblue", labels=labels, edge_color="gray", node_size=2000, font_size=10)
        plt.title("Network Visualization")
        plt.show()

    def visualizing_network(devices):
        global router_ip
        G = nx.Graph()

        # Add nodes and their details (IP and MAC)
        for device in devices:
            G.add_node(device["ip"], mac=device["mac"])

        # Add edges (for example, connecting devices to a router)
        for device in devices[0]:
            router_ip = int(device["ip"])
            G.add_node(router_ip, mac=device["mac"])

        for device in devices[1:]:
            G.add_edge(router_ip, device["ip"])

        # Set positions for nodes using a layout algorithm
        pos = nx.spring_layout(G)

        # Extract positions for nodes
        node_x = []
        node_y = []
        for node in G.nodes():
            x, y = pos[node]
            node_x.append(x)
            node_y.append(y)

        # Create node trace for Plotly visualization
        node_trace = go.Scatter(
            x=node_x, y=node_y,
            mode='markers+text',
            text=[f"{node}<br>MAC: {G.nodes[node]['mac']}" for node in G.nodes()],
            marker=dict(size=20, color='lightblue', line=dict(width=2)),
            textposition='bottom center',
            hoverinfo='text'
        )

        # Create edge trace for Plotly visualization
        edge_x = []
        edge_y = []
        for edge in G.edges():
            x0, y0 = pos[edge[0]]
            x1, y1 = pos[edge[1]]
            edge_x.extend([x0, x1, None])
            edge_y.extend([y0, y1, None])

        edge_trace = go.Scatter(
            x=edge_x, y=edge_y,
            line=dict(width=2, color='lightgray'),
            hoverinfo='none',
            mode='lines'
        )

        # Create figure layout for Plotly
        fig = go.Figure(data=[edge_trace, node_trace],
                        layout=go.Layout(
                            title='ÆtherMap Network Visualization',
                            showlegend=False,
                            hovermode='closest',
                            margin=dict(b=0, l=0, r=0, t=40),
                            xaxis=dict(showgrid=False, zeroline=False),
                            yaxis=dict(showgrid=False, zeroline=False))
                        )

        # Show the graph
        fig.show()

    #list_netifaces()

    os_type = platform.system()

    if os_type == 'Windows':
        ip, subnet_mask, gateway_ip = get_network_info_windows(infacename)
        #print(gateway_ip)
        network = get_network_range(gateway_ip[0], subnet_mask)
        #print(f"{network}\n")

        print("")
        devices = arp_scan_new(network)

        visualize_network_with_colors(devices)
        #visualizing_network(devices)

    elif os_type == 'Linux':
        ip, subnet_mask, gateway_ip = get_network_info_linux(infacename)
        network = get_network_range(gateway_ip[0], subnet_mask)

        devices = arp_scan_new(network)

        visualize_network_with_colors(devices)

    elif os_type == 'Darwin':
        ip, subnet_mask, gateway_ip = get_network_info_mac(infacename)
        print(gateway_ip)
        network = get_network_range(gateway_ip, subnet_mask)

        devices = arp_scan_new(network)

        visualize_network_with_colors(devices)

    else:
        print("Unsupported OS")

    # ip, subnet_mask, gateway_ip = get_network_info(infacename)


if __name__ == '__main__':
    # debug
    infacename = input("Enter the name of the interface: ").strip()
    aethermap(infacename)
