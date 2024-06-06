##############################################################
# Author: Kevin Brandt                                       #
##############################################################
# Note: use command 'sudo crontab -e' to open a text file    #
#       In that text file, add the line:                     #
#       @reboot sudo python3 /home/pi/ButtonLogic5.py        #
#       This line will make it so the script starts at boot  #
##############################################################


import sys
import time
# gpiozero compatible on both rpi4 & 5
from gpiozero import LED, Button, MCP3008

try:
    from evdev import uinput, UInput, AbsInfo, ecodes as e
except ImportError:
    exit("This library requires the evdev module\nInstall with: sudo pip install evdev")

# Constants
CENTER_TOLERANCE = 100 # 10 percent deadzone
BUTTON_ERROR_RESOLUTION = 3 # TODO: this should calculate automatically based on latency and complimented with debounce

# button flag initializations
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

# Error resolution parameter initialization
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

# initializing controller events
capabilities = {e.EV_SYN: [], 
                e.EV_KEY: [e.BTN_A,      # A/east Button (switch inspired design)
                           e.BTN_B,      # B/south Button (switch inspired design)
                           e.BTN_X,      # X/north Button (switch inspired design)
                           e.BTN_Y,      # Y/west Button (switch inspired design)
                           e.BTN_TOP,    # D-PAD up
                           e.BTN_TOP2,   # D-PAD left
                           e.BTN_PINKIE, # D-PAD right
                           e.BTN_BASE,   # D-PAD down
                           e.BTN_SELECT, # Select button
                           e.BTN_START,  # Start Button
                           e.BTN_TL,     # L1 Button
                           e.BTN_TR],    # R1 Button
                e.EV_ABS: [(e.ABS_X, AbsInfo(0, -1000, 1000, 0, 0, 0)),  # Left analog stick X-axis
                           (e.ABS_Y, AbsInfo(0, -1000, 1000, 0, 0, 0)),  # Left analog stick Y-axis
                           (e.ABS_RX, AbsInfo(0, -1000, 1000, 0, 0, 0)), # Right analog stick X-axis
                           (e.ABS_RY, AbsInfo(0, -1000, 1000, 0, 0, 0))] # Right analog stick Y-axis
                           }
    
# setup up the virtual controller (root access required)
try:
    ui = UInput(name="KevBoy Contoller", events=capabilities)
except uinput.UInputError as e:
    sys.stdout.write(e.message)
    sys.stdout.write("Have you tried running as root? sudo {}".format(sys.argv[0]))
    sys.exit(1)

# TODO: implement a bounce time
# initialize input and output pins (Button = input, LED = output)
GPIO23 = Button(23, pull_up=False)
GPIO5  = Button(5,  pull_up=False)
GPIO6  = Button(6,  pull_up=False)
GPIO24 = Button(24, pull_up=False)

GPIO17 = LED(17)
GPIO27 = LED(27)
GPIO22 = LED(22)

# Set up ADC channels
chan1 = MCP3008(channel=0)
chan2 = MCP3008(channel=1)
chan3 = MCP3008(channel=2)
chan4 = MCP3008(channel=3)

