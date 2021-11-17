''' 
Decode Data from Bluetooth Multimeter

* AOPUTTRIVER AP-90EPD
* HoldPeak HP-90EPD

Credits: https://alexkaltsas.wordpress.com/2013/04/19/python-script-to-read-data-from-va18b-multimeter/

'''

import textwrap

nibble_8 = None
nibble_6 = None
last_line = None

digit = {"1111101": "0",
         "0000101": "1",
         "1011011": "2",
         "0011111": "3",
         "0100111": "4",
         "0111110": "5",
         "1111110": "6",
         "0010101": "7",
         "1111111": "8",
         "0111111": "9",
         "0000000": "",
         "1101000": "L"}


def stream_decode(substr):

    ac = int(substr[0:1])
    dc = int(substr[1:2])
    auto = int(substr[2:3])
    pclink = substr[3:4]
    minus = int(substr[4:5])

    digit1 = substr[5:12]
    dot1 = int(substr[12:13])
    digit2 = substr[13:20]
    dot2 = int(substr[20:21])
    digit3 = substr[21:28]
    dot3 = int(substr[28:29])
    digit4 = substr[29:36]

    micro = int(substr[36:37])
    nano = int(substr[37:38])
    kilo = int(substr[38:39])
    diotst = int(substr[39:40])
    mili = int(substr[40:41])
    percent = int(substr[41:42])
    mega = int(substr[42:43])
    contst = int(substr[43:44])
    cap = int(substr[44:45])
    ohm = int(substr[45:46])
    rel = int(substr[46:47])
    hold = int(substr[47:48])
    amp = int(substr[48:49])
    volts = int(substr[49:50])
    hertz = int(substr[50:51])
    lowbat = int(substr[51:52])
    minm = int(substr[52:53])
    temp = int(substr[53:54])
    # celcius  = int(substr[54:55])
    maxm = int(substr[55:56])

    digit = {"1111101": "0",
             "0000101": "1",
             "1011011": "2",
             "0011111": "3",
             "0100111": "4",
             "0111110": "5",
             "1111110": "6",
             "0010101": "7",
             "1111111": "8",
             "0111111": "9",
             "0000000": "",
             "1101000": "L"}

    value = ("-" if minus else " ") +\
        digit.get(digit1, "") + ("." if dot1 else "") +\
        digit.get(digit2, "") + ("." if dot2 else "") +\
        digit.get(digit3, "") + ("." if dot3 else "") +\
        digit.get(digit4, "")

    # Not all flags are verified!
    flags = ["AC" if ac else "",
            "DC" if dc and not temp else "",
            "Auto" if auto else "",
            "Diode test" if diotst else "",
            "Conti test" if contst else "",
            "Capacity" if cap else "",
            "Rel" if rel else "",
            "Hold" if hold else "",
            #"Min" if minm else "", # ?
            #"Max" if maxm else "", # ?
            "LowBat" if lowbat else ""] #?
    flags = [f for f in flags if f]

    unit  = ("n" if nano else "") +\
            ("u" if micro else "") +\
            ("k" if kilo else "") +\
            ("m" if mili else "") +\
            ("M" if mega else "") +\
            ("%" if percent else "") +\
            ("Ohm" if ohm else "") +\
            ("Amp" if amp else "") +\
            ("Volt" if volts else "") +\
            ("F" if cap else "") +\
            ("Hz" if hertz else "") +\
            ("°C" if temp else "")

    return value, unit, flags

def decode_data(data):
    global nibble_8, nibble_6, last_line
    if len(data) == 8:
        nibble_8 = data
        return
    elif len(data) == 6:
        nibble_6 = data
    else:
        return

    # only the lower 4-bits are relevant
    s = ''.join(['{0:08b}'.format(b)[4:] for b in nibble_8 + nibble_6])

    # show me what changed
    # line = " ".join(textwrap.wrap(s,8))
    # if last_line:
    #   print(line)
    #   print(''.join([c if c!=l else " " for (l,c) in zip(last_line, line)]))
    # else:
    #   print(line)
    # last_line = line

    value, unit, flags = stream_decode(s)
    print(f"{value} {unit} {flags}")

