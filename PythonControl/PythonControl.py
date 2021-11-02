from serial import Serial
import keyboard
import pyautogui

arduino = Serial(port='COM5', baudrate=9600, timeout=.1)
throttle_pos = 0
init_pos = False

# Divisor for throttle
DIVISOR = 44

# GEOFS plane speed
speed = 0

def read():
    data = arduino.readline()
    
    try:
        return int(data.decode())
    
    except Exception:
        # Serial recieve takes time, therefore there might be nothing to decode
        # at first, so this try/except is here
        return False

while True:
    if keyboard.is_pressed('enter'):
        arduino.close()
        break
    
    recieved = read() - 300

    # make sure that something was successfully recieved
    if recieved:
        if not init_pos:
            throttle_pos = recieved
            init_pos = True
            speed = throttle_pos // DIVISOR
            print('init pos set')
        
        # if throttle pos changed(small range here)
        if not (throttle_pos + 2 >= recieved >= throttle_pos - 2):
            throttle_pos = recieved
            old_speed = speed
            speed = throttle_pos // DIVISOR
            
            if speed < 0:
                speed = 0
            
            if speed > 9:
                speed = 9

            # if change in speed
            if speed != old_speed:
                pyautogui.press(str(speed))
            
            
    