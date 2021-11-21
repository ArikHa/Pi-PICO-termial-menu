# Pi-PICO-termial-menu
Raspberry PI Pico contain two cores, one internal LED, two UART and more 
This project explains how to use one of the UART as terminal menu. The main menu led to submenu as file menu, parameters menu and some hardware function tests as sensors menu. The implement of submenu base on recursive function. 
The file menu used to list the Pico files, delete a record file and get the Pico hardware version  
and printed the “main.py”. 
The next menu is for parameters setting to demonstrate how to add offset to A2D read out.
The menu based on ASCII character sent from Pico to Raspberry pi Mincom terminal emulator, buad rate 57600 bps.
