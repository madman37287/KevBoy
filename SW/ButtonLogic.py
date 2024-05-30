##############################################################
# Author: Kevin Brandt                                       #
##############################################################

import sys
import RPi.GPIO as GPIO
#GPIO.setmode(GPIO.BOARD)
import busio
import board
import digitalio
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn
#try:
#    import RPi.GPIO as GPIO
#except ImportError:
#    exit("This library requires the RPi.GPIO module\nInstall with: sudo pip install RPi.GPIO")
try:
    from evdev import uinput, UInput, AbsInfo, ecodes as e
except ImportError:
    exit("This library requires the evdev module\nInstall with: sudo pip install evdev")
#import time
#from time import sleep

# Constants
CENTER_TOLERANCE = 2000
BUTTON_ERROR_RESOLUTION = 3

dUp          = 0
dLeft        = 0
dRight       = 0
dDown        = 0
buttonA      = 0
buttonB      = 0
buttonX      = 0
buttonY      = 0
buttonL      = 0
buttonR      = 0
buttonSel    = 0
buttonStart  = 0
leftAnalogX  = 0
leftAnalogY  = 0
rightAnalogX = 0
rightAnalogY = 0

dUpCnt         = 0
dLeftCnt       = 0
dRightCnt      = 0
dDownCnt       = 0
buttonACnt     = 0
buttonBCnt     = 0
buttonXCnt     = 0
buttonYCnt     = 0
buttonLCnt     = 0
buttonRCnt     = 0
buttonSelCnt   = 0
buttonStartCnt = 0

capabilities = {e.EV_SYN: [], e.EV_KEY: [e.BTN_A, e.BTN_B, e.BTN_X, e.BTN_Y, e.BTN_TOP, e.BTN_TOP2, e.BTN_PINKIE, e.BTN_BASE, e.BTN_SELECT, e.BTN_START, e.BTN_TL, e.BTN_TR], e.EV_ABS: [(e.ABS_X, AbsInfo(0, -32750, 32750, 0, 0, 0)), (e.ABS_Y, AbsInfo(0, -32750, 32750, 0, 0, 0)), (e.ABS_RX, AbsInfo(0, -32750, 32750, 0, 0, 0)), (e.ABS_RY, AbsInfo(0, -32750, 32750, 0, 0, 0))]}
    
try:
    ui = UInput(name="KevBoy Contoller", events=capabilities)
except uinput.UInputError as e:
    sys.stdout.write(e.message)
    sys.stdout.write("Have you tried running as root? sudo {}".format(sys.argv[0]))
    sys.exit(1)
    
    
    

#GPIO.setmode(GPIO.BOARD)

GPIO.setup(23, GPIO.IN, pull_up_down = GPIO.PUD_DOWN) # physical pin 16
GPIO.setup(5, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)  # physical pin 29
GPIO.setup(6, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)  # physical pin 31
GPIO.setup(24, GPIO.IN, pull_up_down = GPIO.PUD_DOWN) # physical pin 18

GPIO.setup(17, GPIO.OUT) # physical pin 11
GPIO.setup(27, GPIO.OUT) # physical pin 13
GPIO.setup(22, GPIO.OUT) # physical pin 15

GPIO.output(17, GPIO.LOW)
GPIO.output(27, GPIO.LOW)
GPIO.output(22, GPIO.LOW)

try:
    # Announce SPI pins in use (because normal GPIO pins can be used too)
    spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)
    cs = digitalio.DigitalInOut(board.D8)

    # Create the object that can read from the ADC
    mcp = MCP.MCP3008(spi, cs)

    # Initialize the channels
    chan1 = AnalogIn(mcp, MCP.P0)
    chan2 = AnalogIn(mcp, MCP.P1)
    chan3 = AnalogIn(mcp, MCP.P2)
    chan4 = AnalogIn(mcp, MCP.P3)
#    startTime = time.time()
#    timeCount = 0
#    print("_____________________________________________________________________________________________________________________________")
#    print("| dUp | Lft | right | dwn | A | B | X | Y | Sel | Start | L | R | Left AnalogY | Left AnalogX | RightAnalogY | RightAnalogX |")
#    print("-----------------------------------------------------------------------------------------------------------------------------")

    while(1):
