# -*- coding: utf-8 -*- 
from PyQt4.QtGui import *
from PyQt4.QtCore import *
import sys
import os,re
import subprocess 
import platform
import traceback
from PyQt4 import QtGui,QtCore
QTextCodec.setCodecForTr(QTextCodec.codecForName("utf8"))
class StandardDialog(QDialog):
    def __init__(self,parent=None):
        super(StandardDialog,self).__init__(parent)
        self.setWindowTitle("Standard Dialog")
        fromPushButton=QPushButton(self.tr("FROM"))
        toPushButton=QPushButton(self.tr("TO"))
        yesPushButton=QPushButton(self.tr("YES"))
        self.paraComboBox =QComboBox()
        self.paraComboBox.addItem("Basic")
        self.paraComboBox.addItem("Cover")
        self.fromLineEdit=QLineEdit()
        self.toLineEdit=QLineEdit()
        self.BoxLineEdit=QLineEdit()
        layout=QGridLayout()
        layout.addWidget(self.paraComboBox,2,0)
        layout.addWidget(fromPushButton,0,1)
        layout.addWidget(self.fromLineEdit,0,0 )
        layout.addWidget(toPushButton,1 ,1)
        layout.addWidget(self.toLineEdit,1 ,0)
        layout.addWidget(yesPushButton,2 ,1)
        self.setLayout(layout)
        self.connect(fromPushButton,SIGNAL("clicked()"),self.fromFile)
        self.connect(toPushButton,SIGNAL("clicked()"),self.toFile)
        plat = platform.system()
        if plat == "Windows":
            self.connect(yesPushButton,SIGNAL("clicked()"),self.yesTransWIN)
        elif plat == "Linux":
            self.connect(yesPushButton,SIGNAL("clicked()"),self.yesTransLIN)
    def MountDriver(address,password,username):
        pattern = re.compile(r'(\\\\(\d+\.){3}\d+)(\\\w+)')
        match = pattern.match(address)
        c = str(match.group(1))
        amounted=address.replace(c,"q:")
        #print ("net use q:" +" "+address+" "+password+" "+"/USER:"+username)
        subprocess.call("net use q:" +" "+address+" "+password+" "+"/USER:"+username )
        return amounted
    def fromFile(self):
        self.f=QFileDialog.getExistingDirectory(self,"Open file dialog","/")
        self.fromLineEdit.setText(str(self.f))
 
    def toFile(self):
        self.t=QFileDialog.getExistingDirectory(self,"Open file dialog","/")
        self.toLineEdit.setText(str(self.t))
 
    def yesTransWIN(self):
        param = self.paraComboBox.currentText()
        command={"Basic":"-apz","Cover":"--force"}
        pattern = re.compile(r'(\\\\(\d+\.){3}\d+)(\\\w+)')
        f_rom = self.fromLineEdit.text()
        t_o = self.toLineEdit.text()
        if pattern.match(f_rom):
            verfication = PassWord()
            verfication.setModal(False)
            verfication.setWindowTitle('verfication')
            verfication.exec_()
            info = verfication.verfication()
            print info
        if param == "Basic":
            run = "rsync"+ " " + command["Basic"] + " "  +"/cygdrive/"+ f_rom  + "/" + " " +"/cygdrive/"+ t_o + "/"
            run.replace("\\","/")
            run.replace(":","")
            try:
                prog = subprocess.Popen (str(run),stdout = subprocess.PIPE,stderr = subprocess.PIPE)
                prog.communicate()
                if prog.returncode:
                    raise Exception("program returned error code {0}".format(prog.returncode) )
                QMessageBox.information(self,"information"," transfer successfully")
            except:
                QMessageBox.information(self,"information",traceback.format_exc())
                
 
        elif param == "Cover":
            run = "rsync"+ " " + command["Cover"] + " "  +"/cygdrive/" + f_rom + "/"+ " " + "/cygdrive/"+ t_o + "/"
            run.replace("\\","/")
            run.replace(":","")
            try:
                prog = subprocess.Popen (str(run),stdout = subprocess.PIPE,stderr = subprocess.PIPE)
                prog.communicate()
                if prog.returncode:
                    raise Exception("program returned error code {0}".format(prog.returncode) )
                QMessageBox.information(self,"information"," transfer successfully")
            except:
                QMessageBox.information(self,"information",traceback.format_exc())
        
        print run
        sys.stdout.flush()


    def yesTransLIN(self):
        param = self.paraComboBox.currentText()
        command={"Basic":"-apz","Cover":"--force"}
        f_rom = self.f
        t_o = self.t
        if param == "Basic":
            run = "rsync"+ " " + command["Basic"] + " "  + f_rom  + "/" + " " + t_o + "/"
            run.replace("\\","/")
            run.replace(":","")
            try:
                prog = subprocess.Popen (str(run),stdout = subprocess.PIPE,stderr = subprocess.PIPE)
                prog.communicate()
                if prog.returncode:
                    raise Exception("program returned error code {0}".format(prog.returncode) )
                QMessageBox.information(self,"information"," transfer successfully")
            except:
                QMessageBox.information(self,"information",traceback.format_exc())
                
 
        elif param == "Cover":
            run = "rsync"+ " " + command["Cover"] + " "  + f_rom + "/"+ " " + t_o + "/"
            run.replace("\\","/")
            run.replace(":","")
            try:
                prog = subprocess.Popen (str(run),stdout = subprocess.PIPE,stderr = subprocess.PIPE)
                prog.communicate()
                if prog.returncode:
                    raise Exception("program returned error code {0}".format(prog.returncode) )
                QMessageBox.information(self,"information"," transfer successfully")
            except:
                QMessageBox.information(self,"information",traceback.format_exc())

                
                
                
class PassWord(QtGui.QDialog):
    def __init__(self,parent = None):    
        self.username=QLineEdit()
        self.password=QLineEdit()
        userlabel = QtGui.QLabel("Username: ")
        userlabe2 = QtGui.QLabel("Password: ")
        self.password.setEchoMode(QtGui.QLineEdit.Password)
        QtGui.QWidget.__init__(self)
        yes = QtGui.QPushButton('YES')
        layout=QGridLayout()
        layout.addWidget(userlabel,1,0)
        layout.addWidget(userlabe2,2,0)
        layout.addWidget(self.username,1,1)
        layout.addWidget(self.password,2,1)
        layout.addWidget(yes,3,0)
        self.setLayout(layout)
        self.connect(yes,SIGNAL("clicked()"),self.verfication)
    def verfication(self):
        username = self.username.text()
        password = self.password.text()
        verfication = {"username":username ,"password":password}
        return verfication
        
    
app=QApplication(sys.argv)
form=StandardDialog()
form.show()
app.exec_()
