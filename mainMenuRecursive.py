import uctypes
import ustruct
import binascii
import machine
import utime
import os
import uasyncio
import gc
import filesMenu
import sensorsMenu
import parametersMenu

from machine import UART, Pin
from machine import ADC, Pin
from machine import WDT
'''
A2D_PIN_26 = 26
A2D_PIN_27 = 27
sensor_temp = machine.ADC(4)
conversion_factor = 3.3 / (65535)
'''
uart0 = UART(0, baudrate= 57600, tx=Pin(0), rx=Pin(1))#115200, tx=Pin(0), rx=Pin(1))
ledMode = False
led = Pin(25, Pin.OUT)                     
led.value(0)
menu_retuen_count = 0

def enum(**enums):
    return type('Enum', (), enums)

menuEnum = enum (
    mainMenu = 0x00,
    rp2040Status_temperatue = 0x01,
    rp2040Status_A2D = 0x02,
    rp2040Status_memoey_usage = 0x03,
    main_menu_led_toggle = 0x04,
    main_menu_files_menu = 0x05,
    
)
mainMenuStatus = menuEnum.mainMenu

sub_main_menu_call_count = 0
files_menu_rx_prev = '0'
wdt = WDT(timeout=10000)

def main_menu_display():

    global main_dis_count
    
    uart0.write("\r       main menu\n")
    uart0.write("\r 1. Monitor PICO RS2040 hardware\n")   
    if ledMode == True:
     uart0.write("\r 2. PICO LED TOGGLE ON\n")
    else:
     uart0.write("\r 2. PICO LED TOGGLE OFF\n")   
     
    uart0.write("\r f. Files menu\n")
    uart0.write("\r p. Parameters menu\n")
    uart0.write("\r q. Exit\n")
    uart0.write("\r enter option: ") 
    return(True)


def main_menu_handler():
 global wdt, mainMenuStatus, ledMode
 global menu_retuen_count
 rxData0 = bytes()
 rx_prev = '0'
 rx_ =  '0'
 rxData0 = '0'
 count = 0
 menu_retuen = '0'
  
 while  True:   
    while uart0.any() > 0:

          rxData0 = uart0.read(1)
          count +=1
          if count > 0:
             if rxData0 != b'\xff':
                  rx_ = rxData0.decode('utf-8')
          if rx_ == '0':
                  pass
          elif rx_ == '1' and rx_prev != '1':
                    rx_prev = rx_          
                    menu_retuen = main_menu(sensorsMenu.sensors_menu_display(),sensorsMenu.sensors_menu_handler())
          elif rx_ == '2':
                 if mainMenuStatus == menuEnum.mainMenu or mainMenuStatus == menuEnum.main_menu_led_toggle:
                     mainMenuStatus = menuEnum.main_menu_led_toggle
                     led = Pin(25, Pin.OUT)                     
                     if (ledMode == False):
                         ledMode = True
                         led.value(1)
                     else:
                         ledMode = False
                         led.value(0)
          elif rx_ == 'f':                 
                 if rx_prev != 'f' and mainMenuStatus == menuEnum.mainMenu:
                    rx_prev = rx_
                    menu_retuen = main_menu(filesMenu.files_menu_display(),filesMenu.files_menu_handler())
          elif rx_ == 'p':                 
                 if rx_prev != 'p' and mainMenuStatus == menuEnum.mainMenu:
                    rx_prev = rx_
                    menu_retuen = main_menu(parametersMenu.parameters_menu_display(),parametersMenu.parameters_menu_handler())
          elif rx_ == 'q':
                 if rx_prev != 'q' and mainMenuStatus == menuEnum.mainMenu:
                   rx_prev = rx_
                   menu_retuen = None                  
                   return False
          elif rx_== '\x1B':  #***ESC***#
                 if (rx_prev != '\x1B'):
                   rx_prev = '\x1B'  #ESC
                   mainMenuStatus = menuEnum.mainMenu
                   main_menu_display()
                   uart0.write('\r enter option: '+rx_)
          else:
                   uart0.write('\r enter option: '+rx_)
                   mainMenuStatus = menuEnum.mainMenu
          if menu_retuen == 'EXIT':
                   menu_retuen = '0'
                   menu_retuen_count += 1
                   if menu_retuen_count > 1:
                      return 
          elif mainMenuStatus == menuEnum.main_menu_led_toggle:
                   main_menu_display()
                   #return True
          elif menu_retuen == None:
                   return False
    wdt.feed()      
    utime.sleep(0.1)
    count = 0 
 return True

def main_menu(display, handler):
    x= True
    while x != False:       
     if (display == True): 
       #uart0.write("\r Enter option-------")
       #print("\n Enter option-------")
       x = handler
       if x == None or x == 'ESC':
        return 'ESC'
       elif x == True:
        return 'EXIT'
    return 'UP MENU'
   
def mainMenuThread():
    global menu_retuen_count
    print('mainMenu')
    while True:
      main_menu(main_menu_display(),main_menu_handler())
      menu_retuen_count -= 1      
      if menu_retuen_count <= 0:
         print('main_menu exit')
         return

mainMenuThread()