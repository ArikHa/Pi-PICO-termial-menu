import uctypes
import ustruct
import binascii
import machine
import utime
import os
import menuEnum
import uasyncio
import gc
from machine import UART, Pin

from machine import WDT
uart0 = UART(0, baudrate= 57600, tx=Pin(0), rx=Pin(1))#115200, tx=Pin(0), rx=Pin(1))

menu_retuen_count = 0

mainMenuStatus = menuEnum.menuEnum.mainMenu

sub_main_menu_call_count = 0
files_menu_rx_prev = '0'


wdt = WDT(timeout=10000)

def print_Main_py_File():
    try:
     file = open('main.py','R')
     ch = file.read()
     uart0.write('\n\r') 
     for c in range(len(ch)):
      s = ch[c]   
      if s == '\n':
         uart0.write('\n \r')        
      else:   
         uart0.write(s)
     file.close()
     uart0.write('\n type ESC to menu')
    except:
     uart0.write('\n Main.py not exist type ESC to menu')   

def getMemoryUsage():
     fileList=os.listdir()
     uart0.write("\rNo    file Nane \t\t\t\t  size \n")
     totalZise = 0    
     for l in range(len(fileList)):
       file = open(fileList[l], "R")       
       fileCharacters = file.read()
       X =len(fileCharacters)        
       uart0.write('\r' + str(l+1)+'\t'+fileList[l] + '\t\t\t\t ' +str(X)+'\n')       
       totalZise +=X
       file.close()
       utime.sleep(0.001) 
     uart0.write("\r" + str(len(fileList)) + '      files ' + ' \t\t\t\t Total: ' +  str(totalZise)+'\n')
     uart0.write("\r type ESC. back to menu\n")
     uart0.write("\r enter option: ") 
    

def files_menu_display():
    uart0.write("\r      Files main menu\n")
    uart0.write("\r 1. File list\n")
    uart0.write("\r 2. system version\n")
    uart0.write("\r 3. Delete temperature.txt file\n")
    uart0.write("\r 4. Print main.py\n")
    uart0.write("\r ESC. back to main menu\n")
    uart0.write("\r enter option: ") 
    return(True)

def files_menu_handler():
    global wdt, files_menu_rx_prev, mainMenuStatus 
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
             if rx_ == '1' and files_menu_rx_prev != '1':
                    uart0.write('\n\n')
                    getMemoryUsage()
                    files_menu_rx_prev = rx_
                    mainMenuStatus = menuEnum.menuEnum.main_menu_files_menu
             elif rx_ == '2' and files_menu_rx_prev != '2':
                    systemVersion = os.uname()
                    files_menu_rx_prev  = rx_                                        
                    for l in range(len(systemVersion)):
                        if l == 0:
                           uart0.write("\n\r (sysname:"+ systemVersion[l])
                        elif l == 1:
                           uart0.write(" nodename="+ systemVersion[l])
                        elif l == 2:
                           uart0.write(" release="+ systemVersion[l])
                        elif l == 3:
                           uart0.write(" version="+ systemVersion[l])
                        elif l == 4:
                           uart0.write("\n\r machine="+ systemVersion[l]+")\n")
                    uart0.write("\n\r type ESC. back to menu\n")
                    mainMenuStatus = menuEnum.menuEnum.main_menu_files_menu
             elif rx_ == '3' and files_menu_rx_prev != '3':
                    files_menu_rx_prev  = rx_
                    try:
                     file = open("temperature.txt", "r")
                     if file !=  None:
                      file.close() 
                      os.remove("temperature.txt")
                    except:
                      uart0.write("\n\r temperature.txt already delete\n")
                      uart0.write("\n\r type ESC. back to menu\n")
                    mainMenuStatus = menuEnum.menuEnum.main_menu_files_menu
             elif rx_ == '4' and files_menu_rx_prev != '4':
                    files_menu_rx_prev  = rx_
                    print_Main_py_File()    
                    mainMenuStatus = menuEnum.menuEnum.main_menu_files_menu
             elif rx_== '\x1B' and files_menu_rx_prev != '\x1B':
                  files_menu_rx_prev  = '\x1B'  #ESC
                  if mainMenuStatus == menuEnum.menuEnum.mainMenu:
                      return True
                  else:  
                      mainMenuStatus = menuEnum.menuEnum.mainMenu
                      files_menu_display()

             elif rx_== '\x1B' and files_menu_rx_prev  == '\x1B':                 
                  files_menu_rx_prev = '0'
                  return  True 
             else:
                 files_menu_rx_prev = '0'
                 files_menu_display()
                 uart0.write('\r enter option: '+rx_)                      
    #return False

'''
while True:
    files_menu_display()
    files_menu_handler()    
'''  