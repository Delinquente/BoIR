__author__ = 'Delinquente'

#Import libraries

import ctypes
import serial
import time


#Adress
#BASEADRESS = 0xDA0000
OFF0 = 0x2246B4
OFF1 = 0x114
OFF2 = 0x740
OFF3 = 0x7B0
OFF4 = 0x38
OFF5 = 0x3DC


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


def init_arduino():
    global arduino
    print ""
    print "-------------------------------"
    print "-ARDUINO-PC FOR GAMES BETA 0.9-"
    print "-------------------------------"
    print ""
    arduino = serial.Serial('COM3', 9600)
    print "Port na pewno otworzony?",
    print arduino.isOpen()
    time.sleep(2)
    print ""
    print arduino.readline()


def init_gry():
    global gra
    global BASEADRESS
    print "Podaj nr. procesu gry:"
    try:
        pid = int(raw_input("PID >"))
        gra = Process(pid)
        BASEADRESS = int(raw_input("BASEADRESS >"),16)
    except:
        print "Blad otwarcia procesu!"


def start():
    while True:
        #TODO SEND DATA TO ARDUINO
        bombs=28
        templife=8
        keys=20
        gold=32
        energy=376
        moc=158
        arduino.write(
        'H:' + str(wczytajwartosc(BASEADRESS,(OFF0,OFF1,OFF2,OFF3,OFF4,OFF5))) + ' '
        'B:' + str(wczytajwartosc(BASEADRESS,(OFF0,OFF1,OFF2,OFF3,OFF4,OFF5+bombs))) + ' '
        'T:' + str(wczytajwartosc(BASEADRESS,(OFF0,OFF1,OFF2,OFF3,OFF4,OFF5+templife))) + ' '
        'K:' + str(wczytajwartosc(BASEADRESS,(OFF0,OFF1,OFF2,OFF3,OFF4,OFF5+keys))) + ' '
        'G:' + str(wczytajwartosc(BASEADRESS,(OFF0,OFF1,OFF2,OFF3,OFF4,OFF5+gold))) + ' '
        )
        #print 'BOMBS: ' + str(wczytajwartosc(BASEADRESS,(OFF0,OFF1,OFF2,OFF3,OFF4,OFF5+bombs)))
        #print 'Temporart Life: ' + str(wczytajwartosc(BASEADRESS,(OFF0,OFF1,OFF2,OFF3,OFF4,OFF5+templife)))
        #print 'Keys: ' + str(wczytajwartosc(BASEADRESS,(OFF0,OFF1,OFF2,OFF3,OFF4,OFF5+keys)))
        #print 'Gold: ' + str(wczytajwartosc(BASEADRESS,(OFF0,OFF1,OFF2,OFF3,OFF4,OFF5+gold)))
        #print 'Energy: ' + str(wczytajwartosc(BASEADRESS,(OFF0,OFF1,OFF2,OFF3,OFF4,OFF5+energy)))
        #print 'Moc: ' + str(wczytajwartosc(BASEADRESS,(OFF0,OFF1,OFF2,OFF3,OFF4,OFF5+moc)))

        time.sleep(1)

init_arduino()
init_gry()
start()
gra.close()