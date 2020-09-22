from flask import Flask, render_template
import tkinter
from tkinter import filedialog
import os
import numpy as np 
import cv2 
import imutils 
import datetime 

app=Flask(__name__)

@app.route('/')
def home():
    app.route('/')
    return render_template("home.html")

@app.route('/about/')
def about():
    return render_template("about.html")


@app.route('/json')
def json():
    return render_template('json.html')

#background process happening without any refreshing
@app.route('/background_process_test')
def background_process_test():
    print ("Hello")
    # root = tkinter.Tk()
    # root.withdraw() #use to hide tkinter window
    

    # def search_for_file_path ():
    #     currdir = os.getcwd()
    #     tempdir = filedialog.askdirectory(parent=root, initialdir=currdir, title='Please select a directory')
    #     if len(tempdir) > 0:
    #         print ("You chose: %s" % tempdir)
    #     return tempdir

    # file_path_variable = search_for_file_path()
    # print ("\nfile_path_variable = ", file_path_variable)
    # main_win = tkinter.Tk()
    # main_win.withdraw()
    #
    # main_win.overrideredirect(True)
    # main_win.geometry('0x0+0+0')
    #
    # main_win.deiconify()
    # main_win.lift()
    # main_win.focus_force()
    #
    # #open file selector
    # main_win.sourceFile = filedialog.askopenfilename(parent=main_win, initialdir= "/",
    # title='Please select a directory')
    #
    # #close window after selection
    # main_win.destroy()
    #
    # #print path
    # print('testing file')
    # print(main_win.sourceFile)
    gun_cascade = cv2.CascadeClassifier('cascade.xml') 
    # camera = cv2.VideoCapture(0)
    #path = main_win.sourceFile
    path = '/home/developer/sibghat/flask_Demo/FLIR_THERMAL IR ELLIOT.mp4'
    camera = cv2.VideoCapture(path) #grey video
    # camera = cv2.VideoCapture('flir_ELLIOT RAINBOW(1).mp4') # rainbow video
    # camera = cv2.VideoCapture('FLIR THERMAL 4K.mp4') # normal video

    firstFrame = None
    gun_exist = False

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

        #cv2. ("Security Feed", frame)
        key = cv2.waitKey(1) & 0xFF

        if key == ord('q'): 
            break

        if gun_exist: 
            print("guns detected") 
        else: 
            print("guns NOT detected") 

    camera.release() 
    cv2.destroyAllWindows() 

if __name__=="__main__":
    app.run(debug=True)
