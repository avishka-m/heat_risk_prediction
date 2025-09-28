from flask import Flask , render_template, request
import joblib
import os 
import cv2


BASE_DIR = os.path.dirname(__file__)
model_path = os.path.join(BASE_DIR, "svm_face_recognisation.sav")

model = joblib.load(model_path)

category_dict={0:'Avishka',1:"Dulanga",2:"Iduwara",3:"Isuru"}

app=Flask(__name__)

@app.route('/')
def index():
    return render_template('patient_details.html')

@app.route('/getresults', methods=['post'])
def getresults():
    result = request.form
    print(result)
    return('results printed')

@app.route('/face')
def face():
    face_classifire = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

    # test_img_names = os.listdir(test_data_path)

    source = cv2.VideoCapture(0)


    while(True):
    # for test_img in test_img_names:
        # img_path = os.path.join(test_data_path,test_img) 
        # test_img = cv2.imread(img_path)

        ret,img = source.read()

        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

        faces = face_classifire.detectMultiScale(gray)
        for (x,y,w,h) in faces:
            cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)

            croped_face = gray[y:y+h,x:x+w]
            croped_face = cv2.resize(croped_face,(50,50))
            croped_original = croped_face
            croped_face = croped_face.reshape(1,50*50)

            result = model.predict(croped_face)
            name = category_dict[result[0]]

            cv2.putText(img,name,(x,y-10),cv2.FONT_HERSHEY_SIMPLEX,1.5,(255,0,0),2)
            cv2.imshow('GRAY',croped_original) 
        cv2.imshow("IVE", img)

        k = cv2.waitKey(10)
        if(k==27):
            break

    cv2.destroyAllWindows()


app.run(debug=True)