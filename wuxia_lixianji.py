import win32gui
import win32con
import pyautogui
import time
from PIL import ImageGrab
from PIL import Image
import pytesseract

def activate_window(title):
    hwnd = win32gui.FindWindow(None, title)
    if hwnd:
        win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
        # win32gui.SetForegroundWindow(hwnd)
        return hwnd
    return None

def get_window_position(hwnd):
    if hwnd:
        rect = win32gui.GetWindowRect(hwnd)
        x = rect[0]
        y = rect[1]
        w = rect[2] - x
        h = rect[3] - y
        return x, y, w, h
    return None

def click_window_center(hwnd):
    position = get_window_position(hwnd)
    if position:
        x, y, w, h = position

# 替换为您想要激活的窗口标题
window_title = "武侠历险记"

# 激活窗口
hwnd = activate_window(window_title)
window_rect = get_window_position(hwnd)
x, y, width, height = window_rect
print("窗口大小:", width, "x", height)
# 截取窗口图像
image = ImageGrab.grab(bbox=(x, y, x + width, y + height))
image.save("screenshot.png")

left_x = x + width * 0.01
left_y = y + height // 2

right_x = x + width * 0.9

testdata_dir_config = '--tessdata-dir "C:\\Program Files\\Tesseract-OCR\\tessdata"'

# 使用Tesseract进行文字识别
# eng = pytesseract.image_to_string(image, lang='eng')
# chinese = pytesseract.image_to_string(image, lang='chi-sim')
# print(eng)
# print(chinese)

image2 = Image.open('1.png')
chinese2 = pytesseract.image_to_string(image, config=testdata_dir_config, lang='chi-sim')
print(chinese2)

# while(True):
#   activate_window(window_title)
#   # image = ImageGrab.grab(bbox=(x, y, x + width, y + height))
#   # 使用Tesseract进行文字识别
#   # text = pytesseract.image_to_string(image, lang='eng')
#   # print(text)
#   pyautogui.click(left_x, left_y)
#   time.sleep(1)
#   pyautogui.click(right_x, left_y)
#   time.sleep(2)


# 如果您想要将窗口恢复到后台，可以最小化窗口
# win32gui.ShowWindow(hwnd, win32con.SW_MINIMIZE)
