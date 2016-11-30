from pyBusPirateLite.SPI import *

BB = BBIO_base()
BB.connect()
BB.enter()

spi = SPI()
spi.pins = PIN_POWER | PIN_CS
spi.config = CFG_PUSH_PULL | CFG_CLK_EDGE
spi.speed = '30kHz'

# Read Byte. Address Passed is MSB First

def Read(address, rx_bytes):
    data = bytes()
    spi.cs = True
    spi.transfer([0x03, address[0], address[1], address[2]]) 
    for i in range(rx_bytes) :
        data += spi.transfer([0xFF])
    spi.cs = False 
    return data

# Fast Read.

def Fast_Read(address, rx_bytes):
    data = bytes()
    spi.cs = True
    spi.transfer([0x0B, address[0], address[1], address[2], 0xFF])
    for i in range(rx_bytes) :
        data += spi.transfer([0xFF])
    spi.cs = False
    return data

# Double Transfer Rate Read. (Unsupported)

def X2READ(): 
    pass

# Dual Rate Read. (Unsupported)

def DREAD(): 
    pass

# Quad Transfer Rate Read. (Unsupported)

def X4READ(): 
    pass

# Quad Rate Read. (Unsupported)

def QREAD(): 
    pass

# Page Program/Write.

def PP(Address, data):
    spi.cs = True
    spi.transfer([0x02, Address[0], Address[1], Address[2]])
    for i in range(0,len(data)):
        spi.transfer([data[i]])
    spi.cs = False

# Quad Transfer Page Program. (Unsupported)

def X4PP():
    pass

# Sector Erase

def Sector_Erase(Address): 
    spi.cs = True
    spi.transfer([0x20, Address[0] , Address[1], Address[2]]) 
    spi.cs = False

# 32-Byte Block Erase

def Block_Erase_32(Address):
    spi.cs = True
    spi.transfer([0x52, Address[0], Address[1], Address[2]])
    spi.cs = False

# 64-Byte Block Erase

def Block_Erase_64(Address):
    spi.cs = True
    spi.transfer([0xD8, Address[0], Address[1], Address[2]])
    spi.cs = False

# Chip Erase

def Chip_Erase():
    spi.cs = True
    spi.transfer([0x60])
    spi.cs = False

# Read JEDEC SFDP Data

def RDSFDP(Address,RX_Bytes):
    data = bytes()
    spi.cs = True
    spi.transfer([0x5a, Address[0], Address[1], Address[2], 0xff])
    for i in range(0, RX_Bytes):
        data += spi.transfer([0xff])
    spi.cs = False
    return data

# Set Write Enable Latch

def WREN():
    spi.cs = True
    spi.transfer([0x06])
    spi.cs = False

# Disable Writing

def WRDI():
    spi.cs = True
    spi.transfer([0x04])
    spi.cs = False

# Read Status Register
    
def RDSR():
    #data = bytes()
    spi.cs = True
    data = spi.transfer([0x05, 0xFF])
    spi.cs = False
    return data[1:]

# Read Configuration Register

def RDCR():
    data = bytes()
    spi.cs = True
    data += spi.transfer([0x15, 0xFF,0xFF]) 
    spi.cs = False
    return data[1:]

# Write Status Register

def WRSR(SR_IN):
    spi.cs = True
    spi.transfer([0x01, SR_IN[0], SR_IN[1], SR_IN[2]]) 
    spi.cs = False

# Suspend Program/Erase

def Suspend():
    spi.cs = True
    spi.transfer([0x75])
    spi.cs = False

# Resumes Program/Erase

def Resume(): 
    spi.cs = True
    spi.transfer([0x7A])
    spi.cs = False
    
# Deep Power Down Mode

def DP(): 
    pass
    
# Deep Power Down Mode Release. (Unsupported)
    
def DP_Release(): 
    pass

# Enable Burst Read And Set Depth
    
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

# Read Device ID

def RDID():
    data = bytes()
    spi.cs = True
    data += spi.transfer([0x9F, 0XFF, 0xFF, 0xFF]) 
    spi.cs = False
    return data[1:4] #data[1] = Manufacturers ID = 0xC2, data[2] = Memory Type = 0x28 , data[3] = Data Density = 0x10 = 16-Bytes

# Read Electronic Signature

def RES():
    data = bytes()
    spi.cs = True 
    data += spi.transfer([0xAB, 0xFF, 0xFF, 0xFF, 0xFF]) 
    spi.cs = False
    return data[4:]

# Read Electronic Manufacturer ID & Device ID

def REMS(address):
    data = bytes()
    spi.cs = True
    spi.transfer([0x90, 0xFF, 0xFF])
    data += spi.transfer([address, 0xFF,0xFF]) 
    spi.cs = False 
    return data[1:] # If Address = 0x00 Manufacturer ID Is Read First, If Address = 0x01 Device ID Is Read First

# Enter Secure One Time Programmable Mode
    
def ENSO():
    spi.cs = True
    spi.transfer([0xB1]) 
    spi.cs = False

# Exit Secure One Time Programmable Mode

def EXSO():
    spi.cs = True
    spi.transfer([0XC1]) 
    spi.cs = False

# Read Security Register

def RDSCUR():
    spi.cs = True
    Regs = spi.transfer([0X2B, 0xFF]) 
    spi.cs = False
    return Regs[1]

#!Warning The WRSCUR() will permanently lock the secure 8k-bit onetime programmable area if used 

def WRSCUR(): # Write To Security Register
    spi.cs = True
    spi.transfer([0x2F])
    spi.cs = False

# NO-OP

def NOP(): 
    spi.cs = True
    spi.transfer([0x00])
    spi.cs = False

# Reset Enable

def RSTEN(): 
    spi.cs = True
    spi.transfer([0x66])
    spi.cs = False
    
# Reset Memory

def RST(): 
    spi.cs = True
    spi.transfer([0x99])
    spi.cs = False

# Release From Read Enhance Mode

def Release(): 
    spi.cs = True
    spi.transfer([0xFF])
    spi.cs = False

# Configure Status Register

def Config_Reg(Status_Reg, Config_Reg0, Config_Reg1): 
    Config = [bytes()]
    Config[0] = Status_Reg
    Config[1] = Config_Reg0
    Config[2] = Config_Reg1
    return Config

# Enable Enhanced Mode. (Unsupported)
    
def Enhance_Mode():
    pass

# Reset Enhanced Mode. (Unsupported)

def Enhance_Mode_Reset():
    pass

class BURST_DEPTH():
    X8 = 0x00
    X16 = 0x01
    X32 = 0x02
    X64 = 0x03
    
class STATUS_REG():
    SRWD = 0b10000000 # Status Register Write Protect(0 = Status Register Write Enable, 1 = Status Register Write Disable)
    QE = 0b01000000 # Quad Enable (0 = Not Quad Enable, 1 = Quad Enable)
    BP3 = 0b00100000 # Block 3 Protect
    BP2 = 0b00010000 # Block 2 Protect
    BP1 = 0b00001000 # Block 1 Protect
    BP0 = 0b00000100 # Block 0 Protect
    WEL = 0b00000010 # Write Enable Latch (0 = Write Disable, 1 = Write Enable)
    WIP = 0b00000001 # Write In Progress (0 = Not Writing, 1 = Writing)

class CONFIG_REG0():
    TB = 0b00001000 # Top/Bottom Protect Bit Addressing((Default = 0); 0 = Top To Bottom, 1 = Bottom To Top)
    
class CONFIG_REG1():
    LH = 0b00000010 # L/H Switch((Default = 0); 0 = Ultra Low Power Mode, 1 = High Performance Mode)
    
