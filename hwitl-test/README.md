# Hardware in the Loop Testing

This directory contains files to do hardware in the loop testing of the crazyflie firmware.
Your firmware can be run on the target platform as if it was normal flight time but the 
motors wont move and the sensors are fed with simulated data.

## How it works

The crazyflie is flashed with the desired firmware and a general purpose machine is connected the STLink for debugging. The general purspose machine then interfaces with the crazyflie through OpenOCD[1]. Python scripts can simulate flight time by communicating with OpenOCD through the Telnet application layer. 

When communicating with the crazyflie through openOCD high-level symbols of the software are not availalbe (as they would be for example with GDB) and instead the memory registers of the crazyflie platform have to be direactly accessed.

### Changes in the firmware
To trigger the necessary changes you to define the macro HARDWARE\_IN\_THE\_LOOP in file sensors\_bmi088\_bmp388.c and file power\_distribution\_stock.c

For what concerns the sensing: this will introduce the dummy variables 
 * *accelRaw_hitl* mocking *accelRaw*.
 * *gyroRaw_hitl* mocking *gyroRaw*.

The code of the sensor task is also modified so that these mocking variables are used to generate the  *sensorData* variable used by the controller (in place of the ones carrying the actual  measurements).

Instead, regarding the output, it is only needed to cut out the writing to the motors. This is done by avoiding calling the *motorsSetRatio()* function. 

### Retrieving the memory addresses of the motor outputs
We want to intercept the input to the function *motorsSetRatio()*, when it is called in the file power\_distribution\_stock.c . The variables of interest are: *motorPower.m1*, *motorPower.m2*, *motorPower.m3*, and *motorPower.m4*. Their address can be retrieved with GDB using command *p &motorPower.m2*. 

### Retrieving the memory addresses of the sensors

The memory addresses for the *accelRaw_hitl* and *gyroRaw_hitl* variables are found with gdb using the commands (you will need all the three axis):
 * 'p &accelRaw_hitl'
 * 'p &gyroRaw_hitl'

## Step by step instructions

## Content of the directory

 * _write\_imu\_values.py_ is a script that writes values to the *accelRaw_hitl* and *gyroRaw_hitl*. These variables are the raw output of the sensors and are int16 coded in C2.
 * _read\_motoers\_output.py_ is a script that reads the outputs to the motors. The intercepted values are of type int32 but should contain at most a value of 2^16 (value is saturated in the attitude controller). The motors are mapped so that 2^16 should correspond to a vertical thrust of 60 grams.

[1] OpenOCD: http://openocd.org/
