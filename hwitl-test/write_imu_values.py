#telnet host port << END LOGIN:USER:PASS OTHER TELNET COMMANDS quit END 


import telnetlib 
import time


#################### HELPER FUNC ####################
'''
the translationfromC2 function translates a int16 in C2 in its actual value
i.e. large values become negative
'''
def translationfromC2(num) : 
	if num<(pow(2,15)-1) : # if smaller than largest positive number poissible
		return num
	else : # negative number
		return num - pow(2,16)

'''
the translationtoC2 function translates a general integer to a int16 in C2 
it assumes that the number will fit (i.e. -2^15<num<2^15-1)
'''
def translationtoC2(num) : 
	if num>0 :
		return num
	else :
		return pow(2,16)-num


################## END HELPER FUNC ##################

tn = telnetlib.Telnet("localhost", 4444)

tn.set_debuglevel(0)

tn.write(b"\n")
print(tn.read_until(b"Open On-Chip Debugger\n", timeout=0.5).decode('ascii'))

print("~~~ Starting to write ~~~\n")

''' 
sensor data in accelRaw and gyroRaw are int16 written in C2
for this reason they are to be read with mdh 
(memory dump halfword - halfword is 16bit)
'''

value = 0

while (1) :

	#write accelRaw.x data
	value = (1*value)
	stringa = format("mww 0x2000c810 %d \n" % value)
	tn.write(stringa.encode())
	tmp = tn.read_until(b"\r\n") 
	# print(tmp)

	# #write accelRaw.y data
	# tn.write(b"mwh 0x20008fde \n")
	# tmp1 = tn.read_until(b"0x20008fde: ") # read interaction with openocd -- not interesting
	# tmp2 = tn.read_until(b"\r\n") # read actual memory read
	# print("accelRaw.y = %d " % translationfromC2(int(tmp2.decode('ascii').replace(" ", "").split()[0],16)), end =",")

	# #write accelRaw.z data
	# tn.write(b"mwh 0x20008fe0 \n")
	# tmp1 = tn.read_until(b"0x20008fe0: ") # read interaction with openocd -- not interesting
	# tmp2 = tn.read_until(b"\r\n") # read actual memory read
	# print("accelRaw.z = %d " % translationfromC2(int(tmp2.decode('ascii').replace(" ", "").split()[0],16)))

	time.sleep(0.00001)

tn.close()


