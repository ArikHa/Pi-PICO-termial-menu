# Pi-PICO-termial-menu
Raspberry PI Pico contain two cores, one internal LED, two UART and more 
This project explains how to use one of the UART as terminal menu emulator. The main menu led to submenu as files menu, parameters menu and some hardware function tests as sensors menu. The implement of submenu base on recursive function. 
The file menu used to list the Pico files, delete a record file and get the Pico hardware version  
and printed the “main.py” wich running after power on. 
The next menu is used for parameters setting to demonstrate how to add offset to A2D read out. The most important thing is the capability to setting parameters at real time.
The menu based on ASCII character send from Pico to Raspberry pi Mincom terminal emulator, buad rate 57600 bps.
Eatch sub menu run in loop with delay of 0.1 second, and to quit by ESC key. The main menu keep that the recursive cartridge will not be in overflow situation then the software will stuck.
