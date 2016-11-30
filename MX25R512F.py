from pyBusPirateLite.SPI import *

BB = BBIO_base()
BB.connect()
BB.enter()

spi = SPI()
spi.pins = PIN_POWER | PIN_CS
spi.config = CFG_PUSH_PULL | CFG_CLK_EDGE
spi.speed = '30kHz'

def Read(address, rx_bytes): # TESTED GOOD
    data = bytes()
    spi.cs = True
    spi.transfer([0x03, address[0], address[1], address[2]]) # Read Byte. Address Passed is MSB First
    for i in range(rx_bytes) :
        data += spi.transfer([0xFF]) #NOTE!!!! With MX25R512 Only the last 2 address bytes are used
    spi.cs = False 
    return data

def Fast_Read(address, rx_bytes): # TESTED GOOD
    data = bytes()
    spi.cs = True
    spi.transfer([0x0B, address[0], address[1], address[2], 0xFF])
    for i in range(rx_bytes) :
        data += spi.transfer([0xFF])
    spi.cs = False
    return data

def X2READ(): # Double Transfer Rate Read
    pass

def DREAD(): # Dual Rate Read
    pass

def X4READ(): # Quad Transfer Rate Read (Not Supported)
    pass

def QREAD(): # Quad Rate Read (Not Supported)
    pass

def PP(Address, data): #TESTED WORKING
    spi.cs = True
    spi.transfer([0x02, Address[0], Address[1], Address[2]]) # Page Program
    for i in range(0,len(data)):
        spi.transfer([data[i]])
    spi.cs = False

def X4PP(): # Not Supported
    pass


def Sector_Erase(Address): #TESTED WORKING
    spi.cs = True
    spi.transfer([0x20, Address[0] , Address[1], Address[2]]) # Erase Sector
    spi.cs = False
    
def Block_Erase_32(Address): #TESTED WORKING
    spi.cs = True
    spi.transfer([0x52, Address[0], Address[1], Address[2]])
    spi.cs = False

def Block_Erase_64(Address): #TESTED WORKING
    spi.cs = True
    spi.transfer([0xD8, Address[0], Address[1], Address[2]])
    spi.cs = False
    
def Chip_Erase(): #TESTED WORKING
    spi.cs = True
    spi.transfer([0x60]) # Erase Entire Chip. BP0-4 Must Be Disabled, Raise Error If Not Disabled
    spi.cs = False

def RDSFDP(Address,RX_Bytes): #TESTED WORKING
    data = bytes()
    spi.cs = True
    spi.transfer([0x5a, Address[0], Address[1], Address[2], 0xff])
    for i in range(0, RX_Bytes):
        data += spi.transfer([0xff]) # Read SFDP Data
    spi.cs = False
    return data

def WREN(): #TESTED GOOD
    spi.cs = True
    spi.transfer([0x06]) # Set Write Enable Latch
    spi.cs = False

def WRDI(): #TESTED GOOD
    spi.cs = True
    spi.transfer([0x04]) # Set Write Disable
    spi.cs = False
    
def RDSR(): #TESTED GOOD
    #data = bytes()
    spi.cs = True
    data = spi.transfer([0x05, 0xFF]) # Read Status Register
    spi.cs = False #Status Register Can Be Checked At Any Time During Any Operation
    return data[1:]

def RDCR(): #TESTED GOOD
    data = bytes()
    spi.cs = True
    data += spi.transfer([0x15, 0xFF,0xFF]) # Read Configuration Register
    spi.cs = False
    return data[1:]

#This function is not finished

def WRSR(SR_IN): #Tested GOOD
    spi.cs = True
    spi.transfer([0x01, SR_IN[0], SR_IN[1], SR_IN[2]]) # Write Status Register
    spi.cs = False # Remember To Set Write Enable Latch(WREN) Before Sending Command


def Suspend(): # Suspend Program/Erase
    spi.cs = True
    spi.transfer([0x75])
    spi.cs = False

def Resume(): # Resumes Program/Erase
    spi.cs = True
    spi.transfer([0x7A])
    spi.cs = False

def DP(): # Deep Power Down Mode
    pass #Can not support this feature with BP alone
    
    
    
def DP_Release(): # Unsupported
    pass

# Make sure all this shit is right

Burst_Depth = {
    'X8' : 0x00,
    'X16' : 0x01,
    'X32' : 0x02,
    'X64' : 0x03}
    
