#telnet host port << END LOGIN:USER:PASS OTHER TELNET COMMANDS quit END 


import telnetlib 
import time


#################### HELPER FUNC ####################
'''
the translationC2 function translates a int16 in C2 in its actual value
i.e. large values become negative
'''
def translationC2(num) : 
	if num<(pow(2,15)-1) : # if smaller than largest positive number poissible
		return num
	else : # negative number
		return num - pow(2,16)


################## END HELPER FUNC ##################

tn = telnetlib.Telnet("localhost", 4444)

tn.set_debuglevel(0)

tn.write(b"\n")
print(tn.read_until(b"Open On-Chip Debugger\n", timeout=0.5).decode('ascii'))

print("~~~ Starting to read ~~~\n")

''' 
sensor data in accelRaw and gyroRaw are int16 written in C2
for this reason they are to be read with mdh 
(memory dump halfword - halfword is 16bit)
'''

'''
the memory addresses for the accelRaw and gyroRaw variables
are found with a breakpoint in the sensorsTask function 
-- i.e. in gdb insert the command 'b sensors_bmi088_bmp388.c:289' --
and then ask for 'p &accelRaw'. Otherwise the variable 
is probably being masked by some other definition that is not being used
'''

i = 0
while (1) :

	#read accelRaw.x data
	tn.write(b"mdh 0x20008fdc \n")
	tmp1 = tn.read_until(b"0x20008fdc: ") # read interaction with openocd -- not interesting
	tmp2 = tn.read_until(b"\r\n") # read actual memory read
	print("accelRaw.x = %d " % translationC2(int(tmp2.decode('ascii').replace(" ", "").split()[0],16)), end =",")

	#read accelRaw.y data
	tn.write(b"mdh 0x20008fde \n")
	tmp1 = tn.read_until(b"0x20008fde: ") # read interaction with openocd -- not interesting
	tmp2 = tn.read_until(b"\r\n") # read actual memory read
	print("accelRaw.y = %d " % translationC2(int(tmp2.decode('ascii').replace(" ", "").split()[0],16)), end =",")

	#read accelRaw.z data
	tn.write(b"mdh 0x20008fe0 \n")
	tmp1 = tn.read_until(b"0x20008fe0: ") # read interaction with openocd -- not interesting
	tmp2 = tn.read_until(b"\r\n") # read actual memory read
	print("accelRaw.z = %d " % translationC2(int(tmp2.decode('ascii').replace(" ", "").split()[0],16)))

	#read gyroRaw.x data
	tn.write(b"mdh 0x2000916c \n")
	tmp1 = tn.read_until(b"0x2000916c: ") # read interaction with openocd -- not interesting
	tmp2 = tn.read_until(b"\r\n") # read actual memory read
	print("gyroRaw.x = %d " % translationC2(int(tmp2.decode('ascii').replace(" ", "").split()[0],16)), end =",")

	#read gyroRaw.y data
	tn.write(b"mdh 0x2000916e \n")
	tmp1 = tn.read_until(b"0x2000916e: ") # read interaction with openocd -- not interesting
	tmp2 = tn.read_until(b"\r\n") # read actual memory read
	print("gyroRaw.y = %d " % translationC2(int(tmp2.decode('ascii').replace(" ", "").split()[0],16)), end =",")

	#read gyroRaw.z data
	tn.write(b"mdh 0x20009170 \n")
	tmp1 = tn.read_until(b"0x20009170: ") # read interaction with openocd -- not interesting
	tmp2 = tn.read_until(b"\r\n") # read actual memory read
	print("gyroRaw.z = %d " % translationC2(int(tmp2.decode('ascii').replace(" ", "").split()[0],16)))


	time.sleep(0.1)

tn.close()


