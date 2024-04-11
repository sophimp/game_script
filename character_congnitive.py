import cv2
import pytesseract
from pytesseract import Output

# 配置Tesseract的路径
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Windows示例路径
# pytesseract.pytesseract.tesseract_cmd = '/usr/local/bin/tesseract'  # macOS或Linux示例路径

# 读取图像
image = cv2.imread('screenshot.png')

# 转换图像为灰度
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# 使用Tesseract进行文字识别
# output_type参数设置为Output.DICT，以便获取详细的识别结果
custom_config = r'--oem 3 --psm 6 -l chi_sim'
details = pytesseract.image_to_data(gray, output_type=Output.DICT, config=custom_config)

# 遍历每个识别的文字
for i in range(len(details['text'])):
    # 如果有文字置信度高于某个阈值（例如50），则将其绘制在图像上
    if int(details['conf'][i]) > 50:
        (x, y, w, h) = (details['left'][i], details['top'][i], details['width'][i], details['height'][i])
        image = cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
        image = cv2.putText(image, details['text'][i], (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX,
                            0.5, (0, 0, 255), 1, cv2.LINE_AA)

# 显示图像
cv2.imshow('Image', image)
# cv2.imshow('GrayImage', gray)
cv2.waitKey(0)
cv2.destroyAllWindows()
