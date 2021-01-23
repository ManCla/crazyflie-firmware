import telnetlib 

"""
DESCRIPTION:
Class implementing communication with the cf hardware for hardware
in the loop testing. The communication is handled with the telnet
application layer, that's why it's a super-class. The memory 
addresses of the variables of interest have to be passed with the
add_mem_addr function.

INTERFACE:

USE:

"""

class cfHITL(telnetlib.Telnet):

    """
    Init Function: it established communication with openocd and initializes the
    needed variables.
    """
    def __init__(self):
        super().__init__("localhost", 4444) # init telnet comm
        super().set_debuglevel(0)
        super().write(b"\n")                      # TODO: check if this is needed
        self._addr_book = dict()                  # init dictionary memory addresses

    """
    Function to terminate telnet connection
    """
    def close(self):
        super().close()
    """
    Function to add the memory addresses of the variables in the firmware
    """        
    def add_mem_addr(self, identifier: str, addr: str):
        self._addr_book[identifier] = addr

    """
    Function to read from a given memory address
    """
    def read_mem_addr(self, addr: str):
        cmd = format("mdw %s \n" % addr)   # build openocd command
        super().write(cmd.encode())        # send command to openocd
        reply = format("%s: " % addr)      # expected reply from openocd
        super().read_until(reply.encode()) # flush openocd echo
        read = super().read_until(b"\r\n") # actual memory read and function return
        return int(read.decode('ascii').split()[0],16) # extract and convert to int

    """
    Function to write to a given memory address
    half word (2 bytes) is written unless the optional argument is given
    to write to a full work (4 bytes) 
    """
    def write_mem_addr(self, addr: str, message: str, write_full_word=False):
        cmd = "mww " if write_full_word else "mwh "
        stringa = cmd + addr + ' ' + message + " \n" # build openocd command
        print(stringa)
        super().write(stringa.encode())                 # send command
        super().read_until(b"\r\n")                     # no echo output to handle

    """
    Function that reads all of the motor values and returns them
    """
    def motors(self):
        m1 = self.read_mem_addr(self._addr_book['motorPower_m1'])
        m2 = self.read_mem_addr(self._addr_book['motorPower_m2'])
        m3 = self.read_mem_addr(self._addr_book['motorPower_m3'])
        m4 = self.read_mem_addr(self._addr_book['motorPower_m4'])
        return [m1, m2, m3, m4]

    """
    Function to write pressure measurements
    TODO: convert to float
    """
    def write_pressure(self, pressure:float):
        self.write_mem_addr(self._addr_book['data_pressure_hitl'], str(pressure),   write_full_word=True)

    """
    Function that writes IMU values to sensordata variables
    values are scaled to Least Significant Bit unit of measure and 
    converted to TwosComplement with auxiliary finctions
    """
    def write_imu(self, ax: float, ay: float, az: float, gx: float, gy: float, gz: float):
        self.write_mem_addr(self._addr_book['accelRaw_hitl_x'], str(self.accelToLSB(ax)))
        self.write_mem_addr(self._addr_book['accelRaw_hitl_y'], str(self.accelToLSB(ay)))
        self.write_mem_addr(self._addr_book['accelRaw_hitl_z'], str(self.accelToLSB(az)))
        self.write_mem_addr(self._addr_book['gyroRaw_hitl_x'], str(self.gyroToLSB(gx)))
        self.write_mem_addr(self._addr_book['gyroRaw_hitl_y'], str(self.gyroToLSB(gy)))
        self.write_mem_addr(self._addr_book['gyroRaw_hitl_z'], str(self.gyroToLSB(gz)))
    
    '''
    this function translates an acceleration value to the format of the
    accelRaw_hitl variable of the crazyflie firmware. 

    TODO: the accelScale is not yet accounted for (since it is defined on startup)
    TODO : check for overflow after scaling
    '''
    def accelToLSB(self, num) : 
        num = num * 65536/(2*24)   # scale to LSB
        if num<0 :
            num = pow(2,17) + num  # C2
        return int(num)

    '''
    this function formats an gyro value to the format of the
    gyroRaw_hitl variable of the crazyflie firmware. 

    TODO : the gyroBias is not yet accounted for (since it is defined on startup)
    TODO : check for overflow after scaling
    '''
    def gyroToLSB(self, num) : 
        num = num * 65536/(2*2000)  # scale to LSB
        if num<0 :
            num = (pow(2,17) + num) # C2 
        return int(num)



