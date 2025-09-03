import pyautogui
import time

def _type_cast(*arg_types):
    def _decorator(fn):
        def inner(*inner_args):
            new_args = [arg_type(inner_arg) for arg_type, inner_arg in zip(arg_types, inner_args)]
            for a in new_args: print(f"{a}: {type(a)}")
            return fn(*new_args)
        return inner
    return _decorator

def openApp(appName: str):
    appName = str(appName)
    print("pressing windows")
    pyautogui.press("win")
    time.sleep(0.2)
    print("writing app name")
    pyautogui.typewrite(appName)
    time.sleep(0.2)
    pyautogui.press('enter')
    time.sleep(0.2)

def drag(x1, y1, x2, y2):
    leftClick(x1, y1)
    time.sleep(0.2)
    moveMouse(x2, y2)
    time.sleep(0.2)
    release()

def moveMouse(x: int, y:int):
    x = int(x)
    y = int(y)
    pyautogui.moveTo(x, y)
    time.sleep(0.2)

def moveMouseRel(dx: int, dy: int):
    curx, cury = pyautogui.position()
    sizex, sizey = pyautogui.size()

    newx = (int(dx)/100)*sizex + curx
    newy = (int(dy)/100)*sizey + cury
    moveMouse(newx, newy)


def leftClick(x: int=None, y: int=None):
    if x and y:
        moveMouse(x, y)
    pyautogui.click(button='left')

def rightClick(x: int=None, y: int=None):
    if x and y:
        moveMouse(x, y)
    pyautogui.click(button='right')

def doubleClick(x: int=None, y: int=None):
    if x and y:
        moveMouse(x, y)
    pyautogui.doubleClick()

def clickAndHold():
    pyautogui.mouseDown(button='left')


def release():
    pyautogui.mouseUp(button='left')



def holdKeys(key: str):
    pyautogui.keyDown(key)

def releaseKeys(key: str):
    pyautogui.keyUp(key)


def typeText(text: str):
    text = str(text)
    pyautogui.typewrite(text)

def scroll(scrollBy: int):
    scrollBy = int(scrollBy)
    pyautogui.scroll(-scrollBy)

def keyPress(keyName: str):
    keyName = str(keyName)
    keys = keyName.split('+')
    pyautogui.hotkey(*keys)


def wait(length: int = 1):
    time.sleep(int(length))

def use_tool(toolName: str, toolArguments: dict, **kwargs):
    globals()[toolName](**toolArguments)



if __name__ == "__main__":
    import sys
    function_name = sys.argv[1]
    raw_args = sys.argv[2:]
    locals()[function_name](*raw_args)
