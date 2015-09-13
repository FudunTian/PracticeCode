# -*- coding: utf-8 -*- 
from PyQt4.QtGui import *
from PyQt4.QtCore import *
import sys
import os
import subprocess 
import platform
import traceback

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

    def fromFile(self):
        self.f=QFileDialog.getExistingDirectory(self,"Open file dialog","/")
        self.fromLineEdit.setText(str(self.f))
 
    def toFile(self):
        self.t=QFileDialog.getExistingDirectory(self,"Open file dialog","/")
        self.toLineEdit.setText(str(self.t))
 
    def yesTransWIN(self):
        param = self.paraComboBox.currentText()
        command={"Basic":"-apz","Cover":"--force"}
        f_rom = self.f
        t_o = self.t
        if param == "Basic":
            run = "rsync"+ " " + command["Basic"] + " "  +"/cygdrive/"+ f_rom  + "/" + " " +"/cygdrive/"+ t_o + "/"
            run.replace("\\","/")
            run.replace(":","")
            try:
                subprocess.call(str(run))
                QMessageBox.information(self,"information"," transfer successfully")
            except:
                QMessageBox.information(self,"information",traceback.format_exc())
                
 
        elif param == "Cover":
            run = "rsync"+ " " + command["Cover"] + " "  +"/cygdrive/" + f_rom + "/"+ " " + "/cygdrive/"+ t_o + "/"
            run.replace("\\","/")
            run.replace(":","")
            try:
                subprocess.call(str(run))
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
                os.system(str(run))
                QMessageBox.information(self,"information"," transfer successfully")
            except:
                QMessageBox.information(self,"information",traceback.format_exc())
                
 
        elif param == "Cover":
            run = "rsync"+ " " + command["Cover"] + " "  + f_rom + "/"+ " " + t_o + "/"
            run.replace("\\","/")
            run.replace(":","")
            try:
                os.system(str(run))
                QMessageBox.information(self,"information"," transfer successfully")
            except:
                QMessageBox.information(self,"information",traceback.format_exc())


app=QApplication(sys.argv)
form=StandardDialog()
form.show()
app.exec_()
