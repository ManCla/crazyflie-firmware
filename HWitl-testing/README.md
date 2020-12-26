# Hardware in the Loop Testing

This directory contains files to do hardware in the loop testing of the crazyflie firmware.
Your firmware can be run on the target platform as if it was normal flight time but the 
motors wont move and the sensors are fed with simulated data.

## How it works

The crazyflie is flashed with the desired firmware and a general purpose machine is connected
the STLink for debugging. The general purspose machine then interfaces with the crazyflie
through OpenOCD[1]. Python scripts can simulate flight time by communicating with OpenOCD
through the Telnet application layer. 

When communicating with the crazyflie through openOCD high-level symbols of the software are
not availalbe (as they would be for example with GDB) and instead the memory registers of the
crazyflie platform have to be direactly accessed.

### Retrieving the memory addresses of the motor outputs

When running GDB the content of variables can be polled with the command *p*.
Specifically to read the motor commands you need the addresses of the following variables
(note that the PWM of motors 1,2,3 is controlled with the same timer while motor 4 uses a
different one):

> p &CONN_M1.tim->CCR2 \
> p &CONN_M1.tim->CCR4 \
> p &CONN_M1.tim->CCR1 \
> p &CONN_M4.tim->CCR4 \

### Retrieving the memory addresses of the sensors

## Step by step instructions

## Content of the directory

Currently in this directory there are two scripts, one for reading sensors data and 
another one to read motor output.


[1] OpenOCD: http://openocd.org/
