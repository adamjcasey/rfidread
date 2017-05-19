import struct
import MySQLdb
import sys, json, websocket, ssl, urllib3
import base64

# Constants
infile_path = "/dev/input/event0"
FORMAT = 'llHHI'
EVENT_SIZE = struct.calcsize(FORMAT)
code_to_ascii = {11:0,2:1,3:2,4:3,5:4,6:5,7:6,8:7,9:8,10:9}
DB_SERVER = "192.168.137.1"
DB_USER = "root"
DB_PASS = "root"
DB_NAME = "rfidemo"
MICA = "192.168.137.100"
GPIO_CONTAINER = "GPIODemo"
ROLE = "admin"
PW = "admin"

# Open the file in binary mode
in_file = open(infile_path, "rb")

event = in_file.read(EVENT_SIZE)
out_str = ''

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

    db.close()


###------------------------------------------------------------------------ 
while event:
    (tv_sec,tv_usec, type, code, value) = struct.unpack(FORMAT, event)
    if type == 1 and value == 1:
        if code <= 11:
            out_str += str(code_to_ascii[code])
        else:
            rfid_card_read(out_str)
            out_str = ''
    
    event = in_file.read(EVENT_SIZE)

in_file.close()

