from serial import Serial
import keyboard

arduino = Serial(port='COM5', baudrate=9600, timeout=.01)
throttle_pos = 0
init_pos = False

def read():
    data = arduino.read_until()
    
    try:
        return int(data.decode())
    
    except Exception:
        # Serial recieve takes time, therefore there might be nothing to decode
        # at first, so this try/except is here
        return False

while True:
    if keyboard.is_pressed('q'):
        arduino.close()
        break
    
    recieved = read()

    # make sure that something was successfully recieved
    if recieved:

        if not init_pos:
            print('not init pos')
            throttle_pos = recieved
            init_pos = True
        
        # if throttle pos changed(small range here)
        if not (throttle_pos + 2 >= recieved >= throttle_pos - 2):
            print(recieved)
            throttle_pos = recieved
            
    