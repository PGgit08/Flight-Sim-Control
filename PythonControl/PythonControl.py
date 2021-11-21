from serial import Serial
import keyboard
import pyautogui
import time

# connect to arduino and set up variables
arduino = Serial(port='COM5', baudrate=9600, timeout=.1)

# GEOFS values
throttle = 0
pitch = 0
roll = 0

# Screen dimensions for mouse movement
WIDTH, HEIGHT = pyautogui.size()

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
        
        print(throttle, pitch, roll)
        keyboard.press_and_release(str(throttle))

    # delay a bit and reply
    time.sleep(0.01)
    reply()
