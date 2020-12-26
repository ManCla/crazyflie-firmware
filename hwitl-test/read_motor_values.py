#telnet host port << END LOGIN:USER:PASS OTHER TELNET COMMANDS quit END 


import telnetlib 
import time

tn = telnetlib.Telnet("localhost", 4444)

tn.set_debuglevel(0)

tn.write(b"\n")
print(tn.read_until(b"Open On-Chip Debugger\n", timeout=0.5).decode('ascii'))

print("~~~ Starting to read ~~~\n")

i = 0
while (1) :

	#read controller actuation signals thrust
	tn.write(b"mdw 0x2000c5f4\n")
	tmp1 = tn.read_until(b"0x2000c5f4: ") # read interaction with openocd -- not interesting
	tmp2 = tn.read_until(b"\r\n") # read actual memory read
	num = int(tmp2.decode('ascii').split()[0],16)
	print("control->thrust = %d " % num, end =",")

	#read controller actuation signals roll
	tn.write(b"mdw 0x2000c5ec\n")
	tmp1 = tn.read_until(b"0x2000c5ec: ") # read interaction with openocd -- not interesting
	tmp2 = tn.read_until(b"\r\n") # read actual memory read
	print("control->roll = %d " % int(tmp2.decode('ascii').split()[0],16), end =",")

	#read controller actuation signals pitch
	tn.write(b"mdw 0x2000c5ee\n")
	tmp1 = tn.read_until(b"0x2000c5ee: ") # read interaction with openocd -- not interesting
	tmp2 = tn.read_until(b"\r\n") # read actual memory read
	print("control->pitch = %d " % int(tmp2.decode('ascii').split()[0],16), end =",")

	#read controller actuation signals yaw
	tn.write(b"mdw 0x2000c5f0\n")
	tmp1 = tn.read_until(b"0x2000c5f0: ") # read interaction with openocd -- not interesting
	tmp2 = tn.read_until(b"\r\n") # read actual memory read
	print("control->yaw = %d " % int(tmp2.decode('ascii').split()[0],16))


	# # motors read
	# tn.write(b"mdw 0x40000038\n")
	# tmp1 = tn.read_until(b"0x40000038: ") # read interaction with openocd -- not interesting
	# tmp2 = tn.read_until(b"\r\n") # read actual memory read
	# print("M1 power = %x " % int(tmp2.decode('ascii').split()[0],16), end =",")

	# tn.write(b"mdw 0x40000040\n")
	# tmp1 = tn.read_until(b"0x40000040: ") # read interaction with openocd -- not interesting
	# tmp2 = tn.read_until(b"\r\n") # read actual memory read
	# print("M2 power = %x " % int(tmp2.decode('ascii').split()[0],16), end =",")

	# tn.write(b"mdw 0x40000034\n")
	# tmp1 = tn.read_until(b"0x40000034: ") # read interaction with openocd -- not interesting
	# tmp2 = tn.read_until(b"\r\n") # read actual memory read
	# print("M3 power = %x " % int(tmp2.decode('ascii').split()[0],16), end =",")

	# tn.write(b"mdw 0x40000840\n")
	# tmp1 = tn.read_until(b"0x40000840: ") # read interaction with openocd -- not interesting
	# tmp2 = tn.read_until(b"\r\n") # read actual memory read
	# print("M4 power = %x " % int(tmp2.decode('ascii').split()[0],16))


	# tn.write(b"mwb 0x40000020 90 \n") #write to some meomry address
	# tn.write(b"mdh 0x40000016 32\n")
	# tn.msg("a") # just for debugging

	# the following two lines are a very dumb way of reading what has been outputted
	# tn.write(b"\n")

	time.sleep(0.1)
	# i=i+1

# tn.write(b"exit\n")
# print(tn.read_all().decode('ascii'))

tn.close()

'''
addresses of motors (these depend on the firmware version but can be retrived through gdb)
and telnet commands to get their input:
M1 controlled at address: (volatile uint32_t *) 0x40000038 => tn.write(b"mdh 0x40000038 \n")
M2 controlled at address: (volatile uint32_t *) 0x40000040 => tn.write(b"mdh 0x40000040 \n")
M3 controlled at address: (volatile uint32_t *) 0x40000034 => tn.write(b"mdh 0x40000034 \n")
M4 controlled at address: (volatile uint32_t *) 0x40000840 => tn.write(b"mdh 0x40000840 \n")
'''
