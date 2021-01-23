import cfhitl
import time

if __name__ == "__main__":
    cf = cfhitl.cfHITL()
    
    # convention is to have a dictionary with field names that are the same as the 
    # names of the variables in the firmware 
    # TODO: retrieve automatically the addresses form map file

    # motors
    cf.add_mem_addr("motorPower_m1", "0x2000cde4")
    cf.add_mem_addr("motorPower_m2", "0x2000cde8")
    cf.add_mem_addr("motorPower_m3", "0x2000cdec")
    cf.add_mem_addr("motorPower_m4", "0x2000cdf0")
    #accelerometer
    cf.add_mem_addr("accelRaw_hitl_x", "0x20008e7a")
    cf.add_mem_addr("accelRaw_hitl_y", "0x20008e7c")
    cf.add_mem_addr("accelRaw_hitl_z", "0x20008e7e")
    #gyroscope
    cf.add_mem_addr("gyroRaw_hitl_x", "0x20009012")
    cf.add_mem_addr("gyroRaw_hitl_y", "0x20009014")
    cf.add_mem_addr("gyroRaw_hitl_z", "0x20009016")
    #barometer
    cf.add_mem_addr("data_pressure_hitl", "0x2000efa4")

    #print(cf.motors)
    cf.write_imu(1, 2, 3, 4, 5, 6)
    cf.write_pressure(37*pow(2,25))
    cf.close()
    time.sleep(0.1)
