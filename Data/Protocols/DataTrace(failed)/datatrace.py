import base64
import os
from shodan import Shodan


def datatrace():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(script_dir)
    grandparent_dir = os.path.dirname(parent_dir)
    key_path = os.path.join(grandparent_dir, "Keys", "Shoden_API.key")
    #key_path = "Data\\Keys\\Shoden_API.key"
    with open(key_path, 'rb') as bytekey:
        key = bytekey.read()

    decode_key = base64.b64decode(key)
    api_key = decode_key.decode()
    API = Shodan(api_key)

    API.host("123.231.122.209")


datatrace()
