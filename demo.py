import struct
import MySQLdb
import sys, json, websocket, ssl, urllib3
import base64
import time

# Constants
infile_path = "/dev/input/event0"
FORMAT = 'llHHI'
EVENT_SIZE = struct.calcsize(FORMAT)
code_to_ascii = {11:0,2:1,3:2,4:3,5:4,6:5,7:6,8:7,9:8,10:9}
DB_SERVER = "192.168.137.1"
DB_USER = "root"
DB_PASS = "root"
DB_NAME = "rfiddemo"
MICA = "192.168.137.100"
GPIO_CONTAINER = "GPIODemo"
ROLE = "admin"
PW = "admin"

# Open the file in binary mode
in_file = open(infile_path, "rb")

event = in_file.read(EVENT_SIZE)
out_str = ''

def showScreen(id):
    http = urllib3.PoolManager()
    url = "http://167.114.126.65/~adamjcas/setuser.php?user=" + id
    print url
    r = http.request('get', url)

def rfid_card_read(id):
    print ("RFID: %s" % (id))

    # Open database connection and get the approval
    db = MySQLdb.connect(DB_SERVER, DB_USER, DB_PASS, DB_NAME)
    cursor = db.cursor()
    sql = "SELECT toolaccess FROM user WHERE tagvalue=%s" % (id)
    try:
        cursor.execute(sql)
        results = cursor.fetchone()
        print "Access = %d" % (results[0])
    except:
        print "Error: unable to fecth data"
        return False

    db.close()

    if (results[0] == 1):
    	return True

    return False

def enableGPIO(enable):
	# Get the authorization token from the base services
	payload = {"jsonrpc":"2.0","id":1,"method":"get_auth_token","params": ["admin", base64.b64encode(PW.encode())]}
	payload_as_string = json.dumps(payload)
	print(payload_as_string)

	http = urllib3.PoolManager( assert_hostname=False, ca_certs="/META/harting_web.crt")
	at = http.urlopen("POST", "https://" + MICA + "/base_service/", body=payload_as_string)
	rep_data_str = str(at.data)
	print(rep_data_str)

	ret = json.loads(rep_data_str)
	retl = ret["result"][1]

	# Connect to the GPIO container
	ws_url = "wss://"+MICA+"/"+GPIO_CONTAINER+"/"
	wesckt = websocket.create_connection(ws_url,sslopt = {"cert_reqs":ssl.CERT_NONE, "ca_certs":"/META/harting.crt", "check_hostame":False})
	call = {"id":1, "method":"login", "params": [retl]}
	wesckt.send(json.dumps(call))
	print(json.dumps(call))
	result_str = wesckt.recv()
	print(result_str)

	# Set or clear the GPIO
	if enable:
		call = {"id":1,"method":"set_state","params":[0,1]}
	else:
		call = {"id":1,"method":"set_state","params":[0,0]}
	wesckt.send(json.dumps(call))
	print(wesckt.recv())


###------------------------------------------------------------------------ 
while event:
    (tv_sec,tv_usec, type, code, value) = struct.unpack(FORMAT, event)
    if type == 1 and value == 1:
        if code <= 11:
            out_str += str(code_to_ascii[code])
        else:
            access = rfid_card_read(out_str)
            out_str = ''
            if (access):
            	print "ACCESS GRANTED"
                showScreen(101)
                time.sleep(5)
                enableGPIO(True)
                showScreen(102)
                time.sleep(3)
                showScreen(1)
            else:
            	print "ACCESS DENIED"
                showScreen(103)
                enableGPIO(False)
                time.sleep(3)
                showScreen(0)
    
    event = in_file.read(EVENT_SIZE)

in_file.close()

