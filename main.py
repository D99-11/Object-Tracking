import cv2
import time
import math

gx,gy = 530,300

ballPosX = []
ballPosY = []

video = cv2.VideoCapture("bb3.mp4")

# Load tracker 
tracker = cv2.TrackerCSRT_create()

# Read the first frame of the video
returned, img = video.read()

# Select the bounding box on the image
bbox = cv2.selectROI("Tracking", img, False)

# Initialise the tracker on the img and the bounding box
tracker.init(img, bbox)

print(bbox)

def drawBox(img, bbox):
    x, y, w, h = int(bbox[0]), int(bbox[1]), int(bbox[2]), int(bbox[3])
    
    cv2.rectangle(img,(x,y),((x+w),(y+h)),(255,0,255),3,1)


    cv2.putText(img,"Tracking",(75,90),cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,255,0),2)

def goal_track(img, bbox):
    x, y,w, h = int(bbox[0]),int(bbox[1]),int(bbox[2]),int(bbox[3])
    midX = x + int(w/2)
    midY = y + int(h/2)
    cv2.circle(img,(midX,midY),2,(245,52,89),7)
    cv2.circle(img,(gx,gy),3,(234,34,137),10)

    ballPosX.append(midX)
    ballPosY.append(midY)

    if(math.sqrt(((midX-gx)**2)+(midY-gy)**2) < 20):
            cv2.putText(img,"GOAL",(500,90),cv2.FONT_HERSHEY_SIMPLEX,2,(0,255,0),4)
    
    for x in range(len(ballPosX)-1):
        cv2.circle(img,(ballPosX[x],ballPosY[x]),3,(255,0,0),8)




while True:
    
    check, img = video.read()   

    # Update the tracker on the img and the bounding box
    success, bbox = tracker.update(img)

    if success:
        drawBox(img, bbox)
        
    else:
        cv2.putText(img,"Lost",(75,90),cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,0,255),2)

    goal_track(img,bbox)



    #################
    # ADD CODE HERE #
    #################

    cv2.imshow("result", img)
            
    key = cv2.waitKey(25)
    if key == 32:
        print("Stopped")
        break

video.release()
cv2.destroyALLwindows()