from pynput import mouse as mse
from pynput import keyboard
import math

mouse = mse.Controller()
running = True

def on_press(key):
    print(key)
    if key == keyboard.KeyCode.from_char('q'):
        global running
        running = False
        return False

def on_move(x, y):
    global running
    if not running:
        return False
    if (not x == 500 and not y == 300):

        print(math.sqrt((x-500)**2 + (y-300)**2))
        
        mouse.position = (500, 300)

listener = mse.Listener(on_move=on_move)
listener.start()

kblistener = keyboard.Listener(on_press=on_press)
kblistener.start()

while running:
    pass