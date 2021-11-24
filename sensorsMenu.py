import uctypes
import ustruct
import binascii
import machine
import utime
import os
import uasyncio
import gc
import filesMenu
import menuEnum

from machine import UART, Pin
from machine import ADC, Pin
from machine import WDT

A2D_PIN_26 = 26
A2D_PIN_27 = 27
sensor_temp = machine.ADC(4)
conversion_factor = 3.3 / (65535)
uart0 = UART(0, baudrate= 57600, tx=Pin(0), rx=Pin(1))#115200, tx=Pin(0), rx=Pin(1))
ledMode = False
led = Pin(25, Pin.OUT)                     
led.value(0)
menu_retuen_count = 0

mainMenuStatus = menuEnum.menuEnum.mainMenu

sub_main_menu_call_count = 0
files_menu_rx_prev = '0'


wdt = WDT(timeout=10000)
def rp200Status(dataloger):
    global mainMenuStatus
    photoPIN_26 = 26
    photoPIN_27 = 27
    gc.collect()
    F = gc.mem_free()
    A = gc.mem_alloc()
    T = F+A
    P = '{0:.2f}%'.format(F/T*100)
    reading = sensor_temp.read_u16() * conversion_factor
    temp = 27 - (reading -0.706)/(0.001721)     
    
    v = readA2D(A2D_PIN_26)
    h = readA2D(A2D_PIN_27)
    
    if mainMenuStatus == menuEnum.menuEnum.rp2040Status_temperatue:
     uart0.write("\r  CPU tempertaure: "+str(temp) +"   type ESC to quit")
    elif  mainMenuStatus == menuEnum.menuEnum.rp2040Status_A2D:
     uart0.write("\r Ver =: " + str (v) +" Hor = "+ str(h)+"   type ESC to quit")
    elif  mainMenuStatus == menuEnum.menuEnum.rp2040Status_memoey_usage:                            
     uart0.write("\r Total: "+str(T)+" Free: "+str(F)+" used: "+str(P)+"   type ESC to quit")
    dataloger.write('{0:f}\n'.format(temp))
    dataloger.flush() 
    utime.sleep(0.1)

def readA2D(channel):
    photoRes = ADC(Pin(channel))
    A2D = photoRes.read_u16()
    A2D = round(A2D/65535*255,2)
    return A2D
def sensors_menu_display():
    uart0.write("\n\r      Sensors main menu\n")
    uart0.write("\r 1. RS2040 Temperatue\n")
    uart0.write("\r 2. A2D monitor\n")
    uart0.write("\r 3. Memoery usage\n")
    uart0.write("\r ESC. back to main menu\n")
    uart0.write("\r enter option: ") 
    return(True)
def sensors_menu_handler():
    global wdt, files_menu_rx_prev, mainMenuStatus
    dataloger = open("/temperature.txt", "a")
    rx_ =  '0'
    rxData0 = '0'
    while True: 
     utime.sleep(0.1)
     wdt.feed()     
     count = 0
     while uart0.any() > 0:

          rxData0 = uart0.read(1)
          count +=1
          if count > 0:
             if rxData0 != b'\xff':    
                  rx_ = rxData0.decode('utf-8')
             if rx_ == '1' and (files_menu_rx_prev != '1'):
                  mainMenuStatus = menuEnum.menuEnum.rp2040Status_temperatue
                  uart0.write('\n\n')
                  files_menu_rx_prev = '1'
             elif rx_ == '2' and (files_menu_rx_prev != '2'):
                  mainMenuStatus = menuEnum.menuEnum.rp2040Status_A2D
                  uart0.write('\n\n')
                  files_menu_rx_prev = '2'
             elif rx_ == '3' and (files_menu_rx_prev != '3'):
                  mainMenuStatus = menuEnum.menuEnum.rp2040Status_memoey_usage
                  uart0.write('\n\n')
                  files_menu_rx_prev = '3'
                  
             elif rx_== '\x1B' and files_menu_rx_prev != '\x1B':
                  files_menu_rx_prev  = '\x1B'  #ESC
                  if mainMenuStatus == menuEnum.menuEnum.mainMenu:
                      return True
                  else:  
                      mainMenuStatus = menuEnum.menuEnum.mainMenu
                      sensors_menu_display()

             elif rx_== '\x1B' and files_menu_rx_prev  == '\x1B':                 
                  files_menu_rx_prev = '0'
                  return  True 
             else:
                 files_menu_rx_prev = '0'
                 sensors_menu_display()
                 uart0.write('\r enter option: '+rx_)                      
     
     rp200Status(dataloger)
    dataloger.close() 
'''
while True:
    sensors_menu_display()
    sensors_menu_handler()    
'''    