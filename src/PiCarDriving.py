import pigpio
import pygame as pg
import subprocess
import PiRecording as Pir
import time
import threading

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

def apply_deadzone(value, deadzone): #Returns a value as long as its bigger than the gien deadzone
    """Applies a deadzone to joystick axis input."""
    if abs(value) < deadzone:
        return 0
    return value
def ControllerConectionCheck() : # Returns True or False if a controler is connected or not
    if pg.joystick.get_count() == 0:
        return False
    else :
        return True

#_____________________________GPT_________________________

camConnected = False #This variable is used to manage camera connection adn avoid errors, if there is a camera then camera functions will be called. if not, skip them. Avoids the intrinsic error of the picamera2 library and there not being a camera

try:
    threading.Thread(target=Pir.CameraSetupHandler()).start() #Multithread the Functions relating to the camera
    camConnected = True
    
    
except :
    if(camConnected != True) :
        print("No Camera Connected")
        camConnected = False



pg.init() #Initialzie the pygame library
pg.joystick. init() #Inititalize the pyganme controller reader
#pg.display.set_mode((300,300))
#pg.display.set_caption("Drivin Controller")
Clock = pg.time.Clock() #Needed to add an update rate to the program to reduce CPU oad
if (ControllerConectionCheck()) : # Initialzies the connection with a controller thats connected.
    joystick = pg.joystick.Joystick(0)
    joystick.init()

#PWM Variables
pin1 = 12 # GPIO Pin Number
pin2 = 13 # ^
Freq = 50 # in Hz

#REC Light Variables
pinREC = 25


def startup_signal(): #Siqi made this signal to tell when the car is ready
    for _ in range(3):
        pi.write(pinREC, 1)
        time.sleep(0.5)
        pi.write(pinREC, 0)
        time.sleep(0.5)


startup_signal()


pi.set_PWM_range(pin1,1000) #Scales the Range of the Steering PWM Function
pi.set_PWM_frequency(pin1, Freq)
pi.set_PWM_range(pin2,1000) #Scales the Range of the Throttle PWM Function
pi.set_PWM_frequency(pin2, Freq)


operating = True #main loop variable
DEADZONE =  0.1 #Deadzone for the input of the controler sticks
inputValue = 0 #Used to differentiate between controller and keyboard inputs
button_states = {} #Used by gpt code to log a one time button press
#Control Variables, related to sterring
ControlMsOut = 1.0 # in milliseconds
ControlAxis = 0.0
ControlMsCentered = 1.07 #The point where the servo is centered
ControlMsRange = .1702 #How far the servo can go left or right to ot damage the car


#Throttle Variables
ThrottleMsOut = 0
ThrottleAxis = 0.0
ThrottleMsCentered = 1.35 # in between forward and reverse for the speed controller
ThrottleMsRange = .25 #How far back and forth for a limited FWD and REv speed
ThrottleKey = 0 #used to manage the Digital Transmission

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
def updateControlDuty() : #Upates teh steering based on the desired ms output calculated 
    global ControlMsOut,Freq
    Duty = ControlMsOut / (1/pi.get_PWM_frequency(pin1) * 1000)
    pi.set_PWM_dutycycle(pin1, (Duty*1000 ) ) # this is what changes the PWM duty, mathed to the given Ms output.
    #print(Duty * 1000)

def updateThrottleDuty() : #updates the drive PWM based of the desired ms output from calculations
    global ControlMsOut,Freq
    Duty = ThrottleMsOut / (1/pi.get_PWM_frequency(pin1) * 1000)
    if(ControllerConectionCheck()) : #Turns off the drive if the controller disconnects, emergency feature
         pi.set_PWM_dutycycle(pin2, (Duty*1000 ) )
    else :
        pi.set_PWM_dutycycle(pin2, (0 ) )
    #print(Duty * 1000)
    
def WindowHanlder() : # a window handler for a visual reference while debugging, unused as of now
    global operating
    for event in pg.event.get():  # Check for events
            if event.type == pg.QUIT:  # If the window close button is clicked
                operating = False  # Exit the loop and stop the program
    

