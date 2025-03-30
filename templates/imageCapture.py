import pyautogui
import time
import cv2
import numpy as np
# Captures images for each champion's name, like Octoberfest Gragas, for each player in loading screen
# return some data with image information and player information, perhaps in a tuple (player,image)
# Example: (top1, image_top1) would mean top player from team 1, and its corresponding image
# could continue like top1,top2,jg1,jg2,mid1,mid2,adc1,adc2,sup1,sup2


# calls captureImage 10 times to capture 
def captureNames():
    images=[]
    x=242 #x coordinate for leftmost champion name
    y=400 #y coordinate for top team champions' names
    width=250 #width of name
    height=20 #height of name
    for i in range(5):
        images.append(captureImage(x,y,width,height))
        x+=296
    y=935 #set y coordinate for bottom team names
    x=242 #reset x coordinate to face leftmost champion
    for i in range(5):
        images.append(captureImage(x,y,width,height))
        x+=296
    return images

def captureImage(x,y,width,height):
    return pyautogui.screenshot(region=(x,y,width,height))

def isTopMyTeam():
    images=[]
    x=285
    y=485
    width=165
    height=10
    for i in range(5):
        images.append(captureImage(x,y,width,height))
        x+=296
    for image in images:
        image.save(r"resource\player.jpg")
        image=cv2.imread(r"resource\player.jpg")
        lower=np.array([47,178,228])
        upper=np.array([55,186,236])
        yellows=cv2.inRange(image,lower,upper)
        pixels = cv2.countNonZero(yellows)
        if pixels>0:
            return True
    return False

def whatLaneAmI():
    images=[]
    x=285
    y=485
    width=165
    height=10
    for i in range(5):
        images.append(captureImage(x,y,width,height))
        x+=296
    for i in range(5):
        images[i].save(r"resource\player.jpg")
        images[i]=cv2.imread(r"resource\player.jpg")
        lower=np.array([47,178,228])
        upper=np.array([55,186,236])
        yellows=cv2.inRange(images[i],lower,upper)
        pixels = cv2.countNonZero(yellows)
        if pixels>0:
            return getLaneInfoString(i)
    images.clear()
    x=285
    y = 1020
    for i in range(5):
        images.append(captureImage(x,y,width,height))
        x+=296
    for i in range(5):
        images[i].save(r"resource\player.jpg")
        images[i]=cv2.imread(r"resource\player.jpg")
        lower=np.array([47,178,228])
        upper=np.array([55,186,236])
        yellows=cv2.inRange(images[i],lower,upper)
        pixels = cv2.countNonZero(yellows)
        if pixels>0:
            return getLaneInfoString(i)
    return "error"

def getLaneInfoString(i):
    lane=""
    if i == 0:
        lane = "top"
    elif i == 1:
        lane = "jungle"
    elif i == 2:
        lane = "mid"
    elif i == 3:
        lane = "adc"
    else:
        lane = "support"
    return lane

if __name__ == "__main__":
    time.sleep(2)
    print(whatLaneAmI())
    
