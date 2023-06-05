from msilib.schema import File
from multiprocessing import connection
from os import curdir
from sqlite3 import Date
import tkinter as tk
from tkinter import ttk
from tkinter.font import names
import tkcalendar
import mysql.connector as mc
import pickle as pkl
from datetime import datetime
from datetime import date
import time as t
import facerecwebcammod as frw
from PIL import ImageTk, Image
config=[]
setupstages=["1. Welcome","2. Introduction","3. MySQL connection","4. Making the database and tables","5. Adding users","6. Facial recognition data","7. Testing","8. Finishing and deployment mode"]
stage=0
setupstage=setupstages[stage]
def app():
    frw.LoadFaces()
    con=mc.connect(host="localhost",user=config[0]['user'],passwd=config[1]['pass'],database="facerecattendance")
    cur=con.cursor()
    print("Making window")
    win = tk.Tk()
    win.title("Face Attendance system")
    w=600
    h=600
    win.geometry('{}x{}'.format(w,h))
    frame=tk.Frame(win,width=650,height=400)
    frame.pack(side="top",expand=True, fill="both")
    l1=tk.Label(frame,text="Test",font=("Arial Bold",20)).pack()
    l2=tk.Label()
    def register():
        name=frw.FaceRec()
        if name in config[2]['unames']:
            print(name)
            d=date.today().strftime("%Y/%m/%d")
            print(d)
            nd=name+d
            print(nd)
            print(config[4]['Attendance'])
            l2=tk.Label()
            if nd in config[4]['Attendance']:
                print("Condition satisfied")
                l2.destroy()
                l2=tk.Label(frame,text="Your name is already registered for today. Please come tomorrow!",fg="red").place(x=20,y=100)
            else:
                print("Condition not satisfied")
                config[4]['Attendance'].append(nd)
                print(config[4]['Attendance'])
                uid=config[2]['unames'].index(name)+1
                print(uid)
                cur.execute("INSERT INTO LOG VALUES({},'{}')".format(uid,d))
                print("Command executed")
                con.commit()
                print("Database changed")
                l2.destroy()
                l2=tk.Label(frame,text="Your name is logged for the day successfully. Have a great day! ",fg="green").place(x=20,y=100)
        else:
            l2=tk.Label(frame,text="You are not recognized. Therefore your name is not logged. Please contact administrator if you feel this is a mistake.",fg="red").place(x=20,y=100)
    def report():
 
 
        class Table:
     
            def __init__(self,root):
         
                # code for creating table
                for i in range(total_rows):
                    for j in range(total_columns):
                 
                        self.e = tk.Entry(root, width=20, fg='blue',
                                       font=('Arial',16,'bold'))
                 
                        self.e.grid(row=i, column=j)
                        self.e.insert('end', lst[i][j])
 
    # take the data
        cur.execute("SELECT UID,FNAME,LNAME,COUNT(*) 'Number of days' FROM USERS NATURAL JOIN LOG GROUP BY UID")
        lst = cur.fetchall()
        lst.insert(0,('UID','First name','Last name',"Number of days"))
  
        # find total number of rows and
        # columns in list
        total_rows = len(lst)
        total_columns = len(lst[0])
  
        # create root window
        root = tk.Tk()
        t = Table(root)
        root.mainloop()

    registerbutton=tk.Button(frame,text="Attendance",command=register)
    registerbutton.pack()
    reportbutton=tk.Button(frame,text="Report",command=report)
    reportbutton.pack()

    win.mainloop()
