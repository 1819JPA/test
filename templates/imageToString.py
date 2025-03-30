# gets player info and image by calling methods from imageCapture.py
# converts the image into String
# returns player info and string from the image
from PIL import Image
from pytesseract import pytesseract
import imageCapture


def convertImagetoString():
    images=imageCapture.captureNames()
    names=[]
    for image in images:
        names.append(convertImagetoStringHelper(image))
    return names

def convertImagetoStringHelper(image):
    path_to_tesseract = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    pytesseract.tesseract_cmd = path_to_tesseract
    text=pytesseract.image_to_string(image)
    return text[:-1]

# image=Image.open("resource\\test1.PNG")
# print(convertImagetoString)
# print(convertImagetoString())