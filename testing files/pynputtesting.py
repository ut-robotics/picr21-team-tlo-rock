from pynput import keyboard
import time

'''def on_press(key):
    try:
        print('alphanumeric key {0} pressed'.format(
            key.char))
    except AttributeError:
        print('special key {0} pressed'.format(
            key))

def on_release(key):
    global mark
    print('{0} released'.format(
        key))
    if key == keyboard.KeyCode.from_char('q'):
        # Stop listener
        mark = False
        return False
'''

def on_press(key):
    global manual_inputs, mark
    print('{0} pressed'.format(key))
    if key == keyboard.KeyCode.from_char('q'):
        # Stop program and listener
        mark = False
        return False
    elif key == keyboard.Key.home:
        manual_inputs[0] = 1
    elif key == keyboard.Key.up:
        manual_inputs[1] = 1
    elif key == keyboard.Key.page_up:
        manual_inputs[2] = 1
    elif key == keyboard.Key.left:
        manual_inputs[3] = 1
    elif key == keyboard.Key.right:
        manual_inputs[4] = 1
    elif key == keyboard.Key.down:
        manual_inputs[5] = 1
    elif key == keyboard.Key.end:
        manual_inputs[6] = 1
        manual_inputs[0] = 0
        manual_inputs[1] = 0
        manual_inputs[2] = 0
        manual_inputs[3] = 0
        manual_inputs[4] = 0
        manual_inputs[5] = 0

def on_release(key):
    global manual_inputs, state
    if key == keyboard.Key.home:
        manual_inputs[0] = 0
    elif key == keyboard.Key.up:
        manual_inputs[1] = 0
    elif key == keyboard.Key.page_up:
        manual_inputs[2] = 0
    elif key == keyboard.Key.left:
        manual_inputs[3] = 0
    elif key == keyboard.Key.right:
        manual_inputs[4] = 0
    elif key == keyboard.Key.down:
        manual_inputs[5] = 0
    elif key == keyboard.Key.end:
        manual_inputs[6] = 0

manual_inputs = [0 for i in range(7)]
mark = True
if __name__ == '__main__':
    # ...or, in a non-blocking fashion:
    listener = keyboard.Listener(on_press=on_press, on_release=on_release, suppress = True)
    listener.start()

    while mark:
        #print(manual_inputs)
        pass
    
    print('Closing down!')