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
    Function to add the memory addresses of the variables in the firmware
    """        
    def add_mem_addr(self, identifier: str, addr: str):
        self._addr_book[identifier] = addr

    """
    Function to read from a given memory address
    """
    def read_mem_addr(self, addr: str):
        cmd = format("mdw %s \n" % addr)   # build command openocd command
        super().write(cmd.encode())        # send command to openocd
        reply = format("%s: " % addr)      # expected reply from openocd
        super().read_until(reply.encode()) # flush openocd echo
        read = super().read_until(b"\r\n") # actual memory read and function return
        return int(read.decode('ascii').split()[0],16) # extract and convert to int

    """
    """
    def write_mem_addr(self, addr: str):
        pass

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
    """
    def write(self, identifier: str):
        pass

    """
    
    def fname(self) -> ReturnClass:
        pass
    """

