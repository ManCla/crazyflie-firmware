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

	# motor 1 read
	tn.write(b"mdw 0x40000038\n")
	tmp1 = tn.read_until(b"0x40000038: ") # read interaction with openocd -- not interesting
	tmp2 = tn.read_until(b"\r\n") # read actual memory read
	print("M1 power = %d " % int(tmp2.decode('ascii').split()[0],16), end =",")

	# motor 2 read
	tn.write(b"mdw 0x40000040\n")
	tmp1 = tn.read_until(b"0x40000040: ") # read interaction with openocd -- not interesting
	tmp2 = tn.read_until(b"\r\n") # read actual memory read
	print("M2 power = %d " % int(tmp2.decode('ascii').split()[0],16), end =",")

	# motor 3 read
	tn.write(b"mdw 0x40000034\n")
	tmp1 = tn.read_until(b"0x40000034: ") # read interaction with openocd -- not interesting
	tmp2 = tn.read_until(b"\r\n") # read actual memory read
	print("M3 power = %d " % int(tmp2.decode('ascii').split()[0],16), end =",")

	# motor 4 read
	tn.write(b"mdw 0x40000840\n")
	tmp1 = tn.read_until(b"0x40000840: ") # read interaction with openocd -- not interesting
	tmp2 = tn.read_until(b"\r\n") # read actual memory read
	print("M4 power = %d " % int(tmp2.decode('ascii').split()[0],16))

	# trying to control motor 1 but seems that the variable gets reset very frequently
	# tn.write(b"mww 0x40000038 90 \n") 
	# tn.write(b"mdw 0x40000038\n")
	# tn.msg("a") # just for debugging

	time.sleep(0.001)


tn.close()

'''
addresses of motors (these depend on the firmware version but can be retrived through gdb)
and telnet commands to get their input:
M1 controlled at address: (volatile uint32_t *) 0x40000038 => tn.write(b"mdh 0x40000038 \n")
M2 controlled at address: (volatile uint32_t *) 0x40000040 => tn.write(b"mdh 0x40000040 \n")
M3 controlled at address: (volatile uint32_t *) 0x40000034 => tn.write(b"mdh 0x40000034 \n")
M4 controlled at address: (volatile uint32_t *) 0x40000840 => tn.write(b"mdh 0x40000840 \n")
'''
