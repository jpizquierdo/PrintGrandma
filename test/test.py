from escpos.printer import Usb

""" printing for my 57mm chinese printer, the profile that works is sunmi-V2 """
p = Usb(idVendor=0x6868, idProduct=0x0200, usb_args=0, profile="Sunmi-V2")

p.image("Joel.jpeg")
p.qr("holiiii")
p.text(txt="Hello World\n")
p.text(txt="\n\n\n")
