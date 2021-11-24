def enum(**enums):
    return type('Enum', (), enums)

menuEnum = enum (
    mainMenu = 0x00,
    rp2040Status_temperatue = 0x01,
    rp2040Status_A2D = 0x02,
    rp2040Status_memoey_usage = 0x03,
    main_menu_led_toggle = 0x04,
    main_menu_files_menu = 0x05,
    parmetersSet = 0x06,
    main_menu_led_toggle = 07,
    
)

mainMenuStatus = menuEnum.mainMenu


'''
for c in range(7):#len(menuEnum)):
    
    if mainMenuStatus == menuEnum.mainMenu:
        print('mainMenu')
    elif mainMenuStatus == menuEnum.rp2040Status_temperatue:
        print('rp2040Status_temperatue')
    elif mainMenuStatus == menuEnum.rp2040Status_A2D:
        print('rp2040Status_A2D')
    elif mainMenuStatus == menuEnum.rp2040Status_memoey_usage:
        print('rp2040Status_memoey_usage')
    elif mainMenuStatus == menuEnum.main_menu_led_toggle:
        print('main_menu_led_toggle')
    elif mainMenuStatus == menuEnum.main_menu_files_menu:
        print('main_menu_files_menu')
    elif mainMenuStatus == menuEnum.parmetersSet:
        print('parmetersSet')
    elif mainMenuStatus == menuEnum.main_menu_led_toggle:
        print('main_menu_led_toggle')
    mainMenuStatus += 1    
 '''  