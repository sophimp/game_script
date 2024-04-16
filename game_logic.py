
import cv2
import pytesseract
from pytesseract import Output
from PIL import ImageGrab
from PIL import Image
import numpy as np
import pyautogui
import time
import win32gui
import win32con

# 配置Tesseract的路径
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Windows示例路径
# pytesseract.pytesseract.tesseract_cmd = '/usr/local/bin/tesseract'  # macOS或Linux示例路径

def isFighting(winRect):
  x, y, width, height = winRect
  # 截取窗口图像
  pilImg = ImageGrab.grab(bbox=(x, y, x + width, y + height//5))
  numpyImage = np.array(pilImg)
  # 转换图像为灰度图
  gray_image = cv2.cvtColor(numpyImage, cv2.COLOR_BGR2GRAY)
  cv2.imwrite("topImag.png", gray_image)
  # 使用Tesseract OCR进行汉字识别
  text = pytesseract.image_to_string(gray_image, lang='chi_sim')  # 使用中文简体模型
  print(text)

# 地图单元格大小
def mapItemSize(winWidth:int, winHeight:int):
  itemWidth = winWidth // 10
  itemheight = winHeight // 8
  return (itemWidth, itemheight)

def coordinateImage(winRect, pilImage: Image):
  numpyImage = np.array(pilImage)
  x, y, width, height = winRect
  itemWidth, itemheight = mapItemSize(width, height)
  # print("itemSize:", itemWidth, ",", itemheight)
  # 地图的坐标从0,0开始，不依赖窗口
  for i in range(0,10):
    itemX = i * itemWidth
    for j in range(0, 9):
      itemY = 44 + itemheight * j
      # print("itemXY:", itemX, ",", itemY)
      numpyImage = cv2.rectangle(numpyImage, (itemX, itemY), (itemX + itemWidth, itemY + itemheight), (0, 255, 0), 2)
      numpyImage = cv2.putText(numpyImage, f"{itemX}", (itemX, itemY + 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1, cv2.LINE_AA)
  return numpyImage

def activeForgroundAndClick(hwnd, x : int, y : int, sleepTime : float):
  win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
  win32gui.SetForegroundWindow(hwnd)
  time.sleep(0.2)
  pyautogui.click(x, y)
  if sleepTime > 0:
    time.sleep(sleepTime)


def clickAd(hwnd, winRect, pilImage: Image): 
  # 点击图片调试
  numpyImage = np.array(pilImage)
  x, y, width, height = winRect
  itemWidth, itemHeight = mapItemSize(width, height)
  print("itemSize:", itemWidth, itemHeight)
  settingX = int(itemWidth * 8 + 5)
  settingY = 60
  # 进入设置页面
  pyautogui.click(x + settingX, y + settingY)
  time.sleep(0.3)
  adX = int(itemWidth * 4)
  adY = int(44 + itemHeight * 3)
  boxX = int(itemWidth * 6)
  boxY = int(44 + itemHeight * 3)
  closeX = int(width - itemWidth / 2)
  closeY = 70
  # 点击图片调试
  # numpyImage = cv2.rectangle(numpyImage, (settingX, settingY), (settingX + 10, settingY + 10), (0, 255, 0), 2)
  # numpyImage = cv2.rectangle(numpyImage, (adX, adY), (adX + 10 , adY + 10), (0, 255, 0), 2)
  # numpyImage = cv2.rectangle(numpyImage, (boxX, boxY), (boxX + 10 , boxY + 10 ), (0, 255, 0), 2)
  # numpyImage = cv2.rectangle(numpyImage, (closeX, closeY), (closeX + 10 , closeY + 10 ), (0, 255, 0), 2)
  # cv2.imwrite("click_ad.png", numpyImage)

  for i in range(1,8):
    activeForgroundAndClick(hwnd, boxX + x, boxY + y, 0.3)
    activeForgroundAndClick(hwnd, adX + x, adY + y, 16)
    activeForgroundAndClick(hwnd,closeX + x, closeY + y, 0.3)
    activeForgroundAndClick(hwnd, adX + x, adY + y, 16)
    activeForgroundAndClick(hwnd, closeX + x, closeY + y, 0.3)
    activeForgroundAndClick(hwnd, boxX + x, boxY + y, 0.3)
    activeForgroundAndClick(hwnd, adX + x, adY + y, 16)
    activeForgroundAndClick(hwnd, closeX + x, closeY + y, 0.3)
    activeForgroundAndClick(hwnd, adX + x, adY + y, 16)
    activeForgroundAndClick(hwnd, closeX + x, closeY + y, 0.3)

  for i in range(1, 6):
    activeForgroundAndClick(boxX + x, boxY + y, 61)



# 使用Tesseract进行文字识别
# output_type参数设置为Output.DICT，以便获取详细的识别结果
# custom_config = r'--oem 3 --psm 6 -l chi_sim'
# details = pytesseract.image_to_data(gray, output_type=Output.DICT, config=custom_config)

# # 遍历每个识别的文字
# for i in range(len(details['text'])):
#     # 如果有文字置信度高于某个阈值（例如50），则将其绘制在图像上
#     if int(details['conf'][i]) > 50:
#         (x, y, w, h) = (details['left'][i], details['top'][i], details['width'][i], details['height'][i])
#         image = cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
#         image = cv2.putText(image, details['text'][i], (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX,
#                             0.5, (0, 0, 255), 1, cv2.LINE_AA)

# # 显示图像
# cv2.imshow('Image', image)
# # cv2.imshow('GrayImage', gray)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
