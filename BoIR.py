__author__ = 'Delinquente'

#Import libraries

import ctypes
import serial
import time


#Adress
BASEADRESS = 0xDA0000
OFF0 = 0x2246B4
OFF1 = 0x3DC
OFF2 = 0x38
OFF3 = 0x7B0
OFF4 = 0x740
OFF5 = 0x114


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
        try:
            tmp = hex(ord(gra.read((newadr+i),1)))[2:4]
        except:
           print 'koczkodan'
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
        #TODO Shortcut to working programme....
        print ord(gra.read(0x140CFEDC,1))
        time.sleep(1)


init_gry()
start()
gra.close()