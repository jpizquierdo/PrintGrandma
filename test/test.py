from escpos.printer import Usb

""" Seiko Epson Corp. Receipt Printer (EPSON TM-T88III) """
p = Usb(idVendor=0x6868,idProduct= 0x0200, usb_args=0)#, 0, profile="TM-T88III")
p.text(txt="Hello World\n")