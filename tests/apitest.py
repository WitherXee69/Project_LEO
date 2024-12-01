import base64

apikey = "9226b86f1aa00966b74d1fcde3263ddef0b27694"

bytekey = apikey.encode()

api = open("Hunter_API.key", 'wb')
api.write(base64.b64encode(bytekey))

api.close()