def setup():
    global setupstages
    global stage
    global setupstage
    global unames
    global ucount
    unames=[]
    ucount=0
    window = tk.Tk()
    window.title("Setup")
    w=600
    h=600
    window.geometry('{}x{}'.format(w,h))
    frame=tk.Frame(window,width=650,height=400)
    frame.pack(side="top",expand=True, fill="both")
    def screens():
        global setupstages
        global stage
        global setupstage
        nonlocal frame

        l1=tk.Label(frame,text=setupstage,font=("Arial Bold",20)).pack(padx=10,pady=10)

        if stage==0:


            l2=tk.Label(frame,text="Welcome to setup.  ",font=("Arial",10)).pack()
            l3=tk.Label(frame,text="This wizard will guide you through the setup process of this program. Sit back and relax.",font=("Arial",10)).pack()
            l4=tk.Label(frame,text="This won't take long.",font=("Arial",10)).pack()


            window.mainloop()
        elif stage==1:
            l2=tk.Label(frame,text="Thank you for downloading this program.",font=("Arial",10)).pack()
            l3=tk.Label(frame,text="This program uses facial recognition to record attendances of students/employees in an organisation.",font=("Arial",10)).pack()
            l4=tk.Label(frame,text="We use in device recognition (OPENCV) and we won't use any big company's tech.",font=("Arial",10)).pack()
            l5=tk.Label(frame,text="And, we finally use MySQL to log the attendence of the users.",font=("Arial",10)).pack()
            l6=tk.Label(frame,text="Voila!",font=("Arial",10)).pack()
        elif stage==2:
            l2=tk.Label(frame,text="Now, we need to connect to the MySQL backend, so we can store data.",font=("Arial",10)).pack()
            l3=tk.Label(frame,text="Please enter your details below and click 'Connect'. ",font=("Arial",10)).pack()
            l4=tk.Label(frame,text="Username:",font=("Arial",10)).place(x=10,y=300)
            txt=tk.Entry(frame,width=50)
            txt.place(x=80,y=300)
            l5=tk.Label(frame,text="Password:",font=("Arial",10)).place(x=10,y=320)
            pwd=tk.Entry(frame,show='*',width=50)
            pwd.place(x=80,y=320)
            def cnt():
                global con
                global u
                global p
                u=txt.get()
                p=pwd.get()
                try:
                    global con
                    con=mc.connect(host="localhost",user=u,passwd=p)
                    nonlocal l6
                    if con.is_connected():
                        l6=tk.Label(frame,text="Connected successfully!    ",font=("Arial",10),fg="green").place(x=10,y=340)
                    config.append({"user":u})
                    config.append({"pass":p})
                except:
                    l6=tk.Label(frame,text="Bad credentials. Try again.",font=("Arial",10),fg="red").place(x=10,y=340)


            cb=tk.Button(frame,text="Connect",command=cnt).place(x=10,y=360)
            window.mainloop()
        elif stage==3:
            print(config)
            l2=tk.Label(frame,text="We now have to create the tables",font=("Arial",10))
            l2.pack()
            def tab():
                
                cur.execute("USE FACERECATTENDANCE")
                cur.execute("CREATE TABLE USERS(UID INT PRIMARY KEY, FNAME VARCHAR(30), LNAME VARCHAR(30),SEX CHAR(1), DOB DATE, CLASS INT, SEC CHAR(1) )")
                cur.execute("CREATE TABLE LOG(UID INT, EDATE DATE, FOREIGN KEY(UID) REFERENCES USERS(UID))")
                nonlocal l3
                l3.destroy()
                nonlocal maketb
                maketb.destroy()
                l3=tk.Label(frame,text="Tables created successfully!",fg="green",font=("Arial",10))
                l3.pack()
            maketb=tk.Button(frame,text="Make TABLES",command=tab,font=("Arial",10))
            def db():
                global cur
                cur=con.cursor()
                cur.execute("CREATE DATABASE FACERECATTENDANCE")
                makedb.destroy()
                nonlocal maketb                
                maketb.pack()
                nonlocal l3
                l3=tk.Label(frame,text="Database created successfully!",fg="green",font=("Arial",10))
                l3.pack()
            makedb=tk.Button(frame,text="Make DB",command=db,font=("Arial",10))
            makedb.pack()
        elif stage==4:
            l2=tk.Label(frame,text="Now, this is the part where we add users to our database.")
            l2.pack()
            l3=tk.Label(frame,text="Go ahead and type the credentials of the users. Then, click 'Add' to, well add the users to the database.")
            l3.pack()
            fn=tk.Label(frame,text="First Name:")
            fn.place(x=10,y=200)
            ft=tk.Entry(frame, width=50)
            ft.place(x=75,y=200)
            ln=tk.Label(frame,text="Last Name:")
            ln.place(x=10,y=220)
            lt=tk.Entry(frame, width=50)
            lt.place(x=75,y=220)
            s=tk.Label(frame,text="Sex:")
            s.place(x=10,y=240)
            combo=ttk.Combobox(frame)
            combo.place(x=40,y=240)
            combo['values']=('Select',"Male","Female","Transgender")
            combo.current(0)
            sd={"Male":'M',"Female":'F',"Transgender":'T'}
            b=tk.Label(frame,text="DOB:")
            b.place(x=10,y=260)
            # Add Calendar
            cal = tkcalendar.Calendar(frame, selectmode = 'day',
                           year = 2005, month = 3,
                           day = 7)
            c=tk.Label(frame,text="Class:")
            c.place(x=10,y=450)
            ct=tk.Entry(frame,width=20)
            ct.place(x=60,y=450)
            se=tk.Label(frame,text="Section:")
            se.place(x=10,y=470)
            sect=tk.Entry(frame,width=20)
            sect.place(x=60,y=470)
            
            cal.place(x=40,y=260)
            def addrec():
                firstname=ft.get()
                lastname=lt.get()
                global unames
                unames.append(firstname+"_"+lastname)
                global ucount
                nonlocal cal
                ucount+=1
                sex=sd[combo.get()]
                dob=datetime.strptime(cal.get_date(),"%m/%d/%y").strftime("%Y/%m/%d")
                cla=ct.get()
                sec=sect.get()
                cur.execute("INSERT INTO USERS VALUES({},'{}','{}','{}','{}',{},'{}')".format(ucount,firstname,lastname,sex,dob,cla,sec))
                con.commit()
                conf=tk.Label(frame,text="Added successfully!",fg="green")
                conf.place(x=10,y=520)
                lt.delete(0, "end")
                ft.delete(0, "end")
                ct.delete(0, "end")
                sect.delete(0, "end")
                combo.current(0)
                cal.destroy()
                cal = tkcalendar.Calendar(frame, selectmode = 'day',
                year = 2005, month = 3,
                day = 7)
                cal.place(x=40,y=260)
            add=tk.Button(frame,text="Add",command=addrec)
            add.place(x=20,y=500)
        elif stage==5:
            L=[]
            for i in config:
                for j in i:
                    L.append(j)
            if "uname" not in L and "ucount" not in L:
                config.append({'unames':unames})
                config.append({'ucount':ucount})
            else:
                config[2]={'unames':unames}
                config[3]={'ucount':ucount}
            print(config)
            l1=tk.Label(frame,text="Now is the time to add the faces to the program, so that the program can identify the faces of your users.")
            l1.pack()
            l2=tk.Label(frame,text="Please add the faces in the 'Faces' folder of this program's directory and click on 'Load faces' button below.")
            l2.pack()
            faces=None
            def Load():
                faces=frw.LoadFaces()
                print (faces)
                a=True
                if len(faces)!= len(unames):
                    a=False
                else:
                    for i in unames:
                        print(i)
                        if i not in faces:
                            print("Not found in db")
                            a=False
                            break
                        else:
                            print("Found in db")
                if a:
                    conf=tk.Label(frame,text="All users added!                  ", fg="green")
                    conf.pack()

                else:
                    conf=tk.Label(frame,text="Faces are missing... Please check!",fg="red")
                    conf.pack()
            load=tk.Button(frame,text="Load faces",command=Load)
            load.pack()
        elif stage==6:
            tested=False
            l1=tk.Label(frame,text="Now, we test the facial recognition algorithm.").pack()
            l2=tk.Label(frame,text="Press the 'Test' button below to test the algorithm, and stand in front of the camera.").pack()
            def testalg():
                name=frw.FaceRec(20)
                conf=tk.Label(frame,text=name).pack()
                l3=tk.Label(frame,text="Successfully working!",fg="green").pack()
            test=tk.Button(frame,text="Test",command=testalg)
            test.pack()
        elif stage==7:
            l2=tk.Label(frame,text="We have reached the end of setup.").pack()
            l3=tk.Label(frame,text="Please click the finish button to exit setup and start the software.").pack()
            def finish():
                print(config)
                File=open("Config.dat","wb+")
                for i in config:
                    print(i)
                    pkl.dump(i,File)
                pkl.dump({"Attendance":[]},File)
                window.destroy()
            finishbutton=tk.Button(frame,text="Finish",command=finish).pack()


    def clearframe():
        nonlocal frame
        for widgets in frame.winfo_children():
            widgets.destroy()
    def next():
        global setupstages
        global stage
        global setupstage   
        clearframe()
        if stage!=7:
            stage+=1
            setupstage=setupstages[stage]
        screens()
    def last():
        global setupstages
        global stage
        global setupstage
        clearframe()
        if stage!=0:
            stage-=1
            setupstage=setupstages[stage]
        screens()
    nb=tk.Button(window,text="Next",command=next)
    nb.place(x=w-50,y=h-50)
    lb=tk.Button(window,text="Previous",command=last)
    lb.place(x=10,y=h-50)
    screens()
def configdata():
    cf=open("Config.dat","rb+")
    global config
    config=[]
    try:
        i=pkl.load(cf)
        print(i)
        while i:
            config.append(i)
            i=pkl.load(cf)
            print(i)
    except:
        print(config)



try:
    print("Config")
    configdata()
    print("App")
    app()
except FileNotFoundError:
    setup()
    configdata()
    app()
    