#        sleep(1)
#        timeCount += 1
#        if timeCount >= 10000:
#            print(time.time() - startTime)
#            startTime = time.time()
#            timeCount = 0

        GPIO.output(17, GPIO.HIGH)
        if GPIO.input(23):
            dUp = 1
            dUpCnt = 0
        elif dUpCnt >= BUTTON_ERROR_RESOLUTION:
            dUp = 0
        else:
            dUpCnt += 1

        if GPIO.input(5):
            dLeft = 1
            dLeftCnt = 0
        elif dLeftCnt >= BUTTON_ERROR_RESOLUTION:
            dLeft = 0
        else:
            dLeftCnt += 1

        if GPIO.input(6):
            dRight = 1
            dRightCnt = 0
        elif dRightCnt >= BUTTON_ERROR_RESOLUTION:
            dRight = 0
        else:
            dRightCnt += 1

        if GPIO.input(24):
            dDown = 1
            dDownCnt = 0
        elif dDownCnt >= BUTTON_ERROR_RESOLUTION:
            dDown = 0
        else:
            dDownCnt += 1

        GPIO.output(17, GPIO.LOW)

        GPIO.output(27, GPIO.HIGH)
        if GPIO.input(23):
            buttonA = 1
            buttonACnt = 0
        elif buttonACnt >= BUTTON_ERROR_RESOLUTION:
            buttonA = 0
        else:
            buttonACnt += 1

        if GPIO.input(5):
            buttonB = 1
            buttonBCnt = 0
        elif buttonBCnt >= BUTTON_ERROR_RESOLUTION:
            buttonB = 0
        else:
            buttonBCnt += 1

        if GPIO.input(6):
            buttonX = 1
            buttonXCnt = 0
        elif buttonXCnt >= BUTTON_ERROR_RESOLUTION:
            buttonX = 0
        else:
            buttonXCnt += 1

        if GPIO.input(24):
            buttonY = 1
            buttonYCnt = 0
        elif buttonYCnt >= BUTTON_ERROR_RESOLUTION:
            buttonY = 0
        else:
            buttonYCnt += 1

        GPIO.output(27, GPIO.LOW)

        GPIO.output(22, GPIO.HIGH)
        if GPIO.input(23):
            buttonSel = 1
            buttonSelCnt = 0
        elif buttonSelCnt >= BUTTON_ERROR_RESOLUTION:
            buttonSel = 0
        else:
            buttonSelCnt += 1

        if GPIO.input(5):
            buttonStart = 1
            buttonStartCnt = 0
        elif buttonStartCnt >= BUTTON_ERROR_RESOLUTION:
            buttonStart = 0
        else:
            buttonStartCnt += 1

        if GPIO.input(6):
            buttonL = 1
            buttonLCnt = 0
        elif buttonLCnt >= BUTTON_ERROR_RESOLUTION:
            buttonL = 0
        else:
            buttonLCnt += 1

        if GPIO.input(24):
            buttonR = 1
            buttonRCnt = 0
        elif buttonRCnt >= BUTTON_ERROR_RESOLUTION:
            buttonR = 0
        else:
            buttonRCnt += 1

        GPIO.output(22, GPIO.LOW)
#        print(str(buttonA) + " " + str(buttonACnt), end = '\r')

#        print("|__" + str(dUp) + "__|__" + str(dLeft) + "__|___" + str(dRight) + "___|__" + str(dDown) + "__|_" + str(buttonA) + "_|_" + str(buttonB) + "_|_" + str(buttonX) + "_|_" + str(buttonY) + "_|__" + str(buttonSel) + "__|___" + str(buttonStart) + "___|_" + str(buttonL) + "_|_" + str(buttonR) + "_|____" + str(leftAnalogY).zfill(6) + "____|____" + str(leftAnalogX).zfill(6) + "____|____" + str(rightAnalogY).zfill(6) + "____|____" + str(rightAnalogX).zfill(6) + "____|", end='\r')

        # Left Analog Values
        leftAnalogY = chan1.value - 32750
        if abs(leftAnalogY) <= CENTER_TOLERANCE:
            leftAnalogY = 0

        leftAnalogX = chan2.value - 32750
        if abs(leftAnalogX) <= CENTER_TOLERANCE:
            leftAnalogX = 0

        # Right Analog Values
        rightAnalogY = chan3.value - 32750
        if abs(rightAnalogY) <= CENTER_TOLERANCE:
            rightAnalogY = 0

        rightAnalogX = chan4.value - 32750
        if abs(rightAnalogX) <= CENTER_TOLERANCE:
            rightAnalogX = 0

        # Write to the controller
        ui.write(e.EV_ABS, e.ABS_X, leftAnalogX)
        ui.write(e.EV_ABS, e.ABS_Y, leftAnalogY)
        ui.write(e.EV_ABS, e.ABS_RX, rightAnalogX)
        ui.write(e.EV_ABS, e.ABS_RY, rightAnalogY)
        ui.write(e.EV_KEY, e.BTN_TOP, dUp)           # DPAD_UP up/down
        ui.write(e.EV_KEY, e.BTN_TOP2, dLeft)        # DPAD_LEFT up/down
        ui.write(e.EV_KEY, e.BTN_PINKIE, dRight)     # DPAD_RIGHT up/down
        ui.write(e.EV_KEY, e.BTN_BASE, dDown)        # DPad Down up/down
        ui.write(e.EV_KEY, e.BTN_A, buttonA)         # South Button up/down
        ui.write(e.EV_KEY, e.BTN_B, buttonB)         # East Button up/down
        ui.write(e.EV_KEY, e.BTN_X, buttonX)         # North Button up/down
        ui.write(e.EV_KEY, e.BTN_Y, buttonY)         # West Button up/down
        ui.write(e.EV_KEY, e.BTN_SELECT, buttonSel)  # Select Button up/down
        ui.write(e.EV_KEY, e.BTN_START, buttonStart) # Start Button up/down
        ui.write(e.EV_KEY, e.BTN_TL, buttonL)        # L1 Button up/down
        ui.write(e.EV_KEY, e.BTN_TR, buttonR)        # R1 Button up/down
        ui.syn()
except Exception as e:
    print(e)
    GPIO.cleanup();
    exit("Something went horribly wrong")      
sys.exit(0)
