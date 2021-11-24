import uctypes
import ustruct
import binascii
import machine
import utime
import os
import uasyncio
import gc
import sensorsMenu
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
horizonOffset = 0.0
verticalOffset = 0.0

wdt = WDT(timeout=10000)

def getParameterFromLine(string):
	li = list(string.split(" "))
	return li #li[1]



def parameters_menu_display():
    uart0.write("\n\r      parameters main menu\n")
    uart0.write("\r 7. horizonOffset increase \n")
    uart0.write("\r 1. horizonOffset decrease\n")
    uart0.write("\r 8. verticalOffset increase \n")
    uart0.write("\r 2. verticalOffset decrease\n")
    uart0.write("\r s. Save \n")
    uart0.write("\r ESC. back to main menu\n")
    uart0.write("\r enter option: ") 
    return(True)
def saveParametersFile():
     global horizonOffset, verticalOffset
     file = open('parametersOffset.txt','w')
     file.write('horizonOffset ' + str(horizonOffset) + ' \n')
     file.write('verticalOffset '+ str(verticalOffset) + ' \n')
     file.close()
     uart0.write("\n\r parameters saved")
    
def readParametersFile():
    global horizonOffset, verticalOffset
    try:
        count = 0
        file = open('parametersOffset.txt','R')
        for line in file:
            count += 1
            if count == 1:
                horizonOffset = float(getParameterFromLine(line)[1])
                uart0.write("\n\r horizonOffset = " + str(horizonOffset))                
            elif  count == 2:
                verticalOffset = float(getParameterFromLine(line)[1])
                uart0.write("\n\rverticalOffset = " + str(verticalOffset))                
            
        file.close()
        
    except:
     uart0.write('\n parametersOffset.txt not exist create a new\n\r')
     uart0.write('type ESC to menu\n\r')
     file = open('parametersOffset.txt','w')
     file.write('horizonOffset 10.0  \n')
     file.write('verticalOffset 20.0  \n')
     file.close()     
     
def parameters_menu_handler():
    global wdt, files_menu_rx_prev, mainMenuStatus
    global horizonOffset, verticalOffset
    
    
    rx_ =  '0'
    rxData0 = '0'
    while True: 
     utime.sleep(0.2)
     wdt.feed()     
     count = 0
     while uart0.any() > 0:

          rxData0 = uart0.read(1)
          count +=1
          if count > 0:
             if rxData0 != b'\xff':    
                  rx_ = rxData0.decode('utf-8')
             if rx_ == '7':
                  horizonOffset += 0.10
                  files_menu_rx_prev = '7'
                  mainMenuStatus = menuEnum.menuEnum.parmetersSet
             elif rx_ == '1':
                  horizonOffset -= 0.10                  
                  files_menu_rx_prev = '1'
                  mainMenuStatus = menuEnum.menuEnum.parmetersSet
             elif rx_ == '8':
                  verticalOffset += 0.10                  
                  files_menu_rx_prev = '8'
                  mainMenuStatus = menuEnum.menuEnum.parmetersSet
             elif rx_ == '2':
                  verticalOffset -= 0.10                  
                  files_menu_rx_prev = '2'
                  mainMenuStatus = menuEnum.menuEnum.parmetersSet
             elif rx_ == 's' and files_menu_rx_prev != 's':
                  saveParametersFile()
                  files_menu_rx_prev = 's'
                  mainMenuStatus = menuEnum.menuEnum.mainMenu
             elif rx_== '\x1B' and files_menu_rx_prev != '\x1B':
                  files_menu_rx_prev  = '\x1B'  #ESC
                  if mainMenuStatus == menuEnum.menuEnum.mainMenu:
                      return True
                  else:  
                      mainMenuStatus = menuEnum.menuEnum.mainMenu
                      parameters_menu_display()

             elif rx_== '\x1B' and files_menu_rx_prev  == '\x1B':                 
                  files_menu_rx_prev = '0'
                  return  True 
             else:
                 files_menu_rx_prev = '0'
                 mainMenuStatus = menuEnum.menuEnum.mainMenu
                 parameters_menu_display()
                 key= rx_.format('hex') 
                 uart0.write('\r enter option: '+rx_)
                 print("rx_ =",ord(rx_))
     if mainMenuStatus == menuEnum.menuEnum.parmetersSet:
         verticalOffsetStr = '{0:.1f}'.format(verticalOffset)
         horizonOffsetStr = '{0:.1f}'.format(horizonOffset)
         v = sensorsMenu.readA2D(A2D_PIN_26)
         h = sensorsMenu.readA2D(A2D_PIN_27)
         v +=  verticalOffset
         h +=  horizonOffset
         uart0.write('\r ver :' + verticalOffsetStr + '     hor :'+ horizonOffsetStr+'  V :'+str(v)+'  h:'+str(h)+'  ')
     
readParametersFile()
'''
while True:
    
    parameters_menu_display()
    parameters_menu_handler()
'''   