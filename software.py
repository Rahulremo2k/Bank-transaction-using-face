from imutils import paths
import numpy
import argparse
import imutils
import pickle
from cv2 import cv2
import os
import sys
from os import listdir, name
from os.path import isfile, join
from pathlib import Path
from collections import Counter
# import the necessary packages
from sklearn.preprocessing import LabelEncoder
from sklearn.svm import SVC
from imutils.video import VideoStream
from imutils.video import FPS
import time
from tkinter import *
from tkinter import messagebox
import sqlite3
import pandas as pd
from PIL import Image, ImageTk
import tkinter as tk
import pandas as pd


ARIAL = ("arial",10,"bold")
TIMES=("Times",10,"bold italic")

class BankUi:
    def __init__(self,root):
        self.root = root
        self.header = Label(self.root,text="SRM Valliammai Bank",bg="#000000",fg="white",font=("arial",20,"bold"))
        self.header.pack(fill=X)
        self.frame = Frame(self.root,bg="#ffffff",width=900,height=600)
        root.geometry("900x600")
        self.button1 = Button(self.frame,text="Click to begin transactions",bg="#3372de",fg="white",font=ARIAL,command = self.begin_page)
        self.q = Button(self.frame, text="Quit", bg="#3372de", fg="white", font=ARIAL, command=self.root.destroy)
        self.q.place(x=360, y=440, width=150, height=40)
        self.button1.place(x=230,y=340,width=400,height=36)
        self.countter = 2
        self.frame.pack()
   
    def begin_page(self):
        self.frame.destroy()
        self.frame = Frame(self.root,bg="#ffffff",width=900,height=600)
        root.geometry("900x600")
        self.enroll = Button(self.frame, text="Enroll",bg="#3372de",fg="white",font=ARIAL,command=self.enroll_user)
        self.transaction = Button(self.frame, text="Transaction",bg="#3372de",fg="white",font=ARIAL,command=self.video_check)
        self.q = Button(self.frame, text="Quit", bg="#3372de", fg="white", font=ARIAL, command=self.root.destroy)
        self.enroll.place(x=360, y=240, width=200, height=50)
        self.transaction.place(x=360, y=340, width=200, height=50)
        self.q.place(x=390, y=440, width=130, height=30)
        self.frame.pack()

    def enroll_user(self):
        self.frame.destroy()
        self.frame = Frame(self.root,bg="#ffffff",width=900,height=600)
        #Login Page Form Components
        self.userlabel =Label(self.frame,text="Name",bg="#ffffff",fg="black",font=ARIAL)
        self.uentry = Entry(self.frame,bg="#ffffff",highlightcolor="#c3c7c7",
           highlightthickness=2,
            highlightbackground="white")
        self.plabel = Label(self.frame, text="PIN",bg="#ffffff",fg="black",font=ARIAL)
        self.pentry = Entry(self.frame,bg="#ffffff",show="*",highlightcolor="#c3c7c7",
           highlightthickness=2,
            highlightbackground="white")  
        self.button1 = Button(self.frame,text="Next",bg="#3372de",fg="white",font=ARIAL,command = self.enroll_and_move_to_next_screen)
        self.q = Button(self.frame,text="Quit",bg="#3372de",fg="white",font=ARIAL,command = self.root.destroy)
        self.b = Button(self.frame,text="Back",bg="#3372de",fg="white",font=ARIAL,command = self.begin_page)
        self.userlabel.place(x=125,y=100,width=120,height=20)
        self.uentry.place(x=180,y=130,width=200,height=20)
        self.plabel.place(x=125,y=180,width=120,height=20)
        self.pentry.place(x=180,y=210,width=200,height=20)
        self.button1.place(x=180,y=260,width=180,height=30)
        self.q.place(x=495,y=400,width=120,height=20)
        self.b.place(x=260,y=400,width=120,height=20)
        self.frame.pack()
            
    def enroll_and_move_to_next_screen(self):
        name = self.uentry.get()
        pin = self.pentry.get()
        if not name and not pin:
            messagebox._show("Error", "You need a name to enroll an account and you need to input a pin!")
            self.enroll_user()
        elif not pin:
            messagebox._show("Error", "You need to input a pin!")
            self.enroll_user()
        elif not name:
            messagebox._show("Error", "You need a name to enroll an account!")
            self.enroll_user()
        elif len(pin) != 4:
            messagebox._show("PIN Error", "Your PIN needs to be 4 digits!")
            self.enroll_user()
        else:
            self.write_to_csv()
            self.video_capture_page()
        
    def write_to_csv(self):
        import csv
        from random import randint
        n = 10;range_start = 10**(n-1);range_end = (10**n)-1
        account_number = randint(range_start, range_end)
        bank = "SRM Valliammai Bank"
        account_balance = "10000"
        name = self.uentry.get()
        pin = self.pentry.get()
        with open(r'bank_details.csv','a', newline = '\n') as f:
            writer = csv.writer(f)
            writer.writerow([account_number, name, bank, pin, account_balance])
        messagebox._show("Enrollment Info!", "Successfully Enrolled!")    

    def video_capture_page(self):
        self.frame.destroy()
        self.frame = Frame(self.root,bg="#ffffff",width=900,height=600)
        #Login Page Form Components
        self.button = Button(self.frame,text="Capture",bg="#3372de",fg="white",font=ARIAL,command=self.captureuser)
        self.button.place(x=200,y=300,width=400,height=30)
        self.frame.pack()

    def captureuser(self):
        haar_file = r'E:\AU\Final Yr Project\Bank Transaction using facial recognition\Project\Bank_Facial\haarcascade_frontalface_default.xml'
        
        # All the faces data will be present this folder 
        datasets = 'datasets'  
        
        # These are sub data sets of folder  
        data = pd.read_csv('bank_details.csv')
        sub_data = data.loc[:,'name'].values[-1]    
        
        path = os.path.join(datasets, sub_data) 
        if not os.path.isdir(path):
            os.mkdir(path) 
        
        # defining the size of images  
        (width, height) = (130, 100)     
        
        #'0' is used for my webcam,  
        # if you've any other camera 
        #  attached use '1' like this 
        face_cascade = cv2.CascadeClassifier(haar_file) 
        webcam = cv2.VideoCapture(0)  
        
        # The program loops until it has 50 images of the face. 
        count = 1
        while count < 50:  
            (_, im) = webcam.read() 
            gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY) 
            faces = face_cascade.detectMultiScale(gray, 1.3, 4) 
            for (x, y, w, h) in faces: 
                cv2.rectangle(im, (x, y), (x + w, y + h), (255, 0, 0), 2) 
                face = gray[y:y + h, x:x + w] 
                face_resize = cv2.resize(face, (width, height)) 
                cv2.imwrite('% s/% s.png' % (path, count), face_resize) 
                count += 1
            
            cv2.imshow('OpenCV', im) 
            key = cv2.waitKey(10) 
            if key == 27: 
                break
                
        webcam.release()
        cv2.destroyAllWindows()
        messagebox._show("Registration Info!", "Face ID Successfully Registered!")
        self.begin_page()
    
    def video_check(self):
        size = 4
        haar_file = r'E:\AU\Final Yr Project\Bank Transaction using facial recognition\Project\Bank_Facial\haarcascade_frontalface_default.xml'
        datasets = 'datasets'
        
        # Part 1: Create fisherRecognizer 
        print('Recognizing Face Please Be in sufficient Lights...') 
        
        # Create a list of images and a list of corresponding names
        (images, lables, names, id) = ([], [], {}, 0) 
        for (subdirs, dirs, files) in os.walk(datasets): 
            for subdir in dirs: 
                names[id] = subdir 
                subjectpath = os.path.join(datasets, subdir) 
                for filename in os.listdir(subjectpath): 
                    path = subjectpath + '/' + filename 
                    lable = id
                    images.append(cv2.imread(path, 0)) 
                    lables.append(int(lable)) 
                id += 1
        (width, height) = (130, 100) 
        
        # Create a Numpy array from the two lists above 
        (images, lables) = [numpy.array(lis) for lis in [images, lables]] 
        
        # OpenCV trains a model from the images 
        # NOTE FOR OpenCV2: remove '.face' 
        model = cv2.face.LBPHFaceRecognizer_create() 
        model.train(images, lables) 
        
        # Part 2: Use fisherRecognizer on camera stream 
        face_cascade = cv2.CascadeClassifier(haar_file) 
        webcam = cv2.VideoCapture(0) 
        while True: 
            (_, im) = webcam.read() 
            gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY) 
            faces = face_cascade.detectMultiScale(gray, 1.3, 5)
            if len(faces) != 0:
                for (x, y, w, h) in faces: 
                    cv2.rectangle(im, (x, y), (x + w, y + h), (255, 0, 0), 2) 
                    face = gray[y:y + h, x:x + w] 
                    face_resize = cv2.resize(face, (width, height)) 
                    # Try to recognize the face 
                    prediction = model.predict(face_resize) 
                    cv2.rectangle(im, (x, y), (x + w, y + h), (0, 255, 0), 3) 
            
                    if prediction[1]<75:         
                        cv2.putText(im, '% s - %.0f' % 
            (names[prediction[0]], prediction[1]), (x-10, y-10),  
            cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0)) 
                        self.final_page(names[prediction[0]])
                    else:
                        cv2.putText(im, 'not recognized',  
            (x-10, y-10), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0))
                        messagebox._show("Error!", "Face ID not recognized!") 
            
                cv2.imshow('OpenCV', im) 
                key = cv2.waitKey(50) 
                if key == -1: 
                    break
            
            else:
                messagebox._show("Error!", "No Face detected!\nPlease be in sufficient lights!")
                break

        webcam.release()
        cv2.destroyAllWindows()

    def final_page(self,name1):
        self.frame.destroy()
        self.frame = Frame(self.root, bg="#ffffff", width=900, height=600)
        name="Welcome "+name1
        self.label11 = Label(self.frame, text=name, bg="#ffffff", fg="black", font=("Times",25,"bold italic"))
        self.detail = Button(self.frame, text="Transfer", bg="#3372de",
                             fg="white", font=ARIAL, command=self.final_page)
        self.enquiry = Button(self.frame, text="Balance Enquiry",
                              bg="#3372de", fg="white", font=ARIAL, command=self.final_page)
        self.deposit = Button(self.frame, text="Deposit Money", bg="#3372de",
                              fg="white", font=ARIAL, command=self.final_page)
        self.withdrawl = Button(self.frame, text="Withdrawl Money", bg="#3372de",
                                fg="white", font=ARIAL, command=self.final_page)
        self.q = Button(self.frame, text="Log out", bg="#3372de",
                        fg="white", font=ARIAL, command=self.begin_page)
        self.label11.place(x=290, y=20, width=350, height=50)
        self.detail.place(x=70, y=100, width=200, height=50)
        self.enquiry.place(x=70, y=340, width=200, height=50)
        self.deposit.place(x=620, y=100, width=200, height=50)
        self.withdrawl.place(x=620, y=340, width=200, height=50)
        self.q.place(x=390, y=480, width=150, height=30)
        self.frame.pack()





root = Tk()
root.title("SRM Valliammai Bank")
root.geometry("1000x800")
root.configure(bg="white")
logo=PhotoImage(file="logo.ico")
root.iconphoto(False,logo)
obj = BankUi(root)
root.mainloop()