import telnetlib 
import time

tn = telnetlib.Telnet("localhost", 4444)

tn.set_debuglevel(0)

tn.write(b"\n")
print(tn.read_until(b"Open On-Chip Debugger\n", timeout=0.5).decode('ascii'))

print("~~~ Starting to read ~~~\n")

'''
this script reads outputs to the motors. It intercepts the struct motorPower 
with fields {m1,m2,m3,m4} from file power_distribution_stock.c .
'''

while (1) :

	# motorPower.m1 read
	tn.write(b"mdw 0x2000cde4\n")
	tmp1 = tn.read_until(b"0x2000cde4: ") # read interaction with openocd -- not interesting
	tmp2 = tn.read_until(b"\r\n") # read actual memory read
	print("M1 power = %d " % int(tmp2.decode('ascii').split()[0],16), end =",")

	# motorPower.m2 read
	tn.write(b"mdw 0x2000cde8\n")
	tmp1 = tn.read_until(b"0x2000cde8: ") # read interaction with openocd -- not interesting
	tmp2 = tn.read_until(b"\r\n") # read actual memory read
	print("M2 power = %d " % int(tmp2.decode('ascii').split()[0],16), end =",")

	# motorPower.m3
	tn.write(b"mdw 0x2000cdec\n")
	tmp1 = tn.read_until(b"0x2000cdec: ") # read interaction with openocd -- not interesting
	tmp2 = tn.read_until(b"\r\n") # read actual memory read
	print("M3 power = %d " % int(tmp2.decode('ascii').split()[0],16), end =",")

	# motorPower.m4
	tn.write(b"mdw 0x2000cdf0\n")
	tmp1 = tn.read_until(b"0x2000cdf0: ") # read interaction with openocd -- not interesting
	tmp2 = tn.read_until(b"\r\n") # read actual memory read
	print("M4 power = %d " % int(tmp2.decode('ascii').split()[0],16))

	time.sleep(0.1)


tn.close()

