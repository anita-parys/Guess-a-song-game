import cv2
import csv
import pandas as pd
import random
from cvzone.HandTrackingModule import HandDetector
import cvzone
import time
cap = cv2.VideoCapture(0)
cap.set(3,1280)
cap.set(4,720)
detector = HandDetector(detectionCon=0.8)

class Guess_song():
    def __init__(self, data):
        self.title = data[0]
        self.singer = data[1]
        self.userAns = None
    def update(self, cursor, bboxs):
        for x, bbox in enumerate(bboxs):
            x1,y1,x2,y2 = bbox
            if x1<cursor[0]<x2 and y1<cursor[1]<y2:
                self.userAns = x+1
                cv2.rectangle(img, (x1,y1), (x2,y2), (0,255,0), cv2.FILLED)


#import csv file data

pathCSV = "songs.csv"
with open(pathCSV, newline = '\n') as f:
    reader = csv.reader(f)
    dataAll = list(reader)[1:]


dataAll = random.sample(dataAll, 10)



#Create object
songList = []
for q in dataAll:
    songList.append(Guess_song(q))

qNo = 0
l=0
qTotal = len(dataAll)



while True:
    success, img = cap.read()
    img = cv2.flip(img,1)
    hands, img = detector.findHands(img, flipType=False)
    if qNo<qTotal:
        #qNo = random.randrange(0, qTotal)
        song = songList[qNo]



        img, bbox = cvzone.putTextRect(img, "Singer", [330, 70], 2, 2, offset=20, colorR= (185, 93, 58))
        img, bbox1 = cvzone.putTextRect(img, "Title", [900, 70], 2, 2, offset=20, colorR= (185, 93, 58))
        img, bbox2 = cvzone.putTextRect(img, song.singer, [200, 170], 2, 2, offset=40,colorR= (222, 203, 131))
        img, bbox3 = cvzone.putTextRect(img, song.title, [780, 170], 2, 2, offset=40, colorR= (222, 203, 131))
        img, bbox4 = cvzone.putTextRect(img, "Correct", [200, 400], 2, 2, offset=40, colorR= (0,255,0))
        img, bbox5 = cvzone.putTextRect(img, "Next", [1000, 400], 2, 2, offset=40, colorR= (0,0,255))

        if hands:
            lmList = hands[0]['lmList']
            cursor = lmList[8]
            length, info = detector.findDistance(lmList[8], lmList[12])
            if length < 50:
                song.update(cursor, [bbox4, bbox5])
                if song.userAns is not None:
                    time.sleep(1)
                    qNo = qNo+1

    else:
        score = 0
        for song in songList:
            if song.userAns == 1:
                score += 1
        #score = round((score/qTotal) * 100,2)
        img, _ = cvzone.putTextRect(img, "Game Over", [250,300], 2, 2, offset = 50, border = 5)
        img, _ = cvzone.putTextRect(img, f'your score: {score}/10', [700,300], 2, 2, offset = 16, border = 5)


     #Draw Progress Bar
    barValue = 150 + (950//10)*qNo
    cv2.rectangle(img, (150,600), (barValue,650), (0,255,0), cv2.FILLED)
    cv2.rectangle(img, (150, 600), (1100, 650), (255, 0, 255), 5)
    img, _ = cvzone.putTextRect(img, f'{(round((qNo/10)*100))}%', [1130, 635], 2, 2, offset=16)

    cv2.imshow("image", img)
    cv2.waitKey(1)
