"""
scripts are user defined keywords that map directly to deterministic commands
"""
import time
import string
import tools
from word2num import word2num
import pyautogui

KEYS_HELD = []
def call_script(command):
    """
    Checks a command against a set of scripted command patterns
    If the command matches the pattern, do executed the scripted action and return True
    if no pattern matched, return False
    """

    command_lowercase = command.lower().replace(".","")
    command_stripped = command_lowercase.strip().replace(" ", "")
    parts = command_lowercase.split(" ")


    if parts[0] in ("press","hit") and len(parts) > 1:
        key = "+".join(parts[1:])
        key.replace("control", "ctrl")
        print("pressing {}".format(key))
        tools.keyPress(key)
        return True

    if parts[0] in ("mouse", "mass", "cursor"):
        if len(parts) < 3:
            return False
        try:
            amount = int(parts[2])
        except ValueError:
            amount = int(word2num(" ".join(parts[2:])))

        if parts[1] == "up": tools.moveMouseRel(0, -amount)
        elif parts[1] == "down": tools.moveMouseRel(0, amount)
        elif parts[1] == "left": tools.moveMouseRel(-amount, 0)
        elif parts[1] in ( "right", "write"): tools.moveMouseRel(amount, 0)
        
        return True
   
    if command_stripped == "leftclick":
        tools.leftClick()
        return True

    if command_stripped == "rightclick":
        tools.rightClick()
        return True

    if command_stripped == "doubleclick":
        tools.doubleClick()
        return True

    if command_stripped == "holdclick":
        tools.clickAndHold()
        return True

    if command_stripped == "release":
        tools.release()
        return True

    if command_stripped.startswith("type"):
        if command_stripped == "type":
            return False

        else:
            text = command[5:]
            tools.typeText(text)
            return True 

    if command_stripped.startswith("open"):
        app = " ".join(parts[1:])
        tools.openApp(app)
        return True
    
    if command_stripped.startswith("goto"):
        app = command.replace("go to", "")
        app = app.replace("goto", "")
        if app.startswith(" "):
            app = app[1:]
        tools.openApp(app)
        return True
   
    if command_stripped == "close":
        tools.keyPress("f4")
        return True

    if command_stripped == "tabover":
        tools.keyPress("ctrl+tab")
        return True

    if command_stripped == "tabback":
        tools.keyPress("ctrl+shift+tab")
        return True

    if command_stripped == "newwindow":
        tools.keyPress("ctrl+shift+n")
        return True
    
    if command_stripped == "newtab":
        tools.keyPress("ctrl+t")
        return True

    if command_stripped == "reopentab":
        tools.keyPress("ctrl+shift+t")
        return True

    if command_stripped == "closetab":
        tools.keyPress("ctrl+w")
        return True

    if command_stripped == "tabover":
        tools.keyPress("ctrl+tab")
        return True


    if command_stripped == "tabback":
        tools.keyPress("ctrl+shift+tab")
        return True

    if command_stripped == "searchbar":
        tools.keyPress("alt+d")
        return True

    if parts[0] in "hold":
        if len(parts) == 1:
            return False
        global KEYS_HELD
        keys = "+".join(parts[1:])
        tools.holdKeys(keys)
        KEYS_HELD.append(keys)
        return True

    if command_stripped == "releasekeys":
        for key in KEYS_HELD:
            tools.releaseKeys(key)
        return True

    if command_stripped.startswith("appselect"):
        tools.holdKeys("alt")
        KEYS_HELD.append("alt")
        tools.keyPress("tab")
        time.sleep(0.2)
        return True

    if command_stripped == "goback":
        pyautogui.hotkey("alt","left")
        return True

    if command_stripped == "swapwindow":
        pyautogui.keyDown("alt")
        pyautogui.press("tab")
        time.sleep(0.2)
        pyautogui.keyUp("alt")

    if command_stripped == "enter":
        pyautogui.press('enter')

    return False

