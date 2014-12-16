__author__ = 'Delinquente'
import ctypes
import serial
import time

BASEADRESS = 0x6F3C0000
OFF0 = 0x67FF44
OFF1 = 0x17C
OFF2 = 0x18
OFF3 = 0x1E0
OFF4 = 0x1D4
OFF5 = 0x568

kernel = ctypes.windll.kernel32

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


def mapuj(z,inMin,inMax,outMin,outMax):
    return int((z - inMin)*(outMax-outMin)/(inMax-inMin)+outMin )


def kolor(R,G,B):
    arduino.write(str(R)+' '+str(G)+' '+str(B)+'\n')

def init_gry():
    global gra
    print "Podaj nr. procesu gry:"
    try:
        pid = int(raw_input("PID >"))
        gra = Process(pid)
    except:
        print "Blad otwarcia procesu!"

def init_arduino():
    global arduino
    print ""
    print "-------------------------------"
    print "-ARDUINO-PC FOR GAMES BETA 0.9-"
    print "-------------------------------"
    print ""
    arduino = serial.Serial('COM4', 9600)
    print "Port na pewno otworzony?",
    print arduino.isOpen()
    time.sleep(2)
    print ""
    print arduino.readline()

def start():
    temp = 0
    while True:
        try:
            light = wczytajwartosc(BASEADRESS,(OFF0,OFF1,OFF2,OFF3,OFF4,OFF5))
        except:
            light = 0
        if temp != light:
            light_map = mapuj(light,0,25,0,200)
            kolor(0,0,light_map)
            temp = light
        time.sleep(0.1)

#def start():

#    while True:
#       light_ave=0
#        for i in range(5):
#            light = wczytajwartosc(BASEADRESS,(OFF0,OFF1,OFF2,OFF3,OFF4,OFF5))
#            light_map = mapuj(light,0,32,0,255)
#            light_ave += light_map
#        light_sum = light_ave / 5
#        kolor(0,light_sum,0)

init_gry()
init_arduino()
start()
gra.close()