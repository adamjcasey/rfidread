import struct
import time
import sys

infile_path = "/dev/input/event0"
FORMAT = 'llHHI'
EVENT_SIZE = struct.calcsize(FORMAT)
code_to_ascii = {11:0,2:1,3:2,4:3,5:4,6:5,7:6,8:7,9:8,10:9}

# Open the file in binary mode
in_file = open(infile_path, "rb")

event = in_file.read(EVENT_SIZE)
out_str = ''

def rfid_card_read(id):
	print ("RFID: %s" % (id))

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
