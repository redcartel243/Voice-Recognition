import os
import sys
import time
from threading import Thread
import pyttsx3
from PyQt5 import QtCore, QtGui, QtWidgets
import speech_recognition as sr
from PyQt5.QtWidgets import *


import Data
from VoiceType import Ui_MainWindow
from FaceRecognition import Ui_MainWindow2

class VoiceRecorder(Thread):#thread for the gui
    def __init__(self):
        Thread.__init__(self)



    def takeCommands(self):
        while True:
           if Data.Listen == True:
               r = sr.Recognizer()
               with sr.Microphone() as source:
                   Data.state = "Listening"
                   print(Data.state)
                   r.pause_threshold = 0.7
                   audio = r.listen(source)
                   try:
                       Data.state = "Recognizing"
                       print(Data.state)

                       Query = r.recognize_google(audio, language='en-in')
                       print("the query is printed =", Query, "'")
                       Data.state="Done"
                       Data.Listen = False
                       return Query
                   except Exception as e:
                       print(e)
                       print("say that again sir")
                       return "None"



           else:
               pass
    def supptxt(self,red):
        if Data.supp == True:
            red=""
            self.txt = " "
            Data.supp = False
            print(self.txt)

    def quitSelf(self):
        self.Speak("do you want to switch off the computer sir")
        take = self.takeCommands()
        choice = take
        if "yes" in choice:
            print("shutting down the computer")
            self.Speak("shutting down the computer")
            os.system("shutdown /s /t 30")
        if "no" in choice:
            print("thank you sir")
            self.Speak("thank you sir")
    def run(self):
        while True:
            self.rec = VoiceRecorder()
            self.txt=""
            self.txt=self.txt +" "+ self.rec.takeCommands()
            Data.text=Data.text+" "+self.txt
            self.supptxt(Data.text)





class WorkerThread(QtCore.QObject):
    State = QtCore.pyqtSignal()
    Display=QtCore.pyqtSignal()

    def __init__(self):
        super().__init__()

    @QtCore.pyqtSlot()
    def run(self):
        while True:
            # Long running task ...
            self.State.emit()
            self.Display.emit()
            time.sleep(0.5)

class MyActions(Ui_MainWindow):
    def __init__(self, title=" "):
        self.title = title
        self.left = 250
        self.top = 250
        self.width = 200
        self.height = 150

        # update setupUi

    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)
        # MainWindow.resize(400, 300) # do not modify it
        MainWindow.move(self.left, self.top)  # set location for window
        MainWindow.setWindowTitle(self.title)  # change title
        self.worker = WorkerThread()
        self.workerThread = QtCore.QThread()
        self.workerThread.started.connect(self.worker.run)  # Init worker run() at startup (optional)
        self.worker.State.connect(self.State)  # Connect your signals/slots
        self.worker.Display.connect(self.Display)
        self.worker.moveToThread(self.workerThread)  # Move the Worker object to the Thread object
        self.workerThread.start()
        self.pushButton.clicked.connect(self.Onclick1)
        self.pushButton_2.clicked.connect(self.Onclick2)
        self.pushButton_3.clicked.connect(self.Listen)
        self.pushButton_4.clicked.connect(self.Read)
        self.comboBox.currentIndexChanged.connect(self.ComboChange)
    def ComboChange(self):
        if self.comboBox.currentIndex()==1:
            print("1")
            MainWindow.close()
            MainWindow2.show()
        if self.comboBox.currentIndex()==0:
            print("0")
            MainWindow2.close()
            MainWindow.show()


    def Listen(self):
        Data.Listen=True
    def State(self):

        self.label_2.setText(Data.state)
    def Display(self):

        self.textEdit.setText(Data.text+"\n")
    def Speak(self, audio):
        engine = pyttsx3.init('sapi5')
        voices = engine.getProperty('voices')
        engine.setProperty('voice', voices[1].id)
        engine.say(audio)
        engine.runAndWait()
    def Read(self):
        try:
            self.red=self.textEdit.toPlainText()
            self.Speak(self.red)
        except Exception as e:
            self.Speak("nothing is displayed")




    def Onclick1(self):
        file_exists = os.path.isfile("Printed.txt")
        if file_exists:
            fichier = open("Printed.txt", "a")
            fichier.write(Data.text+"\n")
        else:
            fichier = open("Printed.txt", "w")
            fichier.write(Data.text+"\n")
        fichier.close()
    def Onclick2(self):
        self.textEdit.clear()
        Data.text=""
class MyActions2(Ui_MainWindow2):
    def __init__(self, title=" "):
        self.title = title
        self.left = 250
        self.top = 250
        self.width = 200
        self.height = 150

        # update setupUi

    def setupUi1(self, MainWindow):
        super().setupUi(MainWindow)
        # MainWindow.resize(400, 300) # do not modify it
        MainWindow.move(self.left, self.top)  # set location for window
        MainWindow.setWindowTitle(self.title)  # change title
        self.comboBox.currentIndexChanged.connect(self.ComboChange)
    def ComboChange(self):
        if self.comboBox.currentIndex()==1:
            print("1")
            MainWindow2.close()
            MainWindow.show()
        if self.comboBox.currentIndex()==0:
            print("0")
            MainWindow.close()
            MainWindow2.show()

app = QtWidgets.QApplication(sys.argv)
app2=QtWidgets.QApplication(sys.argv)
MainWindow = QtWidgets.QMainWindow()
MainWindow2=QtWidgets.QMainWindow()
ui = MyActions("Speech recognizer")
ui2 = MyActions2("Face Recognition")
ui.setupUi(MainWindow)
ui2.setupUi(MainWindow2)
MainWindow.show()
sys.exit(app.exec_())



thread_1=VoiceRecorder()
thread_1.start()
thread_1.join()