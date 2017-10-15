import numpy as np
import cv2
from flask import Flask, Response
import json
import random
cs = []
ages = [ x for x in range(20,40)]
probs = [1]*20
Ages = []
Genders = []
maxvisitors = 0
def inside(r, q):
    rx, ry, rw, rh = r
    qx, qy, qw, qh = q
    return rx > qx and ry > qy and rx + rw < qx + qw and ry + rh < qy + qh

def draw_detections(img, rects, thickness = 1):
	global cs
	for x, y, w, h in rects:
		# the HOG detector returns slightly larger rectangles than the real objects.
		# so we slightly shrink the rectangles to get a nicer output.
		pad_w, pad_h = int(0.15*w), int(0.05 * h)
		cv2.rectangle(img, (x+pad_w, y+pad_h), (x+w-pad_w, y+h-pad_h), (0, 255, 0), thickness)
		cs.append(     (  ((x+w-pad_w)+(x+pad_w))/2,    ((y+h-pad_h)+(y+pad_h))/2   )        )

	for c in cs:
		overlay = img.copy()
		output = img.copy()
		cv2.circle(overlay, c,10,(5,231,252),-1)
		alpha = 0.05
		cv2.addWeighted(overlay, alpha, img, 1 - alpha,0, img)


def GetGenders(frame):
    return np.random.choice([1 , 0],p=[0.7,0.3])
def GetAges(frame):
    return random.randint(20,41)
if __name__ == '__main__':
    live_visitors = 0
    hog = cv2.HOGDescriptor()
    hog.setSVMDetector( cv2.HOGDescriptor_getDefaultPeopleDetector() )
    cap=cv2.VideoCapture(0)
    post_frame = cap.get(cv2.CAP_PROP_POS_FRAMES)
    print(post_frame)
    # break
    w=int(cap.get(cv2.CAP_PROP_FRAME_WIDTH ))
    h=int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT ))
    # fourcc = cv2.VideoWriter_fourcc(*'XVID') 
    # out = cv2.VideoWriter("output.avi", fourcc, 20, (w,h))
    
    # cap = cv2.VideoCapture(0)
    count = 0
    # app = Flask(__name__)        
    # app.run(host='localhost', port=5000)
    
    while True:
    	count += 1
      
        ret,frame=cap.read()
        found,w=hog.detectMultiScale(frame, winStride=(8,8), padding=(32,32), scale=1.05)
        visitors = []
        for detected in found:
            a,b,c,d = detected
            if(a > 90 and a <110  and b > 50 and b <110 and  c < 170 and c >130 and d >250 and d  < 310 ):
                continue
            else:
                # print(detected)
                visitors.append(detected)

        live_visitors = len(visitors)
        if(maxvisitors < live_visitors):
            for face in range(int(live_visitors - maxvisitors)):
                Ages.append(GetAges(frame))
                Genders.append(GetGenders(frame))
            maxvisitors = live_visitors

            
        datastore={}
        with open('data.json','r') as f:
            datastore=json.load(f)
        with open('data.json','w') as f:
            datastore["people"] = live_visitors
            datastore["Ages"] = Ages[0:live_visitors]
            datastore["Genders"] = Genders[0:live_visitors]
            json.dump(datastore,f)
        
        # print(live_visitors)
        draw_detections(frame,visitors)
        # print out.write(frame)
        cv2.imshow('feed',frame)
        cv2.imwrite("../advertiseserverweb/public/images.png", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            out.release()
            break

    cv2.destroyAllWindows()
    cap.release()
    out.release()