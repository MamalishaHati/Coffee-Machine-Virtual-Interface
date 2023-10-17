# Main.py
import os
from cvzone.HandTrackingModule import HandDetector
import cv2

cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

imgbackround = cv2.imread("Resources/Background.png")

# importing  all the mode images to a list
folderPathModes = "Resources/Modes"
listImgModesPath = os.listdir(folderPathModes)
listImgModes = []
for imgModePath in listImgModesPath:
    listImgModes.append(cv2.imread(os.path.join(folderPathModes, imgModePath)))
print(listImgModes)

# importing all the icons to a list

folderPathIcons = "Resources/Icons"
listImgIconPath = os.listdir(folderPathIcons)
listImgIcons = []
for imgIconsPath in listImgIconPath:
    listImgIcons.append(cv2.imread(os.path.join(folderPathIcons, imgIconsPath)))
print(listImgIcons)

modetype = 0  # for changing selection mode
selection = -1
counter = 0
selectionSpeed = 5

detector = HandDetector(detectionCon=0.8, maxHands=1)  # using for hand detection
modePositions = [(1136, 196), (1000, 384), (1136, 581)]
counterPause = 0
selectionList = [-1, -1, -1]

while True:
    success, img = cap.read()

    # find the hand and its landmarks
    hands, img = detector.findHands(img)  # with draw

    # overlaying the webcam feed on the background image
    imgbackround[139:139 + 480:, 50:50 + 640] = img
    imgbackround[0:720, 847:1280] = listImgModes[modetype]  #

    if hands and counterPause == 0 and modetype < 3:
        # Hand 1
        hand1 = hands[0]
        fingers1 = detector.fingersUp(hand1)
        print(fingers1)

        if fingers1 == [0, 1, 0, 0, 0]:
            if selection != 1:
                counter = 1
            selection = 1

        elif fingers1 == [0, 1, 1, 0, 0]:
            if selection != 2:
                counter = 1
            selection = 2

        elif fingers1 == [0, 1, 1, 1, 0]:
            if selection != 3:
                counter = 1
            selection = 3
        else:
            selection = -1
            counter = 0
        if counter > 0:
            counter += 1
            print(counter)

            cv2.ellipse(imgbackround, modePositions[selection - 1], (103, 103), 0, 0, counter * selectionSpeed
                        , (0, 255, 0), 20)
            if counter * selectionSpeed > 360:
                selectionList[modetype] = selection
                modetype += 1
                counter = 0
                selection = -1
                counterPause = 1

    if counterPause > 0:  # to stop after  1st each selection is made
        counterPause += 1
        if counterPause > 60:
            counterPause = 0
    # add selection icon at the bottom
    if selectionList[0] != -1:
        imgbackround[636:636 + 65, 133:133 + 65] = listImgIcons[selectionList[0] - 1]
    if selectionList[1] != -1:
        imgbackround[636:636 + 65, 340:340 + 65] = listImgIcons[2 + selectionList[1]]
    if selectionList[2] != -1:
        imgbackround[636:636 + 65, 542:542 + 65] = listImgIcons[5 + selectionList[2]]

    # displaying the image
    # cv2.imshow("Image",img)
    cv2.imshow("Background", imgbackround)
    cv2.waitKey(1)
