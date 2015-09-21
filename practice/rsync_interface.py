# -*- coding: utf-8 -*- 
from PyQt4.QtGui import *
from PyQt4.QtCore import *
import sys
import os,re
import subprocess 
import platform
import traceback
from PyQt4 import QtGui,QtCore
import ctypes
import rsync
reload(rsync)

PLAT = platform.system()

class NewDir(QtGui.QDialog):
    def __init__(self,parent = None):    
        yes=QPushButton("ESTIBILISH")
        no=QPushButton("Cancel")
        userlabel = QtGui.QLabel("The destination is not exist, do you want to set up it?")
        layout=QGridLayout()
        layout.addWidget(userlabel,1,0)
        layout.addWidget(yes,1,1)
        layout.addWidget(no,2,1)
        self.setLayout(layout)
        self.connect(yes,SIGNAL("clicked()"),self.SetUP)
        self.connect(no,SIGNAL("clicked()"),self.Cancel)
    def SetUP(self,dir):
        try:
            os.mkdir(dir)
        except:
            QMessageBox.critical(self,"error",traceback.format_exc())
        self.close()
    def Cancel(self):
        self.close()

class FileDialog(QtGui.QFileDialog):
    def __init__(self, *args):
        QtGui.QFileDialog.__init__(self, *args)
        self.setWindowModality(QtCore.Qt.ApplicationModal)
        self.setOption(self.DontUseNativeDialog, True)
        self.setFileMode(self.ExistingFiles)
        btns = self.findChildren(QtGui.QPushButton)
        self.openBtn = [x for x in btns if 'open' in str(x.text()).lower()][0]
        self.openBtn.clicked.disconnect()
        self.openBtn.clicked.connect(self.openClicked)
        self.tree = self.findChild(QtGui.QTreeView)
        self.selectedFiles = ""
    def setdir(dir):
        self.selectedFiles = dir
    def openClicked(self):
        inds = self.tree.selectionModel().selectedIndexes()
        files = []
        for i in inds:
            if i.column() == 0:
                files.append(os.path.join(str(self.directory().absolutePath()),str(i.data().toString())))
        self.selectedFiles = files
        self.hide()

    def filesSelected(self):
        return self.selectedFiles
 
class StandardDialog(QDialog):
    def __init__(self,parent=None):
        super(StandardDialog,self).__init__(parent)
        self.setWindowTitle("Rsync Dialog")
        self.resize(400,200)
        fromPushButton=QPushButton(self.tr("Select"))
        toPushButton=QPushButton(self.tr("Select"))
        yesPushButton=QPushButton(self.tr("Start"))
        CopyFrom = QtGui.QLabel("Copy from")
        CopyTo = QtGui.QLabel("Copy to")
        self.paraComboBox =QComboBox()
        self.paraComboBox.addItem("Copy")
        self.paraComboBox.addItem("Overrides")
        self.fromLineEdit=QLineEdit()
        self.toLineEdit=QLineEdit()
        self.BoxLineEdit=QLineEdit()
        spacerItem = QtGui.QSpacerItem(20, 166, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        layout=QGridLayout()
        layout.addWidget(CopyFrom,0,0)
        layout.addWidget(self.fromLineEdit,0,1 )
        layout.addWidget(fromPushButton,0,2)
        layout.addWidget(CopyTo,1,0)
        layout.addWidget(self.toLineEdit,1 ,1)
        layout.addWidget(toPushButton,1 ,2,)
        layout.addWidget(yesPushButton,3 ,0,1,3)
        layout.addWidget(self.paraComboBox,2,0,1,3)
        layout.addItem(spacerItem, 4, 0, 1, 3)
        self.setLayout(layout)
        self.connect(fromPushButton,SIGNAL("clicked()"),self.fromFile)
        self.connect(toPushButton,SIGNAL("clicked()"),self.toFile)
        self.connect(yesPushButton,SIGNAL("clicked()"),self.yesTrans)
    def fromFile(self):
        current_path = self.toLineEdit.text()
        if not current_path:
            current_path = '/'
        form = FileDialog(self,"Open file dialog",current_path)
        form.show()
        form.exec_()
        current_path = str(form.filesSelected())
        current_path = current_path.replace("]","")
        current_path = current_path.replace("[","")
        current_path = current_path.replace("'","")
        if current_path!= "":
            self.fromLineEdit.setText(current_path)
    def toFile(self):
        #print self.last_dst
        current_path = self.toLineEdit.text()
        if not current_path:
            current_path = '/'
        selected_path=QFileDialog.getExistingDirectory(self,"Open file dialog", current_path)
        if str(selected_path)!= "":
            self.toLineEdit.setText(str(selected_path))
        #self.last_dst = str(self.t)
        
    def yesTrans(self):
        param = self.paraComboBox.currentText()
        pattern = re.compile(r'(\\\\(\d+\.){3}\d+)(\\\w+)')
        src  = self.fromLineEdit.text()
        dst = self.toLineEdit.text()
        src = str(src)
        dst = str(dst)
        src_username = ""
        src_password = ""
        dst_username = "" 
        dst_password =""
        if  not  os.path.isdir(dst):
            askresult = QtGui.QMessageBox.question(self, 'make folder?', 'folder: %s does not exist, make it?' % dst,
                                                   QtGui.QMessageBox.Yes | QtGui.QMessageBox.Cancel)
            if askresult != QtGui.QMessageBox.Yes:
                return
            try:
                os.makedirs(dst)
            except:
                QMessageBox.critical(self,"error",traceback.format_exc() )
            
        mounted = False
        if param =="Copy":
            args = []
        else:
            args = ["--delete-after", "--force"]
        try:
            rsync.rsync(src, dst, args, src_username,src_password,dst_username,dst_password,mounted )
            QMessageBox.information(self,"information"," transfer successful")
        except:
            QMessageBox.critical(self,"error",traceback.format_exc())
    

                
                
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
        self.verfication = {"username":username ,"password":password}
        self.close()
    def getValue(self):
        return self.verfication

  
            
  
    
app=QApplication(sys.argv)
form=StandardDialog()
form.show()
form.raise_()
app.exec_()
