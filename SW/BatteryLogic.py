##############################################################
# Author: Kevin Brandt                                       #
##############################################################

import serial
import math
import re
from time import sleep
import subprocess

class BatteryLogic():
    def __init__(self):
        self.chargeIcon = "/home/pi/RetroPie/roms/images/chargeBat.png"
        self.batIcon    = "/home/pi/RetroPie/roms/images/bat"
        self.currIcon   = self.batIcon + '100.png'
        self.number     = "/home/pi/RetroPie/roms/images/number"
        self.percent    = "/home/pi/RetroPie/roms/images/percent.png"
        self.currCap    = 0

        self.pngview_path = "/home/pi/src/raspidmx/pngview/pngview"
        self.pngview_call = [self.pngview_path, "-d", "0", "-b", "0x0000", "-n", "-l", "15000", "-y", "0", "-x"]
        self.resolution = 800
        self.iconSize = 32
        self.position = 3

        self.iconProcess = subprocess.Popen(self.pngview_call + [str(int(self.resolution) - self.iconSize * self.position), self.currIcon])
        self.percentProc = subprocess.Popen(self.pngview_call + [str(int(self.resolution) - 15 * 4), self.percent])
        self.percentProcs = [None, None, None]
        return
    
    def parseData(self, data):
        outData = dict()
        outData['charge'] = ''
        outData['cap'] = ''

        charge = re.findall(r',Vin (.*?),', data)
        cap    = re.findall(r',BATCAP (.*?),', data)
        try:
            print(f'charger = {charge[0]}, cap = {cap[0]}')            
            outData['charge'] = charge[0]
            outData['cap'] = cap[0]
        except Exception as e:
            print(e)
        return outData
    
    def updatePercent(self, cap):
        status = True
        try:
            if self.currCap != cap:
                self.currCap = cap
                count = 0
                strcap = str(cap)
                for i in range(len(self.percentProcs)):
                    if self.percentProcs[i] != None:
                        self.percentProcs[i].kill()
                for i in strcap:
                    self.percentProcs[count] = subprocess.Popen(self.pngview_call + [str(int(self.resolution) - 15 * (3 - count)), self.number + f'{i}.png'])
                    count = count + 1
        except Exception as e:
            print(e)
            status = False
        return status
    
    def changeIcon(self, type):
        if self.currIcon != type:
            self.currIcon = type
            self.iconProcess.kill()
            self.iconProcess = subprocess.Popen(self.pngview_call + [str(int(self.resolution) - self.iconSize * self.position), self.currIcon])
        return

    def main(self):
        failCount = 0
        chargerCon = False
        
        # Connect to the Raspberry pi serial port.  
        # TODO: run a check between S0 and AMA0
        ser = serial.Serial("/dev/ttyS0", 9600, timeout=1)
        
        while True:
            # receive entire message
            received_data = ser.read(100)
            sleep(0.03)
        
            # convert to string
            data = received_data.decode("utf-8")
            print(data, end="")

            outdata = self.parseData(data)

            self.updatePercent(outdata['cap'])

            # check charger status
            if outdata['charge'] == 'GOOD':
                failCount = 0
                chargerCon = True
                self.changeIcon(self.chargeIcon)
                print("charger: connected")
            elif outdata['charge'] == 'NG':
                failCount = 0
                chargerCon = False
                
                self.changeIcon(self.batIcon + f"{math.ceil(int(outdata['cap'])/10) * 10}.png")
                print("charger: disconnected")
            else:
                failCount = failCount + 1
                # A single serial failure happens every few seconds due to split data
                if failCount >= 10:
                    psFailure = True
                    chargerCon = False
                    print("Something went wrong")
    
if __name__ == "__main__":
    batLogic = BatteryLogic()
    batLogic.main()