try:
    # TODO: Tie printouts to a verbose flag
    #print("_____________________________________________________________________________________________________________________________")
    #print("| dUp | Lft | right | dwn | A | B | X | Y | Sel | Start | L | R | Left AnalogY | Left AnalogX | RightAnalogY | RightAnalogX |")
    #print("-----------------------------------------------------------------------------------------------------------------------------")
    counter = 0
    startTime = time.time()
    while(1):
        # Calculate the latency of the pushbuttons
        # Because reading time costs a large amount of time, this is reduced by only reading once every 10000 cycles
        if counter == 10000:
            latency = (time.time()-startTime)/counter
            startTime = time.time()
            print(f'latency = {latency} sec | frequency = {1/latency} Hz')
            # TODO: tie button error resolution to the latency
            #btnErrTime = 0.0005
            #btnErrResolution = int(btnErrTime/latency)
            counter = 0
        counter = counter + 1

        # This could easily be for-looped, but chose not to for ease of readability and adding new buttons
        # each output is activated once at a time.  While an output rail is active, each input rail checks for voltage.
        # a high voltage read during a time period where a given rail is active means a specific button has been pushed.
        #############################################
        # D-PAD Buttons
        #############################################
        GPIO17.on()
        if GPIO23.is_pressed:
            dUp = 1
            dUpCnt = 0
        elif dUpCnt >= BUTTON_ERROR_RESOLUTION:
            dUp = 0
        else:
            dUpCnt += 1

        if GPIO5.is_pressed:
            dLeft = 1
            dLeftCnt = 0
        elif dLeftCnt >= BUTTON_ERROR_RESOLUTION:
            dLeft = 0
        else:
            dLeftCnt += 1

        if GPIO6.is_pressed:
            dRight = 1
            dRightCnt = 0
        elif dRightCnt >= BUTTON_ERROR_RESOLUTION:
            dRight = 0
        else:
            dRightCnt += 1

        if GPIO24.is_pressed:
            dDown = 1
            dDownCnt = 0
        elif dDownCnt >= BUTTON_ERROR_RESOLUTION:
            dDown = 0
        else:
            dDownCnt += 1

        GPIO17.off()
        #############################################
        
        #############################################
        # ABXY Buttons
        #############################################
        GPIO27.on()
        if GPIO23.is_pressed:
            buttonA = 1
            buttonACnt = 0
        elif buttonACnt >= BUTTON_ERROR_RESOLUTION:
            buttonA = 0
        else:
            buttonACnt += 1

        if GPIO5.is_pressed:
            buttonB = 1
            buttonBCnt = 0
        elif buttonBCnt >= BUTTON_ERROR_RESOLUTION:
            buttonB = 0
        else:
            buttonBCnt += 1

        if GPIO6.is_pressed:
            buttonX = 1
            buttonXCnt = 0
        elif buttonXCnt >= BUTTON_ERROR_RESOLUTION:
            buttonX = 0
        else:
            buttonXCnt += 1

        if GPIO24.is_pressed:
            buttonY = 1
            buttonYCnt = 0
        elif buttonYCnt >= BUTTON_ERROR_RESOLUTION:
            buttonY = 0
        else:
            buttonYCnt += 1

        GPIO27.off()
        #############################################
        
        #############################################
        # Start, Select, R1, L1 (soon to be R3, L3)
        #############################################
        GPIO22.on()
        if GPIO23.is_pressed:
            buttonSel = 1
            buttonSelCnt = 0
        elif buttonSelCnt >= BUTTON_ERROR_RESOLUTION:
            buttonSel = 0
        else:
            buttonSelCnt += 1

        if GPIO5.is_pressed:
            buttonStart = 1
            buttonStartCnt = 0
        elif buttonStartCnt >= BUTTON_ERROR_RESOLUTION:
            buttonStart = 0
        else:
            buttonStartCnt += 1

        if GPIO6.is_pressed:
            buttonL = 1
            buttonLCnt = 0
        elif buttonLCnt >= BUTTON_ERROR_RESOLUTION:
            buttonL = 0
        else:
            buttonLCnt += 1

        if GPIO24.is_pressed:
            buttonR = 1
            buttonRCnt = 0
        elif buttonRCnt >= BUTTON_ERROR_RESOLUTION:
            buttonR = 0
        else:
            buttonRCnt += 1
        GPIO22.off()
        #############################################

        #############################################
        # Coming Soon: L1, L2, R1, R2 
        # (assuming R2/L2 are not analog)
        #############################################
        #############################################

        #print("|__" + str(dUp) + "__|__" + str(dLeft) + "__|___" + str(dRight) + "___|__" + str(dDown) + "__|_" + str(buttonA) + "_|_" + str(buttonB) + "_|_" + str(buttonX) + "_|_" + str(buttonY) + "_|__" + str(buttonSel) + "__|___" + str(buttonStart) + "___|_" + str(buttonL) + "_|_" + str(buttonR) + "_|____" + str(leftAnalogY).zfill(6) + "____|____" + str(leftAnalogX).zfill(6) + "____|____" + str(rightAnalogY).zfill(6) + "____|____" + str(rightAnalogX).zfill(6) + "____|", end='\r')

        #############################################
        # Left Analog Values
        #############################################
        # Adjust ADC Values from 0 to 1, to -1000 to 1000
        leftAnalogY = int(chan1.value * 2000) - 1000
        # Instantiate deadzone
        if abs(leftAnalogY) <= CENTER_TOLERANCE:
            leftAnalogY = 0

        leftAnalogX = int(chan2.value * 2000) - 1000
        if abs(leftAnalogX) <= CENTER_TOLERANCE:
            leftAnalogX = 0
        #############################################

        #############################################
        # Right Analog Values
        #############################################
        rightAnalogY = int(chan3.value * 2000) - 1000
        if abs(rightAnalogY) <= CENTER_TOLERANCE:
            rightAnalogY = 0

        rightAnalogX = int(chan4.value * 2000) - 1000
        if abs(rightAnalogX) <= CENTER_TOLERANCE:
            rightAnalogX = 0
        #############################################

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
    GPIO17.off()
    GPIO27.off()
    GPIO22.off()
    exit("Something went horribly wrong")      
sys.exit(0)