def getKeyboardInputs() : # manages the control axis and throttle axis based off the arrowkey inputs
    
    global ControlAxis, ThrottleAxis
    
    keys = pg.key.get_pressed() # gets input keys
    
    a = 0
    b = 0
    
    
    if (keys[pg.K_LEFT]) : # left key, etc
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
    
def SteeringHandler() : # Calculates the desired Steering Ms output basd of collected data and the user's input
    global ControlMsCentered, ControlAxis, ControlMsRange, ControlMsOut
    ControlMsOut = ControlMsCentered + ControlMsRange * ControlAxis
    #print(ControlAxis)
    #print(ControlMsOut)
def ThrottleHandler(): # ^^^ but for thottle
    global ThrottleMsCentered, ThrottleAxis, ThrottleMsRange,ThrottleMsOut, ThrottleKey
    ThrottleMsOut = ThrottleMsCentered + ThrottleMsRange * ThrottleAxis * ThrottleKey
    #print(ThrottleMsOut)

def getControllerInputs() : #obtains controller inputs with pygame
    global DEADZONE, ControlAxis, ThrottleAxis,ThrottleKey, ThrottleMsCentered,ThrottleMsOut
    ControlAxis = apply_deadzone(joystick.get_axis(0),DEADZONE)
    ThrottleAxis = joystick.get_axis(4)/2  +.5 #gets number here
    #print(ThrottleAxis)

    if(handle_one_shot_button(4)): #Start recording
        CameraFlipFlopHandler()

    dpad = joystick.get_hat(0) # Handles dpad input for transmission usage
    if(dpad[1] == 1) :
        ThrottleKey = 1
        
    elif(dpad[1] == -1) :
        ThrottleKey = -0.625
    elif(dpad[0] == 1 or dpad[0] == -1):
        ThrottleKey = 0

    a = ThrottleMsOut/(ThrottleMsCentered + ThrottleMsRange) #Controls rumble for fun
    #print(a)
    if(a > .85):
        joystick.rumble(0,a,0)
    elif(a < .83) :
        joystick.rumble(a,0,0)
    else :
        joystick.stop_rumble()
    
    
    

        
    

def InputHandler() : #Prioritizes instanced keyboard inputs over constant controller inputs
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
    

def CameraFlipFlopHandler() : # Starts recording using the GPT generated library
    global Recording

    if  not Recording :
        if(camConnected) : #only do it when cam is connected, avoids errors
            threading.Thread(target=Pir.start_recording(Pir.output_file)).start()
            
            print("Started Recording")
        
    else :
        if(camConnected) :
            threading.Thread(target=Pir.stop_recording()).start()
            print("Stopped Recording")
    
    Recording = not Recording

def RecordingLightHandler() : # Turns on an LED on when recording, off when not recording
    global Recording, pinREC
    if(Recording) :
        pi.write(pinREC, 1) # on
    else :
        pi.write(pinREC, 0) # off

#--------------------MAIN LOOP---------------------------------------------------

#ControllerConectionCheck()

#pg.display.update()

try:
    while operating: #calls functions over and over until the pi is turned off or commanded by the keyobard
        
        RecordingLightHandler()
        pg.event.pump()
        WindowHanlder()  
        #print(camConnected)

        ControllerReconnectionHandler()
        InputHandler()
        SteeringHandler()
        ThrottleHandler()
        
        updateThrottleDuty()
        updateControlDuty()
        Clock.tick(60) # Limit it to 60 updates per second, can be reduced to spare processing power
except KeyboardInterrupt :
    print("\nProgram Ended")

#Closing Commands, turns off PWMS, 
pg.quit()
pi.set_PWM_dutycycle(pin1,  0)
pi.set_PWM_dutycycle(pin2,  0)
pi.set_mode(pinREC, 0)
if(camConnected) :
    
    threading.Thread(target=Pir.CameraEnd()).start() #turn off camera


