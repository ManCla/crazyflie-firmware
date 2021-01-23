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

'''
this function formats an acceleration value to the format of the
accelRaw_hitl variable of the crazyflie firmware. 

TODO: the accelScale is not yet accounted for (since it is defined on startup)
TODO : check for overflow after scaling
'''
#def formatAccel(num) : 
#    if num<0 :
#        num = pow(2,17) - pow(2,15) + num # C2 representation ?????
#    return int(num*65536/(2*24))
def formatAccel(num) : 
    num = num * 65536/(2*24)
    if num<0 :
        num = pow(2,17) + num
    return int(num)

'''
this function formats an gyro value to the format of the
gyroRaw_hitl variable of the crazyflie firmware. 

TODO : the gyroBias is not yet accounted for (since it is defined on startup)
TODO : check for overflow after scaling
'''
def formatGyro(num) : 
    #num=num+0.148
    num = num * 65536/(2*2000)
    if num<0 :
        num = (pow(2,17) + num) # C2 (pow(2,17)-1)
    return int(num)

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

'''
the memory addresses for the accelRaw_hitl and gyroRaw_hitl variables
are found with gdb using the command 'p &accelRaw_hitl'


If the variable is masked by some other definition use a breakpoint
to make sure you are in the right scope:
b sensors_bmi088_bmp388.c:300
'''

#value = pow(2,17)-pow(2,15)-1
#value = 10
#value = int(value*65536/(2*24))

value= 123


#write accelRaw_hitl.x data
stringa = format("mwh 0x20008e7a %d \n" % formatAccel(value) )
tn.write(stringa.encode())
tn.read_until(b"\r\n") 

#write accelRaw_hitl.y data
stringa = format("mwh 0x20008e7c %d \n" % formatAccel(value))
tn.write(stringa.encode())
tn.read_until(b"\r\n") 

# #write accelRaw_hitl.z data
stringa = format("mwh 0x20008e7e %d \n" % formatAccel(value))
tn.write(stringa.encode())
tn.read_until(b"\r\n") 

#write gyroRaw_hitl.x data
stringa = format("mwh 0x20009012 %d \n" % formatGyro(value))
print(stringa)
tn.write(stringa.encode())
tn.read_until(b"\r\n") 

#write gyroRaw_hitl.y data
stringa = format("mwh 0x20009014 %d \n" % formatGyro(value))
tn.write(stringa.encode())
tn.read_until(b"\r\n") 

#write gyroRaw_hitl.z data
stringa = format("mwh 0x20009016 %d \n" % formatGyro(value))
tn.write(stringa.encode())
tn.read_until(b"\r\n") 

tn.close()


