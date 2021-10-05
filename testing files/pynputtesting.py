from pynput import keyboard
import time

def on_press(key):
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

mark = True
if __name__ == '__main__':
    # ...or, in a non-blocking fashion:
    listener = keyboard.Listener(on_press=on_press, on_release=on_release, suppress = True)
    listener.start()

    while mark:
        pass
    
    print('Closing down!')