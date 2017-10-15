#identifies people on a cctv cam footage
import numpy as np
import cv2, time, requests, random, json

def inside(r, q):
    rx, ry, rw, rh = r
    qx, qy, qw, qh = q
    return rx > qx and ry > qy and rx + rw < qx + qw and ry + rh < qy + qh


def draw_detections(img, rects, thickness = 1):
    for x, y, w, h in rects:
        # the HOG detector returns slightly larger rectangles than the real objects.
        # so we slightly shrink the rectangles to get a nicer output.
        pad_w, pad_h = int(0.15*w), int(0.05*h)
        cv2.rectangle(img, (x+pad_w, y+pad_h), (x+w-pad_w, y+h-pad_h), (0, 255, 0), thickness)

def send_request(age, gender):
    url = 'https://eagleeye123.firebaseio.com/data.json'
    nop = 1 #increment by x everytime a new person comes in

    response = requests.get(url)

    gender_count = json.loads(response.text)[gender]
    age_count = json.loads(response.text)[age]
    nop_count = json.loads(response.text)["nop"]
    fa1_count = json.loads(response.text)["fa1"]

    gender_string = '"' + str(gender) + '"'
    age_string = '"' + str(age) + '"'
    nop_string = '"' + "nop" + '"'
    # fa1_string = '"' + str(age) + '"'

    data_gender = '{' + gender_string + ':' + str(gender_count+1) + '}'
    data_age = '{' + age_string + ':' + str(age_count+1) + '}'
    data_nop = '{' + nop_string + ':' + str(nop_count+1) + '}'
    data_fa1 = {}
    data_fa1["fa1"] = fa1_count;
    data_fa1["fa1"][6] += 1


    response_gender = requests.patch(url, data=data_gender)
    response_age = requests.patch(url, data=data_age)
    response_nop = requests.patch(url, data=data_nop)
    response_fa1 = requests.patch(url, data=json.dumps(data_fa1))

    print json.loads(requests.get(url).text)["fa1"]

    #young #adult #elderly

    # fa 1 week
    # fa 2 month
    # fa 3 time 

 

cap = cv2.VideoCapture('ftw2.mp4')                        #video record code
# facedata = "haarcascade_frontalface_default.xml" #face detect haar casscade training data
facedata = "haarcascade_upperbody.xml" 
cascade = cv2.CascadeClassifier(facedata)        #training the classififer

ret, frame = cap.read()                          #read data from input stream

count = 0

#while frames get retrieved successfuly
while(ret):  
    print count
    count +=1
    img = frame
    # if count%4 == 0:
    if count == 8 or count == 56 or count == 88:
        
        
        # minisize = (img.shape[1],img.shape[0])       #video code
        # miniframe = cv2.resize(img, minisize)
        
        miniframe = img
        faces = cascade.detectMultiScale(miniframe)
        
        for f in faces:
        
            x, y, w, h = [ v for v in f ]
            
            cv2.rectangle(img, (x,y), (x+w,y+h), (255,255,255))
            # text_color = (255,255,255)
            # cv2.putText(img, "Gender: Male", (x+w,y+15), cv2.FONT_HERSHEY_PLAIN, 1.0, text_color, thickness=2)
            # cv2.putText(img, "Age: 16-25", (x+w,y+30), cv2.FONT_HERSHEY_PLAIN, 1.0, text_color, thickness=2)
            # cv2.putText(img, "Height: 6 feet", (x+w,y+45), cv2.FONT_HERSHEY_PLAIN, 1.0, text_color, thickness=2)
 
            sub_face = img[y:y+h, x:x+w]

            
        
        print count


            
    cv2.imshow('img', img)
    if cv2.waitKey(100) & 0xFF == ord('q'):
        break
    ret, frame = cap.read()


cap.release()
cv2.destroyAllWindows()