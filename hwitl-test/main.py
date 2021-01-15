import cfhitl
import time

if __name__ == "__main__":
    cf = cfhitl.cfHITL()
    
    # convention is to have a dictionary with field names that are the same as the 
    # names of the variables in the firmware 
    cf.add_mem_addr("motorPower_m1", "0x2000cde4")
    cf.add_mem_addr("motorPower_m2", "0x2000cde8")
    cf.add_mem_addr("motorPower_m3", "0x2000cdec")
    cf.add_mem_addr("motorPower_m4", "0x2000cdf0")

    while (1) :
        tmp = cf.motors()
        print(tmp)
        time.sleep(0.1)
