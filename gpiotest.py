import sys, json, websocket, ssl, urllib3
import base64
import hashlib


MICA = "mica-efjyn.local"

GPIO_CONTAINER = "GPIOTest"
ROLE = "admin"
PW = "admin"



def getCredentials(role, passwd):
    role_as_bytes = role.encode()
    passwd_as_bytes = passwd.encode()
    zw = hashlib.sha256( role_as_bytes + base64.b64encode(passwd_as_bytes)).digest()
    return base64.b64encode(zw).decode()

cred = getCredentials(ROLE,PW)

payload = {"jsonrpc":"2.0","id":1,"method":"get_auth_token","params": [cred]}


payload_as_string = json.dumps(payload)

http = urllib3.PoolManager( assert_hostname=False, ca_certs="/META/harting_web.crt")

at = http.urlopen("POST", "https://" + MICA + "/base_service/", body=payload_as_string)

rep_data_str = str(at.data, "utf-8")

ret = json.loads(rep_data_str)

retl = ret["result"][1]

ws_url = "wss://"+MICA+"/"+GPIO_CONTAINER+"/"

wesckt = websocket.create_connection(ws_url,sslopt = {"cert_reqs":ssl.CERT_NONE, "ca_certs":"/META/harting.crt", "check_hostame":False})

call = {"id":1, "method":"login", "params": [ret1]}
weskt.send(json.dumps(call))

print(json.dumps(call))

result_str = wesckt.recv()

print(result_str)

call = {"id":1,"method":"get_pin_states", "params":[0]}

wesckt.send(json.dumps(call))

print(wesckt.recv())