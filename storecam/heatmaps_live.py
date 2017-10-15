import numpy as np
import cv2, requests, json, gender_detect, age_detect

def send_request(age, gender):
    url = 'https://eagleeye123.firebaseio.com/data.json'
    nop = 1 #increment by x everytime a new person comes in

    response = requests.get(url)

    gender_count = json.loads(response.text)[gender]
    age_count = json.loads(response.text)[age]

    gender_string = '"' + str(gender) + '"'
    age_string = '"' + str(age) + '"'


    data_gender = '{' + gender_string + ':' + str(gender_count+1) + '}'
    data_age = '{' + age_string + ':' + str(age_count+1) + '}'


    response_gender = requests.patch(url, data=data_gender)
    response_age = requests.patch(url, data=data_age)


    print json.loads(requests.get(url).text)["fa1"]


if __name__ == '__main__':    
    cap = cv2.VideoCapture(0)                       #video record code
    facedata = "haarcascade_frontalface_default.xml" #process code
    cascade = cv2.CascadeClassifier(facedata)

    ret, frame = cap.read()
    count = 0

    
    while(ret):
        count += 1                                      #record code
        img = frame
        if count % 50 == 0:
            print count

            minisize = (img.shape[1],img.shape[0])       #video code
            miniframe = cv2.resize(img, minisize)
     
            faces = cascade.detectMultiScale(miniframe)

            for f in faces:
            
                x, y, w, h = [ v for v in f ]
                
                cv2.rectangle(img, (x,y), (x+w,y+h), (255,255,255))
     
                sub_face = img[y:y+h, x:x+w]
                cv2.imshow('sub_face',sub_face)
                cv2.waitKey(1)
                send_request(age_detect(sub_face), gender_detect(sub_face))
                
                
                sub_gray = cv2.cvtColor(sub_face, cv2.COLOR_BGR2GRAY)
            
        cv2.imshow('frame',img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        ret, frame = cap.read()
        
    cap.release()
    cv2.destroyAllWindows()
    

    #while(True):
        #key = cv2.waitKey(20)
        #if key in [27, ord('Q'), ord('q')]:
            #break