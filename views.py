from flask import Flask, request, render_template, redirect, url_for, Response
#from webapp.main import app
import cv2
import time
import face_recognition
#from selenium import webdriver
#from selenium.webdriver.common.keys import Keys
#PATH = 'C:\Program Files (x86)\chromedriver.exe'


app = Flask(__name__)

rec_name = 'default'
          
@app.route('/',methods=['GET'])
@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/start_cam', methods=['POST'])
def start_cam():
    if request.method == 'POST':
        return redirect(url_for('index'))
    #return render_template('home.html', start_cam = "yes")

@app.route('/stop_cam', methods=['POST'])
def stop_cam():
    if request.method == 'GET':
        return redirect((url_for('home')))
    if request.method == 'POST':
        return Response(gen_frames(True), mimetype='multipart/x-mixed-replace; boundary=frame'), {"Refresh": "0.01; url=home"}
        #yield '<script>document.location.href="http://127.0.0.1:5000/home"</script>'
    #return render_template('home')

@app.route('/video_feed',methods=['GET','POST'])
def video_feed():
    #camera = cv2.VideoCapture(0)
    def gen_frames(stop):
            
        myFace = cv2.imread("C:/Users/91901/webapp/image.jpg")

        myEncoding = face_recognition.face_encodings(myFace)[0]



        trainEncodings=[myEncoding]
        #print(trainEncodings)
        Names=['Ram Sreekar']
        ####Testing####
        cam = cv2.VideoCapture(0) #referencing the webcam
        while True:
            if stop:
                cv2.destroyAllWindows()
                cam.release()
                stop = False
                print('\nstopped\n')
                break
            ret,testImage=cam.read()
            facePositions=face_recognition.face_locations(testImage)
            #print(facePositions)
            if not ret:
                print('\nNot Success\n')
                break
            else:
                testEncodings=face_recognition.face_encodings(testImage,facePositions)
                for (top,left,bottom,right),face_encoding in zip(facePositions,testEncodings):
                    name='Unknown' #By default identified will be unknows
                    matches=face_recognition.compare_faces(trainEncodings,face_encoding)

                    if True in matches:
                        global rec_name
                        print(matches)
                        i=matches.index(True)
                        name=Names[i]
                        rec_name = name
                        #cv2.waitkey(0)
                        #query = Names[i]
                        #chrome_path = r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe %s'
                        #for url in search(query,1):
                            #webbrowser.open("https://google.com/search?q=%s" % query)

                    cv2.rectangle(testImage,(left,top),(right,bottom),(0,0,255),2)
                    cv2.putText(testImage,name,(left-50,top-10),cv2.FONT_HERSHEY_SIMPLEX,.75,(255,0,0),1)
                    matches[i] = False
                #cv2.imshow("Output",testImage)
                ret2, buffer = cv2.imencode('.jpg', testImage)
                frame = buffer.tobytes()
                
                yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n') 
                
                

    if request.method == 'GET':
        return Response(gen_frames(False), mimetype='multipart/x-mixed-replace; boundary=frame')
    if request.method == 'POST':
        return Response(gen_frames(True), mimetype='multipart/x-mixed-replace; boundary=frame'), {"Refresh": "0.05; url=search"}
        #return redirect('index')
    #return render_template('index.html')

@app.route('/search/', methods=['GET','POST'])
def search():
    if request.method == 'GET':
        return render_template('search.html',rec_name=rec_name)
    if request.method == 'POST':
        #driver = webdriver.Chrome(PATH)
        #url1 = "https://www.linkedin.com/public-profile/in/prince-jhonson-bb9418207"
        #url2 = "https://www.instagram.com/{rec_name}/"
        return render_template('search.html'), {"Refresh": f"0.05; url=https://www.instagram.com/{rec_name}/"}

if __name__ == '__main__':
    app.run(debug=True)

