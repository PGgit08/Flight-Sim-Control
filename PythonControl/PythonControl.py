from serial import Serial
import keyboard
import pyautogui
import time

# pyautogui settings
pyautogui.FAILSAFE = False

# connect to arduino and set up variables
arduino = Serial(port='COM5', baudrate=9600, timeout=.1)

# GEOFS values
throttle = 0
pitch = 0.00
roll = 0.00

# screen dimensions for mouse movement
WIDTH, HEIGHT = pyautogui.size()
HALF_WIDTH = WIDTH / 2
HALF_HEIGHT = HEIGHT / 2

# move mouse function
def move():
    global mouseX, mouseY
    pyautogui.moveTo(mouseX, mouseY)

# click throttle values function
def clickThrottle():
    global throttle
    keyboard.press_and_release(str(throttle))

# mouse positions (initial)
mouseX = HALF_WIDTH
mouseY = HALF_HEIGHT

# set initial positions through GUI
move()
clickThrottle()

# old values to prevent unneeded movements
old_throttle = throttle
old_mouseX = mouseX
old_mouseY = mouseY 

# pre-loop message(s)
print("CLICK ENTER TO EXIT \n")

# read from device
def read():
    data = arduino.read_until(b"o")
    
    return data.decode()

# reply to arduino
def reply():
    arduino.write(b'o')

# set geofs values from arduino
def setValues(input_list):
    global throttle, pitch, roll

    throttle = int(input_list[0])
    pitch = float(input_list[1])
    roll = float(input_list[2])

while True:
    if keyboard.is_pressed('enter'):
        arduino.close()
        break

    # read
    recieved = read()

    # make sure recieved something
    if(len(recieved) > 0):
        valList = recieved.replace('o', '').split(',')

        # sometimes there might be a small error in recieving, so just use old working values
        try:
            setValues(valList)
        
        except Exception:
            pass


        # get new mouseX and mouseY positions
        mouseX = (roll * HALF_WIDTH) + HALF_WIDTH
        mouseY = (pitch * HALF_HEIGHT) + HALF_HEIGHT

        # old values to prevent unneeded movements
        if(mouseX != old_mouseX):
            move()
            old_mouseX = mouseX

        if(mouseY != old_mouseY):
            move()
            old_mouseY = mouseY
        
        if(throttle != old_throttle):
            clickThrottle()
            old_throttle = throttle


        # print(throttle, pitch, roll)

    # delay a bit and reply
    time.sleep(0.01)
    reply()
