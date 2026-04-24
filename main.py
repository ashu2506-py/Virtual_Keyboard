import cv2
import cvzone

from pynput.keyboard import Controller

kb = Controller()
from cvzone.HandTrackingModule import HandDetector
detector=HandDetector(0.5)
cap=cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4,480)



kb = Controller()
def drawAll(img,buttonList):
    for button in buttonList:
        x,y=button.pos
        w,h=button.size
        cvzone.cornerRect(img,(button.pos[0],button.pos[1],button.size[0],button.size[1]),20,rt=0)
        cv2.rectangle(img,button.pos,(x+w,y+h),(0,255,105),cv2.FILLED)
        cv2.putText(img,button.text,(x+40,y+65),cv2.FONT_HERSHEY_SIMPLEX,2,(255,255,255),4)

    return img


class Button():
    def __init__(self,pos,text,size=[85,85]):
        self.pos=pos
        self.text=text
        self.size=size

keys=[["Q","W","E","R","T","Y","U","I","O","P"],
      ["A","S","D","F","G","H","J","K","L",";"],
      ["Z","X","C","V","B","N","M",",",".","/"]]


buttonList=[]
for i in range(len(keys)):
    for j,key in enumerate(keys[i]):
        buttonList.append(Button([100*j+50,100*i+50],key))

while True:
    ret,img=cap.read()
    hands, img = detector.findHands(img)

    if hands:
        hand = hands[0]
        lmList = hand["lmList"]


        l, _, _ = detector.findDistance(lmList[8][:2], lmList[12][:2], img)

        for button in buttonList:
            x, y = button.pos
            w, h = button.size

            # hover
            if x < lmList[8][0] < x + w and y < lmList[8][1] < y + h:
                cv2.rectangle(img, (x - 5, y - 5), (x + w + 5, y + h + 5), (175, 175, 175), cv2.FILLED)

                # click
                if l < 50:
                    kb.press(button.text)
                    kb.release(button.text)
                    cv2.rectangle(img, button.pos, (x + w, y + h), (255, 0, 0), cv2.FILLED)
                    cv2.putText(img, button.text, (x + 20, y + 65),
                                cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 2)




    img=drawAll(img,buttonList)
    cv2.imshow('frame',img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()