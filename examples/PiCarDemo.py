import pigpio
import time
import subprocess

#Defining Variables
Freq = 50
pin1 = 12
pin2 = 13

#Steering Ms
StraightMs = 1.07
LeftMs = StraightMs + .1702 
RightMs = StraightMs - .1702 


#Throttle Ms
NeutralMs = 1.5
ForwardMs = 1.65
ReverseMs = 1.15


#GPT Code that gets the Daemon to start Pipio.
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

pi = pigpio.pi()
time.sleep(1)
if not pi.connected:
    raise RuntimeError("Failed to connect to pigpio daemon.")

#GPT Code end

#Sets the operating range of the duty input variable. (In this case, duty is 0-1000 instead of 0-100) 
pi.set_PWM_range(pin1,1000) 
#Sets the frequency of a PWM on a pin.
pi.set_PWM_frequency(pin1, Freq)
pi.set_PWM_range(pin2,1000) 
pi.set_PWM_frequency(pin2, Freq)

def updateSteering(a): #Input goal Ms, convert to duty% and update PWM.
    Duty = a / (1/pi.get_PWM_frequency(pin1) * 1000)
    pi.set_PWM_dutycycle(pin1, (Duty*1000 ) )

def updateThrottle(a): #Input goal Ms, convert to duty% and update PWM.
    Duty = a / (1/pi.get_PWM_frequency(pin1) * 1000)
    pi.set_PWM_dutycycle(pin2, (Duty*1000 ) )

updateThrottle(NeutralMs)
time.sleep(4)
try:
    while True :
        updateSteering(StraightMs)
        updateThrottle(NeutralMs)
        time.sleep(1)
        updateThrottle(ForwardMs)
        time.sleep(2)
        updateThrottle(NeutralMs)
        time.sleep(0.75)
        updateSteering(LeftMs)
        time.sleep(0.5)
        updateSteering(RightMs)
        time.sleep(.5)
        updateSteering(StraightMs)
        time.sleep(.5)
        updateThrottle(ReverseMs)
        time.sleep(.1)
        updateThrottle(NeutralMs)
        time.sleep(.1)
        updateThrottle(ReverseMs)
        time.sleep(2)
        updateThrottle(NeutralMs)
        time.sleep(0.75)
        updateSteering(LeftMs)
        time.sleep(0.5)
        updateSteering(RightMs)
        time.sleep(.5)
        updateSteering(StraightMs)
        time.sleep(.5)
except KeyboardInterrupt:
    print("Demo Ended")

#TURN OFF ALL PWMS FOR TH LOVE OF GOD
pi.set_PWM_dutycycle(pin1,  0)
pi.set_PWM_dutycycle(pin2,  0)