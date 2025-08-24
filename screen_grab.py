import pyautogui
import time
from PIL import ImageGrab

def capture_screen(file_path: str = "screenshot.png"):
    screenshot = ImageGrab.grab() 
    screenshot.save(file_path)

if __name__ == "__main__":
    capture_screen()
