This is a low-level library for the MX25R512F 512-Kbit CMOS serial flash memory module for use with the Buspirate using SPI bitbanging mode.
Not all functions of the MX25R512F are supported as the Buspirate only has 1 set of I/O pins.
In the fututure extended support will be implemented using the AUX pin as an I/O pin.
Extended support will allow for enhanced functionality such as dual read/write mode.
The functions included are low-level hardware functions and do not perform bounds checking, error checking, etc.
A high level library is forthcoming as well as well as GDK GUI app for flashing and backing up the ROM.
