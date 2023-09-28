import numpy as np
import cv2 as cv
from PIL import Image, ImageFont, ImageDraw


def pillowImagePrintGray(img,densityString= """.\'`^",:;Il!i<~+_-?[{1(|/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$""",fontSize = 15):
    # For Normal
    image_height,image_width,_ = img.shape
    font_height, font_width,font = loadFontAndGetDimensions(fontSize)
    output = np.zeros_like(img)
    pillow_output = Image.fromarray(output)
    pillow_drawer = ImageDraw.Draw(pillow_output)
    densityStringLen = len(densityString) - 1

    for i in range(int(image_height/font_height)):
        for j in range(int(image_width/font_width)):

            y_start = i * font_height
            x_start = j * font_width

            y_end = y_start + font_height
            x_end = x_start + font_width

            intensity = np.mean(img[y_start:y_end,x_start:x_end])
            intensityValue = int(intensity * densityStringLen/255)

            pillow_drawer.text((x_start,y_start),str(densityString[intensityValue]),font=font,fill=(255,255,255))

    output = np.array(pillow_output)
    return output

def pillowImagePrintColor(img,densityString= """.\'`^",:;Il!i<~+_-?[{1(|/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$""",fontSize = 15):
    # For Normal
    image_height,image_width,_ = img.shape
    font_height, font_width,font = loadFontAndGetDimensions(fontSize)
    output = np.zeros_like(img)
    pillow_output = Image.fromarray(output)
    pillow_drawer = ImageDraw.Draw(pillow_output)
    densityStringLen = len(densityString) - 1

    for i in range(int(image_height/font_height)):
        for j in range(int(image_width/font_width)):

            y_start = i * font_height
            x_start = j * font_width

            y_end = y_start + font_height
            x_end = x_start + font_width

            intensity = np.mean(img[y_start:y_end,x_start:x_end])
            intensityValue = int(intensity * densityStringLen/255)

            color = np.mean(img[y_start:y_end, x_start:x_end], axis = (0, 1)).astype(np.uint8)

            pillow_drawer.text((x_start,y_start),str(densityString[intensityValue]),font=font,fill=tuple(color))

    output = np.array(pillow_output)
    return output

def grayPillowImagePrintGray(img,densityString,font_height, font_width,font):
    # For grayscale
    image_height,image_width = img.shape
    # font_height, font_width,font = loadFontAndGetDimensions()
    output = np.zeros_like(img)
    pillow_output = Image.fromarray(output)
    pillow_drawer = ImageDraw.Draw(pillow_output)
    densityStringLen = len(densityString) - 1

    for i in range(int(image_height/font_height)):
        for j in range(int(image_width/font_width)):

            y_start = i * font_height
            x_start = j * font_width

            y_end = y_start + font_height
            x_end = x_start + font_width

            intensity = np.mean(img[y_start:y_end,x_start:x_end])
            intensityValue = int(intensity * densityStringLen/255)
            # print("Intensity"+str(intensity)+" index"+str(intensityValue))

            pillow_drawer.text((x_start,y_start),str(densityString[intensityValue]),font=font,fill=255)

    output = np.array(pillow_output)
    return output

def loadFontAndGetDimensions(fontSize = 15):
    # fontSize = 15
    if fontSize < 5:
        print("Warning: Font size too small , can cause infinite loop.")
        _ = input()
    FONT_PATH = "./secret_code/secrcode.ttf"
    font = ImageFont.truetype(FONT_PATH, fontSize)
    (left, top, right, bottom) = font.getbbox("$")
    # print(left,top,right,bottom)
    font_width = right - left + 0
    font_height = bottom - top + 0

    return font_height,font_width,font

def webcamGrayMode(densityString):
    font_height, font_width,font = loadFontAndGetDimensions()
    cap = cv.VideoCapture(0)
    if not cap.isOpened():
        print("Cannot open camera")
        exit()
    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()
        # if frame is read correctly ret is True
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            break
        # Our operations on the frame come here
        gray = pillowImagePrintGray(frame, densityString, font_height, font_width, font)
        # Display the resulting frame
        cv.imshow('frame', gray)
        if cv.waitKey(1) == ord('q'):
            break
    # When everything done, release the capture
    cap.release()
    cv.destroyAllWindows()

def webcamColorMode(densityString):
    font_height, font_width,font = loadFontAndGetDimensions()
    cap = cv.VideoCapture(0)
    if not cap.isOpened():
        print("Cannot open camera")
        exit()
    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()
        # if frame is read correctly ret is True
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            break
        # Our operations on the frame come here
        # frame = modifyContrastAndBrightness(frame,1,100)
        gray = pillowImagePrintColor(frame, densityString, font_height, font_width, font)
        # Display the resulting frame
        cv.imshow('frame', gray)
        if cv.waitKey(1) == ord('q'):
            break
    # When everything done, release the capture
    cap.release()
    cv.destroyAllWindows()

def modifyContrastAndBrightness(img,contrast = 1,brightness = 0):
    new_image = np.zeros(img.shape, img.dtype)
    for y in range(img.shape[0]):
        for x in range(img.shape[1]):
            for c in range(img.shape[2]):
                new_image[y, x, c] = np.clip(contrast * img[y, x, c] + brightness, 0, 255)

    return  new_image

if __name__ == '__main__':

    img = cv.imread("./assests/Lenna.png")
    # img = cv.imread("./assests/redfort.jpg")

    densityString = """.\'`^",:;Il!i<~+_-?[{1(|/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$"""
    font_height, font_width,font = loadFontAndGetDimensions()

    # output = pillowImagePrint(img,densityString)
    # output = pillowImagePrintGrey(img,densityString)
    #output = modifyContrastAndBrightness(img,3,100)
    #output = pillowImagePrintColor(img,densityString,font_height,font_width,font)

    #cv.imshow("Output", output)
    #cv.waitKey(0)

    # webcamGrayMode(densityString)
    webcamColorMode(densityString)
