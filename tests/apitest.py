import base64

apikey = ""

bytekey = apikey.encode()

api = open("Hunter_API.key", 'wb')
api.write(base64.b64encode(bytekey))

api.close()

