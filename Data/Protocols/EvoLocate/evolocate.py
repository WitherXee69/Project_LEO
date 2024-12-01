import base64
import os
import requests
from terminaltables import SingleTable

script_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(script_dir)
grandparent_dir = os.path.dirname(parent_dir)
key_path = os.path.join(grandparent_dir, "Keys", "Hunter_API.key")
with open(key_path, 'rb') as bytekey:
    key = bytekey.read()

decode_key = base64.b64decode(key)
api_key = decode_key.decode()


def evolocate_all(domain, lname):
    try:
        response = requests.get(
            f"https://api.hunter.io/v2/email-finder?domain={domain}&full_name={lname}&api_key={api_key}")

        response.raise_for_status()
        data = response.json()
        print(data)

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")


def evolocate_dom(domain):
    TABLE_DATA = []
    count = 0
    offcount = 0
    while count < 5:
        try:
            response = requests.get(
                f"https://api.hunter.io/v2/domain-search?domain={domain}&offset={offcount}&api_key={api_key}")

            response.raise_for_status()
            data = response.json()
            emails_list = data['data']['emails']

            if emails_list:
                info = ("Email", "First Name", "Last Name", "Position", "Phone", "Linkedin", "Twitter")
                TABLE_DATA.append(info)
                for email in emails_list:
                    infos = (
                        email['value'], email['first_name'], email['last_name'], email['position'],
                        email['phone_number'],
                        email['linkedin'], email['twitter'])
                    TABLE_DATA.append(infos)
                    TABLE_DATA.append(['', '', ''])

            count = count + 1
            offcount = offcount + 10
            print(offcount)

        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")

    print("\nExtracted Emails:: ")
    table = SingleTable(TABLE_DATA, domain)
    print("\n" + table.table)


if __name__ == '__main__':
    evolocate_dom("slt.lk")