def Burst_Read(BurstDepth, Wrap):
    if Wrap == True :
        spi.cs = True
        spi.transfer([0xC0, 0x00, BurstDepth])
        spi.cs = False
        Wrap = True
        return Wrap
    
    elif Wrap == False :
        spi.cs = True
        spi.transfer([0XC0, 0X1])
        spi.cs = False
        Wrap = False
        return Wrap

def RDID(): #TESTED GOOD
    data = bytes()
    spi.cs = True
    data += spi.transfer([0x9F, 0XFF, 0xFF, 0xFF]) # Read Device ID
    spi.cs = False
    return data[1:4] #data[1] = Manufacturers ID = 0xC2, data[2] = Memory Type = 0x28 , data[3] = Data Density = 0x10=16 probably bytes

def RES(): #TESTED GOOD
    data = bytes()
    spi.cs = True # This Method Of Reading Electronic Signature Is Antiquated Use RDID Instead
    data += spi.transfer([0xAB, 0xFF, 0xFF, 0xFF, 0xFF]) # Read Electronic Signature
    spi.cs = False
    return data[4:]

def REMS(address): #TESTED GOOD
    data = bytes()
    spi.cs = True
    spi.transfer([0x90, 0xFF, 0xFF])
    data += spi.transfer([address, 0xFF,0xFF]) # Read Electronic Manufacturer ID & Device ID
    spi.cs = False # If Address = 0x00 Manufacturer ID Is Read First, If Address = 0x01 Device ID Is Read First
    return data[1:]
    
def ENSO(): #TESTED WORKING
    spi.cs = True
    spi.transfer([0xB1]) # Enter Secure One Time Programmable Mode
    spi.cs = False
    

def EXSO(): #TESTED WORKING
    spi.cs = True
    spi.transfer([0XC1]) # Exit Secure One Time Programmable Mode
    spi.cs = False

def RDSCUR(): #TESTED WORKING
    spi.cs = True
    Regs = spi.transfer([0X2B, 0xFF]) # Read Security Register
    spi.cs = False
    return Regs[1]

#!Warning The WRSCUR() will permanently lock the secure 8k-bit onetime programmable area if used 

#def WRSCUR(): # Write To Security Register
#    spi.cs = True
#    spi.transfer([0x2F])
#    spi.cs = False

def NOP(): # NO-OP Can Be Used For Timing Function 
    spi.cs = True
    spi.transfer([0x00])
    spi.cs = False

def RSTEN(): # Reset Enable
    spi.cs = True
    spi.transfer([0x66])
    spi.cs = False

def RST(): # Reset Memory
    spi.cs = True
    spi.transfer([0x99])
    spi.cs = False

def Release(): # Release From Read Enhance Mode
    spi.cs = True
    spi.transfer([0xFF])
    spi.cs = False

def Config_Reg(Status_Reg, Config_Reg0, Config_Reg1): # Use This With WRSR To Configure Status Register
    Config = [bytes()]
    Config[0] = Status_Reg
    Config[1] = Config_Reg0
    Config[2] = Config_Reg1
    return Config
    
def Enhance_Mode(): # Skips the command cycle and saves a clock cycle for every read. Only available in High Performance Mode
    pass
def Enhance_Mode_Reset():
    pass

#Combine Status And Config Regs Into A Single Class Of Dicts

class STATUS_REG():
    SRWD = 0b10000000 # Status Register Write Protect(0 = Status Register Write Enable, 1 = Status Register Write Disable)
    QE = 0b01000000 # Quad Enable (0 = Not Quad Enable, 1 = Quad Enable)
    BP3 = 0b00100000 # Block Protect
    BP2 = 0b00010000 # Block Protect
    BP1 = 0b00001000 # Block Protect
    BP0 = 0b00000100 # Block Protect
    WEL = 0b00000010 # Write Enable Latch (0 = Write Disable, 1 = Write Enable)
    WIP = 0b00000001 # Write In Progress (0 = Not Writing, 1 = Writing)

class CONFIG_REG0():
    TB = 0b00001000 # Top/Bottom Protect Bit(Default = 0, 0=TOP 1=Bottom)
    
class CONFIG_REG1():
    LH = 0b00000010 # L/H Switch(0 = Ultra Low Power Mode(Default), 1 = High Performance Mode)
    
