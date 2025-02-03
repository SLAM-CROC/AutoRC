import pigpio
import pygame as pg
import subprocess
import PiRecording as Pir
import time

#______________________________GPT___________________________________
def ensure_pigpiod_running():
    try:
        result = subprocess.run(['pgrep', 'pigpiod'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        if result.returncode != 0:
            print("pigpiod is not running. Starting it now...")
            subprocess.run(['sudo', 'pigpiod'], check=True)
        else:
            print("pigpiod is already running.")
    except Exception as e:
        print(f"Error ensuring pigpiod is running: {e}")
    
    

ensure_pigpiod_running()
time.sleep(1)
pi = pigpio.pi()
if not pi.connected:
    raise RuntimeError("Failed to connect to pigpio daemon.")


pinREC = 25
pi.set_mode(pinREC, pigpio.OUTPUT)

def startup_signal():
    for _ in range(3):
        pi.write(pinREC, 1)
        time.sleep(0.5)
        pi.write(pinREC, 0)
        time.sleep(0.5)

startup_signal()


def apply_deadzone(value, deadzone):
    """Applies a deadzone to joystick axis input."""
    if abs(value) < deadzone:
        return 0
    return value
def ControllerConectionCheck() :
    if pg.joystick.get_count() == 0:
        return False
    else :
        return True

Pir.CameraSetupHandler()
#_____________________________GPT_________________________

pg.init()
pg.joystick. init()
#pg.display.set_mode((300,300))
#pg.display.set_caption("Drivin Controller")
Clock = pg.time.Clock()
if (ControllerConectionCheck()) :
    joystick = pg.joystick.Joystick(0)
    joystick.init()

#PWM Variables
pin1 = 12 # GPIO Pin Number
pin2 = 13 # ^
Freq = 50 # in Hz

# #REC Light Variables
# pinREC = 25


pi.set_PWM_range(pin1,1000) #Scales the Range of the Steering PWM Function
pi.set_PWM_frequency(pin1, Freq)
pi.set_PWM_range(pin2,1000) #Scales the Range of the Throttle PWM Function
pi.set_PWM_frequency(pin2, Freq)


operating = True
DEADZONE =  0.1
inputValue = 0
button_states = {}
#Control Variables
ControlMsOut = 1.0 # in milliseconds
ControlAxis = 0.0
ControlMsCentered = 1.07
ControlMsRange = .1702
ControlLScale = 1.1

#Throttle Variables
ThrottleMsOut = 0
ThrottleAxis = 0.0
ThrottleMsCentered = 1.35

ThrottleMsRange = .25
ThrottleKey = 1

#Camera Control Variables
Recording = False


#GPT---------------------------------------------------------------------------------------------
def ControllerReconnectionHandler():
    """Handle reconnection of the controller."""
    global joystick
    if(pg.joystick.get_count() == 0) :
        print("Controller Disconnected. Please Wait For Reconnection.")
    else:
        joystick = pg.joystick.Joystick(0)
        joystick.init()



def handle_one_shot_button(button_index):
    """
    Detect a one-shot press for a specific button.

    Args:
        button_index (int): The index of the button to track.

    Returns:
        bool: True if the button is pressed as a one-shot, False otherwise.
    """
    global button_states
    if joystick is not None:
        # Initialize the button state if not already tracked
        if button_index not in button_states:
            button_states[button_index] = False  # Initially not pressed
        
        # Get the current state of the button
        button_current = joystick.get_button(button_index)
        
        # Check for one-shot press
        if button_current == 1 and not button_states[button_index]:
            button_states[button_index] = True  # Update the state
            return True  # Button was pressed (one-shot)
        elif button_current == 0 and button_states[button_index]:
            button_states[button_index] = False  # Reset the state on release

    return False  # No one-shot press detected
#GPT-------------------------------------------------------------------------------------
def updateControlDuty() :
    global ControlMsOut,Freq
    Duty = ControlMsOut / (1/pi.get_PWM_frequency(pin1) * 1000)
    pi.set_PWM_dutycycle(pin1, (Duty*1000 ) )
    #print(Duty * 1000)

def updateThrottleDuty() :
    global ControlMsOut,Freq
    Duty = ThrottleMsOut / (1/pi.get_PWM_frequency(pin1) * 1000)
    if(ControllerConectionCheck()) :
         pi.set_PWM_dutycycle(pin2, (Duty*1000 ) )
    else :
        pi.set_PWM_dutycycle(pin2, (0 ) )
    #print(Duty * 1000)
    
def WindowHanlder() :
    global operating
    for event in pg.event.get():  # Check for events
            if event.type == pg.QUIT:  # If the window close button is clicked
                operating = False  # Exit the loop and stop the program
    

def getKeyboardInputs() :
    
    global ControlAxis, ThrottleAxis
    
    keys = pg.key.get_pressed()
    
    a = 0
    b = 0
    
    
    if (keys[pg.K_LEFT]) :
        #print("left is Pressed")
        a -= 1 
    if ((keys[pg.K_RIGHT]) ) :
        #print("Right is Pressed")
        a += 1
   

    
    if (keys[pg.K_DOWN]) :
        #print("left is Pressed")
        b -= 1 
    if ((keys[pg.K_UP]) ) :
        #print("Right is Pressed")
        b += 1
   

    ControlAxis = a # NEED TO BE HERE TO RESET, WILL NOT RESET IN FUNCTION
    ThrottleAxis = b
    
def SteeringHandler() :
    global ControlMsCentered, ControlAxis, ControlMsRange, ControlMsOut
    ControlMsOut = ControlMsCentered + ControlMsRange * ControlAxis
    #print(ControlAxis)
def ThrottleHandler():
    global ThrottleMsCentered, ThrottleAxis, ThrottleMsRange,ThrottleMsOut, ThrottleKey
    ThrottleMsOut = ThrottleMsCentered + ThrottleMsRange * ThrottleAxis * ThrottleKey
    print(ThrottleMsOut)

def getControllerInputs() :
    global DEADZONE, ControlAxis, ThrottleAxis,ThrottleKey, ThrottleMsCentered
    ControlAxis = apply_deadzone(joystick.get_axis(0),DEADZONE)
    ThrottleAxis = joystick.get_axis(4)/2  +.5
    #print(ThrottleAxis)

    if(handle_one_shot_button(4)):
        CameraFlipFlopHandler()


    if(joystick.get_button(6)) :
        print("Put it in reverse terry!")
        ThrottleKey = -1.5
        
    else :
        ThrottleKey = 1
        
    

def InputHandler() :
    global inputValue, ControlAxis, ThrottleAxis

    ControlAxis = 0 #NEED TO BE HERE TO RESET CONROL AXIS WHEN COTNROLLER IS NOT PLUGGED IN. 
    ThrottleAxis = 0

    keys = pg.key.get_pressed()    
    if any(keys) :
        inputValue = 0
        #print("Keyboard Input")
    
    else:
        inputValue = 1
        #print("Controller Input")

    match inputValue :
        case 0 :
            getKeyboardInputs()
        case 1:
            if(ControllerConectionCheck()) :
                getControllerInputs()
    

def CameraFlipFlopHandler() :
    global Recording
    if  not Recording :
        Pir.start_recording(Pir.output_file)
        print("Started Recording")
        
    else :
        Pir.stop_recording()
    
    Recording = not Recording

def RecordingLightHandler() :
    global Recording, pinREC
    if(Recording) :
        pi.write(pinREC, 1)
    else :
        pi.write(pinREC, 0)

#--------------------MAIN LOOP---------------------------------------------------

#ControllerConectionCheck()

#pg.display.update()

try:
    while operating:
        
        RecordingLightHandler()
        pg.event.pump()
        WindowHanlder()  
        

        ControllerReconnectionHandler()
        InputHandler()
        SteeringHandler()
        ThrottleHandler()
        
        updateThrottleDuty()
        updateControlDuty()
        Clock.tick(60) # Limit it to 60 updates per second, can be reduced to spare processing power
except KeyboardInterrupt :
    print("\nSim has Ended")

pi.write(pinREC, 0)

#Closing Commands
pg.quit()
pi.set_PWM_dutycycle(pin1,  0)
pi.set_PWM_dutycycle(pin2,  0)
Pir.CameraEnd()


