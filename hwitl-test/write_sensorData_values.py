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

'''
'''
the memory addresses for the accelRaw and gyroRaw variables
are found with a breakpoint in the sensorsTask function 
-- i.e. in gdb insert the command 'b sensors_bmi088_bmp388.c:289' --
and then ask for 'p &accelRaw'. Otherwise the variable 
is probably being masked by some other definition that is not being used
'''

value = 0

while (1) :

	#write sensorData.acc.x data
	## THOSE ARE FLOAT SO YOU NEED TO WRITE IN TWO CONSECUTIVE PAIRS OF BYTES
	stringa = format("mwh 0x20009638 %d \n" % 56)
	tn.write(stringa.encode())
	tn.read_until(b"\r\n") 
	stringa = format("mwh 0x2000963a %d \n" % 1000000)
	tn.write(stringa.encode())
	tn.read_until(b"\r\n") 

	#write sensorData.acc.y data
	stringa = format("mww 0x2000963c %d \n" % value)
	tn.write(stringa.encode())
	tn.read_until(b"\r\n") 

	# #write sensorData.acc.z data
	stringa = format("mww 0x20009640 %d \n" % value)
	tn.write(stringa.encode())
	tn.read_until(b"\r\n") 

	#write sensorData.gyro.x data
	stringa = format("mww 0x2000916c %d \n" % value)
	tn.write(stringa.encode())
	tn.read_until(b"\r\n") 

	#write sensorData.gyro.y data
	stringa = format("mww 0x20009648 %d \n" % value)
	tn.write(stringa.encode())
	tn.read_until(b"\r\n") 

	# #write sensorData.gyro.z data
	stringa = format("mww 0x2000964c %d \n" % value)
	tn.write(stringa.encode())
	tn.read_until(b"\r\n") 

	time.sleep(0.00001)

tn.close()


