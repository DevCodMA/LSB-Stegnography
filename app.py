from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PIL import Image
from main import *

class Ui_MainWindow(object):

    isValid = False
    isVisible = True
    isFile = False

    def alertbox(self, icon, text, title):
        msg = QMessageBox()
        msg.setIcon(icon)
        msg.setText(text)
        msg.setWindowTitle(title)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()

    def uploadFile(self):
        Ui_MainWindow.isFile = False
        self.filename2 = QFileDialog.getOpenFileName()[0]
        self.extension = self.filename2.split(".")[-1]
        if self.filename2 != "":
            self.filepath.setText(self.filename2)
            Ui_MainWindow.isFile = True
            if self.extension in ('png', 'jpg', 'jpeg', 'bmp', 'gif'):
                img = QtGui.QPixmap(self.filename2)
                img = img.scaled(self.label4.width(), self.label4.height())
                self.label4.setPixmap(img)


    def openFile(self):
        self.filename = QFileDialog.getOpenFileName(None, 'Browse Image', '', 'Image Files (*.png;*.jpg;*.jpeg;*.bmp;*.gif)')[0]

        if self.filename != '':
            filetype = self.filename.split('.')[-1].lower()
            Ui_MainWindow.isValid = [False, True][filetype in ('png', 'jpg', 'jpeg')]
            if Ui_MainWindow.isValid:
                img = QtGui.QPixmap(self.filename)
                img = img.scaled(self.label.width(), self.label.height())
                self.label.setPixmap(img)
            else:
                self.alertbox(QMessageBox.Warning, "Please upload a valid image! (accepted file types are: png, jpg, jpeg)", "Image Error")
                print("Please upload a valid image! (accept file types are: png, jpg, jpeg)")
        else:
            self.label.setPixmap(QtGui.QPixmap("Images/Upload.jpg"))

    def Encode(self):
        password = self.pswd.text()
        if not Ui_MainWindow.isFile:
            self.alertbox(QMessageBox.Warning, "Please upload a file before encrypt!", "File Error")
            return

        if Ui_MainWindow.isValid:
            if password == '':
                self.alertbox(QMessageBox.Warning, "Please enter the password!", "Password Error")
                return
            try:
                self.img = Image.open(self.filename)
                if self.extension in ('txt', 'dat'):
                    with open(self.filename2, 'rt') as file:
                        message = file.read()
                    self.imdata = encode(list(self.img.getdata()), password, f"{self.extension}{chr(254)}{message}")
                else:
                    with open(self.filename2, 'rb') as file:
                        message = file.read()
                    message = f'{self.extension}{chr(254)}{",".join([f"{i}" for i in message])}'
                    print(message)
                    pass
                    self.imdata = encode(list(self.img.getdata()), password, message)
                    self.filepath.setText("")
                    self.label4.setPixmap(QtGui.QPixmap("Images/no-img.jpg"))
                self.alertbox(QMessageBox.Information, "Encoding completed!", "Information")
            except Exception as ex:
                self.alertbox(QMessageBox.Warning, f"{ex}", "Processing Error")
        else:
            self.alertbox(QMessageBox.Warning, "Please upload an image to continue!", "Image Error")

    def Decode(self):
        password = self.pswd.text()
        try:
            if Ui_MainWindow.isValid:
                if password == '':
                    self.alertbox(QMessageBox.Warning, "Please enter the password!", "Password Error")
                else:
                    try:
                        de_image = Image.open(self.filename)
                        exten, dec_data = decode(tuple(de_image.getdata()), password)

                        if dec_data == chr(247):
                            self.alertbox(QMessageBox.Warning, "Incorrect password!", "Processing Error")
                        else:
                            savefile = QFileDialog.getSaveFileName(None, 'Save File', f'decrypted.{exten}', 'All Files (*.*)')[0]
                            if exten in ['txt', 'text', 'dat', 'csv']:
                                with open(savefile, 'wt') as file:
                                    file.write(dec_data)
                            else:
                                print(dec_data)
                                # byte = bytes()
                                # for i in dec_data.split(","):
                                #     byte += int(i).to_bytes(1, byteorder='little')
                                # with open(f"{savefile}", "wb") as file:
                                #     file.write(byte)

                    except Exception as ex:
                        print(ex)
                        self.alertbox(QMessageBox.Warning, f"{ex}", "Processing Error")
            else:
                self.alertbox(QMessageBox.Warning, "Please upload an image to continue!", "Image Error")
        except Exception as ex:
            print(ex)

    def saveFile(self):
        if Ui_MainWindow.isValid:
            self.pathname = QFileDialog.getSaveFileName(None, 'output', 'output.png', "Image Files (*.png)")[0]
            if self.pathname != '':
                fname = self.pathname.split('.')
                fname = fname[0]+'.png'
                try:
                    self.img.putdata(tuple(self.imdata))
                    self.img.save(fname)
                    self.label.setPixmap(QtGui.QPixmap("Images/Upload.jpg"))
                    self.msg.setText("")
                    self.pswd.setText("")
                except Exception as ex:
                    self.alertbox(QMessageBox.Warning, f"{ex}", "Processing Error")
        else:
            self.alertbox(QMessageBox.Warning, "Please upload an image to continue!", "Image Error")

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1333, 559)
        MainWindow.setMinimumSize(QtCore.QSize(1333, 559))
        MainWindow.setMaximumSize(QtCore.QSize(1333, 559))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        MainWindow.setFont(font)
        MainWindow.setCursor(QtGui.QCursor(QtCore.Qt.WhatsThisCursor))
        MainWindow.setMouseTracking(False)
        MainWindow.setToolTip("")
        MainWindow.setAutoFillBackground(False)
        MainWindow.setStyleSheet("QMainWindow{background: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(255, 178, 102, 255), stop:0.55 rgba(235, 148, 61, 255), stop:0.98 rgba(0, 0, 0, 255), stop:1 rgba(0, 0, 0, 0))}")
        MainWindow.setDocumentMode(True)
        MainWindow.setTabShape(QtWidgets.QTabWidget.Triangular)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.encode_btn = QtWidgets.QPushButton(self.centralwidget)
        self.encode_btn.setGeometry(QtCore.QRect(640, 130, 161, 61))
        self.encode_btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.encode_btn.setStyleSheet("QPushButton{border:2px solid rgba(0,0,0,0.5);border-radius:15px;font-weight:bold;background-color:white;font-size:17px;}")
        self.encode_btn.setObjectName("encode_btn")
        self.decode_btn = QtWidgets.QPushButton(self.centralwidget)
        self.decode_btn.setGeometry(QtCore.QRect(640, 220, 161, 61))
        self.decode_btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.decode_btn.setStyleSheet("QPushButton{border:2px solid rgba(0,0,0,0.5);border-radius:15px;font-weight:bold;background-color:white;font-size:17px;}")
        self.decode_btn.setObjectName("decode_btn")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(20, 20, 591, 361))
        self.label.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.label.setToolTip("")
        self.label.setStyleSheet("QLabel{border : 4px dashed rgba(0,0,0,0.4);background-color:rgba(255,255,255);cursor:pointer;}")
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap("Images/Upload.jpg"))
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.file_open = QtWidgets.QPushButton(self.centralwidget)
        self.file_open.setGeometry(QtCore.QRect(220, 430, 161, 61))
        self.file_open.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.file_open.setStyleSheet("QPushButton{border:2px solid rgba(0,0,0,0.5);border-radius:15px;font-weight:bold;background-color:white;font-size:17px;}")
        self.file_open.setObjectName("file_open")
        self.file_open.clicked.connect(self.openFile)
        self.file_save = QtWidgets.QPushButton(self.centralwidget)
        self.file_save.setGeometry(QtCore.QRect(450, 430, 161, 61))
        self.file_save.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.file_save.setStyleSheet("QPushButton{border:2px solid rgba(0,0,0,0.5);border-radius:15px;font-weight:bold;background-color:white;font-size:17px;}")
        self.file_save.setObjectName("file_save")

        self.browsebtn3 = QtWidgets.QPushButton(self.centralwidget)
        self.browsebtn3.setGeometry(QtCore.QRect(840, 90, 141, 55))
        self.browsebtn3.setStyleSheet("QPushButton{border:2px solid black;border-radius:10px;background-color:white;border-right:none;font-weight:bold;font-size:14px;border-top-right-radius:0px;border-bottom-right-radius:0px;}")
        self.browsebtn3.setObjectName("browsebtn3")
        self.browsebtn3.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.filepath = QtWidgets.QLabel(self.centralwidget)
        self.filepath.setGeometry(QtCore.QRect(981, 90, 310, 55))
        self.filepath.setStyleSheet("QLabel{background-color:rgba(255,255,255,0.35);border:2px solid black;border-top-right-radius:10px;border-bottom-right-radius:10px;}")
        self.filepath.setText("")
        self.filepath.setObjectName("filepath")

        self.label4 = QtWidgets.QLabel(self.centralwidget)
        self.label4.setGeometry(QtCore.QRect(840, 170, 451, 300))
        self.label4.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.label4.setToolTip("")
        self.label4.setStyleSheet("QLabel{border:3px dashed rgba(0,0,0,0.4);background-color:rgba(255,255,255);cursor:pointer;}")
        self.label4.setText("")
        self.label4.setPixmap(QtGui.QPixmap("Images/no-img.jpg"))
        self.label4.setAlignment(QtCore.Qt.AlignCenter)
        self.label4.setObjectName("label")

        self.msg = QtWidgets.QTextEdit(self.centralwidget)
        self.msg.setGeometry(QtCore.QRect(840, 100, 451, 281))
        self.msg.setToolTip("")
        self.msg.setStyleSheet("QTextEdit{padding:15px;border: 2px solid rgba(0,0,0,0.5);border-radius:15px;background-color:rgba(255,255,255);font-size:18px;}")
        self.msg.setObjectName("msg")
        self.msg.setVisible(False)

        self.pswd = QtWidgets.QLineEdit(self.centralwidget)
        self.pswd.setGeometry(QtCore.QRect(840, 20, 451, 51))
        self.pswd.setStyleSheet("QLineEdit{padding-left:10px;border: 2px solid rgba(0,0,0,0.5);border-radius:10px;font-size:18px;}")
        self.pswd.setMaxLength(40)
        self.pswd.setEchoMode(QLineEdit.Password)
        self.pswd.setDragEnabled(True)
        self.pswd.setObjectName("pswd")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1333, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.encode_btn.clicked.connect(self.Encode)
        self.decode_btn.clicked.connect(self.Decode)
        self.file_save.clicked.connect(self.saveFile)
        self.browsebtn3.clicked.connect(self.uploadFile)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "StegHide"))
        self.encode_btn.setText(_translate("MainWindow", "ENCODE"))
        self.decode_btn.setText(_translate("MainWindow", "DECODE"))
        self.label.setStatusTip(_translate("MainWindow", "Image Preview"))
        self.label.setWhatsThis(_translate("MainWindow", "You can view the uploaded image in this box."))
        self.file_open.setStatusTip(_translate("MainWindow", "Upload Image"))
        self.file_open.setText(_translate("MainWindow", "OPEN"))
        self.file_save.setStatusTip(_translate("MainWindow", "Save Image"))
        self.file_save.setText(_translate("MainWindow", "SAVE"))
        self.msg.setStatusTip(_translate("MainWindow", "Text to be hide"))
        self.msg.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\"><html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">p, li { white-space: pre-wrap; }</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:18px; font-weight:600; font-style:normal;\"><p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-weight:400;\"><br /></p></body></html>"))
        self.msg.setPlaceholderText(_translate("MainWindow", "Enter the text to hide: "))
        self.pswd.setPlaceholderText(_translate("MainWindow", "Enter the password: "))
        self.browsebtn3.setText(_translate("MainWindow", "BROWSE"))

        if Ui_MainWindow.isVisible:
            MainWindow.setStatusTip(_translate("MainWindow", "Hello World"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
