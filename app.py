from flask import Flask, render_template, request, redirect, url_for
import tkinter
from tkinter import filedialog
# from werkzeug import secure_filename
from flask import send_file
from zipfile import ZipFile

import os
import numpy as np 
import cv2 
import imutils 
import datetime 




# app=Flask(__name__)
app = Flask(__name__, static_folder='static')

# @app.route('/')
# def home():
#     app.route('/')
#     return render_template("home.html")

# @app.route('/about/')
# def about():
#     return render_template("about.html")

# @app.route('/player')
# def player():
#     video = request.args.get("video")

#     return render_template('player.html',video=video)



@app.route('/home')
def json():
    return render_template('home.html')

#background process happening without any refreshing
@app.route('/background_process_test',  methods = ['GET', 'POST'])
def background_process_test():
    print ("Hello")
    
    # return redirect(url_for('player', video='your_video123.avi'))
    if request.method == 'POST':
        f = request.files['file']
        x=1
        f.save('static/uploaded_file.mp4')

    gun_cascade = cv2.CascadeClassifier('cascade.xml') 
    # camera = cv2.VideoCapture(0)
    #path = main_win.sourceFile
    path = 'static/uploaded_file.mp4'
    camera = cv2.VideoCapture(path) #grey video
    # camera = cv2.VideoCapture('flir_ELLIOT RAINBOW(1).mp4') # rainbow video
    # camera = cv2.VideoCapture('FLIR THERMAL 4K.mp4') # normal video
    # out = cv2.VideoWriter('uploaded_file_detected.mp4', -1, 20.0, (640, 480))
    width = int(camera.get(cv2.CAP_PROP_FRAME_WIDTH) + 0.5)
    height = int(camera.get(cv2.CAP_PROP_FRAME_HEIGHT) + 0.5)
    size = (width, height)
    fourcc = cv2.VideoWriter_fourcc(*'MJPG')
    out = cv2.VideoWriter('static/your_video1235.avi', fourcc, 20.0, size)
    outFile = open("static/detection_logs.txt", "w")
    outFile.close()
    # print('out')
    # print(out)
    # con_video = os.popen("ffmpeg -i {input} -ac 2 -b:v 2000k -c:a aac -c:v libx264 -b:a 160k -vprofile high -bf 0 -strict experimental -f mp4 {output}.mp4".format(input = out, output = 'y_video'))
    firstFrame = None
    gun_exist = False
    
    try:
        while True:

            ret, frame = camera.read()

            frame = imutils.resize(frame, width = 500)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            gun = gun_cascade.detectMultiScale(gray,
                                            1.3, 5,
                                            minSize = (100, 100))

            if len(gun) > 0:
                gun_exist = True

            for (x, y, w, h) in gun:

                frame = cv2.rectangle(frame,
                                    (x, y),
                                    (x + w, y + h),
                                    (255, 0, 0), 2)
                roi_gray = gray[y:y + h, x:x + w]
                roi_color = frame[y:y + h, x:x + w]

            if firstFrame is None:
                firstFrame = gray
                continue

            # print(datetime.date(2019))
            # draw the text and timestamp on the frame
            cv2.putText(frame, datetime.datetime.now().strftime("% A % d % B % Y % I:% M:% S % p"),
                        (10, frame.shape[0] - 10),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.35, (0, 0, 255), 1)

            #cv2.imshow("Security Feed", frame)
            out.write(cv2.resize(frame, size ))
            key = cv2.waitKey(1) & 0xFF

            if key == ord('q'):
                break
            if gun_exist:
                outFile = open("static/detection_logs.txt", "a")
                outFile.write('guns detected at: '+ str(datetime.datetime.now()))
                outFile.write("\n")
                outFile.close()
                print('guns detected' + str(datetime.datetime.now()))
            else:
                outFile = open("static/detection_logs.txt", "a")
                outFile.write('guns NOT detected' + str(datetime.datetime.now()))
                outFile.write("\n")
                outFile.close()
                print('guns NOT detected' + str(datetime.datetime.now()))
            
    except:
        pass

    
    zipObj = ZipFile('detection_log_vid.zip', 'w')
    # Add multiple files to the zip
    zipObj.write('static/detection_logs.txt')
    zipObj.write('static/your_video1235.avi')
    # close the Zip File
    zipObj.close()
    print('*** Create a zip file from multiple files using with ')
    # Create a ZipFile Object
    out.release()
    camera.release()

    cv2.destroyAllWindows()
    # return redirect(url_for('player', video='your_video1235.mp4'))
    # return redirect('/static/your_video1235.avi')
    path = "detection_log_vid.zip"
    return send_file(path, as_attachment=True)
    # return "your_video1235.avi"

if __name__=="__main__":
    app.run('0.0.0.0', port='8000', debug=True)
