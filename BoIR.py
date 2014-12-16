__author__ = 'Delinquente'

#Import libraries

import ctypes
import serial
import time


#Adress
BASEADRESS = 0x61D30000
OFF0 = 0x67FF44
OFF1 = 0x17C
OFF2 = 0x18
OFF3 = 0x1E0
OFF4 = 0x1D4
OFF5 = 0x568
#koczkodanfedrfsdfsdfs

#Init kernel32
kernel = ctypes.windll.kernel32

#clasa procesu
class Process(object):

    def __init__(self, pid):
        self.pid = pid
        self.h = kernel.OpenProcess(0x0018, 0, pid)
    def close(self):
        if (self.h):
            kernel.CloseHandle(self.h)
            self.h = None
    def __del__(self):
        self.close()
    def read(self, addr, size):
        buf = ctypes.create_string_buffer(size)
        bytesread = ctypes.c_size_t()
        kernel.ReadProcessMemory(self.h, addr, buf,ctypes.c_size_t(size),ctypes.addressof(bytesread))
        return buf[:bytesread.value]


def wczytaj(baseadres,off):
    global newadr
    newadr = baseadres + off
    wynik = ''
    for i in range(3,-1,-1):
        tmp = hex(ord(gra.read((newadr+i),1)))[2:4]

        if len(tmp) == 1:
            tmp = '0'+tmp
        wynik += tmp
    return int(wynik,16)

def wczytajwartosc(base,off):
    for ofsety in off:
        base = wczytaj(base,ofsety)
    return base



def init_gry():
    global gra
    print "Podaj nr. procesu gry:"
    try:
        pid = int(raw_input("PID >"))
        gra = Process(pid)
    except:
        print "Blad otwarcia procesu!"



def start():
    while True:
        print wczytajwartosc(BASEADRESS,(OFF0,OFF1,OFF2,OFF3,OFF4,OFF5))
        time.sleep(0.01)


init_gry()
start()
gra.close()