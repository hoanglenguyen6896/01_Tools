from keyboard import *
import time
import threading
sem = threading.Semaphore()
i=0

ALT_START=True

_UP = "UP"
_DOWN = "DOWN"
_LEFT = "LEFT"
_RIGHT = "RIGHT"

_CONFIRM = "ENTER"
# _CONFIRM = "X"
_BACK = "ESC"
# _BACK = "D"

def release_hook(x):
    global ALT_START
    print(f"Released:  {x}")
    ALT_START = False

def get_hook(x):
    print(f"Pressed:  {x}")
    global ALT_START
    if is_pressed("r"):
        press(_LEFT)
        time.sleep(0.2)
        release(_LEFT)
        press(_UP)
        time.sleep(0.1)
        release(_UP)
        print(f"Pressed_sub:  r")

    if is_pressed("s"):
        press(_LEFT)
        time.sleep(0.2)
        release(_LEFT)
        press(_UP)
        time.sleep(0.1)
        release(_UP)
        send(_CONFIRM) # Open Advance menu
        time.sleep(0.05)
        send(_UP) # Move to skip
        time.sleep(0.05)
        send(_CONFIRM) # Skip
        time.sleep(0.05)
        send(_CONFIRM) # Skip
        time.sleep(1)
        send(_CONFIRM) # Skip
        time.sleep(1)
        send(_CONFIRM) # Skip
        time.sleep(1)
        print(f"Pressed_sub:  s")


    if is_pressed("1"):
        # Advanced
        send(_RIGHT) # Team management
        send(_CONFIRM) # Open TM menu
        send(_CONFIRM) # Enter Game Plan
        time.sleep(0.8)
        press(_RIGHT) # Hold to most right
        time.sleep(0.1)
        release(_RIGHT)
        send(_CONFIRM) # Open Save/Load
        send(_DOWN)  # Select Load
        send(_CONFIRM) # Enter Load
        time.sleep(0.2)
        send(_CONFIRM) # Load 1
        send(_CONFIRM) # Confirm Exit
        send(_BACK)   # Back to Save/Load
        send("z")       # Check Stamina
        send(_BACK)   # Back to Game Plan option
        send(_BACK)   # Back to main
        time.sleep(0.8)
        press(_LEFT)
        time.sleep(0.2)
        release(_LEFT)
    # while(ALT_START):rrqq

def on_action(event: KeyboardEvent):
    if event.event_type == KEY_DOWN:
        get_hook(event.name)
    elif event.event_type == KEY_UP:
        release_hook(event.name)

hook(on_action)
while(not is_pressed("q")):
    pass