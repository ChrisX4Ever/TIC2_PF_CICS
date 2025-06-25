# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtGui, QtWidgets
import serial
import threading


class Ui_Form(object):
    def setupUi(self, Form):
        self.Form = Form
        Form.setObjectName("Form")
        Form.resize(913, 805)
        Form.setStyleSheet("background-color: rgb(0, 0, 127) ;")
        self.verticalLayoutWidget = QtWidgets.QWidget(Form)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(230, 220, 471, 281))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(10, 10, 10, 10)
        self.verticalLayout.setObjectName("verticalLayout")

        self.J1 = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.J1.setStyleSheet("background-color: rgb(255, 255, 0);")
        self.J1.setObjectName("J1")
        self.verticalLayout.addWidget(self.J1)

        self.J2 = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.J2.setStyleSheet("background-color: rgb(255, 255, 0);")
        self.J2.setObjectName("J2")
        self.verticalLayout.addWidget(self.J2)

        self.J3 = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.J3.setStyleSheet("background-color: rgb(255, 255, 0);")
        self.J3.setObjectName("J3")
        self.verticalLayout.addWidget(self.J3)

        self.textBrowser = QtWidgets.QTextBrowser(Form)
        self.textBrowser.setGeometry(QtCore.QRect(230, 120, 471, 101))
        self.textBrowser.setFocusPolicy(QtCore.Qt.NoFocus)
        self.textBrowser.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.textBrowser.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.textBrowser.setObjectName("textBrowser")

        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(720, 470, 161, 151))
        self.label.setPixmap(QtGui.QPixmap("imagenes/Daco_31286.png"))
        self.label.setScaledContents(True)
        self.label.setObjectName("label")

        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(30, 50, 171, 241))
        self.label_2.setPixmap(QtGui.QPixmap("imagenes/pngwing.com.png"))
        self.label_2.setScaledContents(True)
        self.label_2.setObjectName("label_2")

        self.label_3 = QtWidgets.QLabel(Form)
        self.label_3.setGeometry(QtCore.QRect(720, 60, 161, 181))
        self.label_3.setPixmap(QtGui.QPixmap("imagenes/584df3ad6a5ae41a83ddee08.png"))
        self.label_3.setScaledContents(True)
        self.label_3.setObjectName("label_3")

        self.label_4 = QtWidgets.QLabel(Form)
        self.label_4.setGeometry(QtCore.QRect(40, 510, 271, 81))
        self.label_4.setPixmap(QtGui.QPixmap("imagenes/pngwing.com (1).png"))
        self.label_4.setScaledContents(True)
        self.label_4.setObjectName("label_4")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

        # Lista de botones y selección actual
        self.buttons = [self.J1, self.J2, self.J3]
        self.current_index = 0
        self.highlight_selection()

        # Conectar clics
        self.J1.clicked.connect(self.launch_S_D)
        self.J2.clicked.connect(self.launch_M_A)
        self.J3.clicked.connect(self.launch_E_L)

        # Iniciar hilo de lectura serial
        self.running = True
        self.serial_thread = threading.Thread(target=self.read_serial, daemon=True)
        self.serial_thread.start()

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.J1.setText(_translate("Form", "Simon dice"))
        self.J2.setText(_translate("Form", "Modo aventura"))
        self.J3.setText(_translate("Form", "Estilo libre"))
        self.textBrowser.setHtml(_translate("Form", """
        <!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">
        <html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">
        p, li { white-space: pre-wrap; }
        </style></head><body style=\" font-family:'MS Shell Dlg 2'; font-size:8.25pt; font-weight:400; font-style:normal;\">
        <p align=\"center\"><span style=\" font-size:18pt; font-weight:600; color:#ffff00;\">🎮Welcome to Game Center 🎮</span></p></body></html>"""))

    def highlight_selection(self):
        for i, btn in enumerate(self.buttons):
            if i == self.current_index:
                btn.setStyleSheet("background-color: rgb(0, 255, 0);")
            else:
                btn.setStyleSheet("background-color: rgb(255, 255, 0);")

    def read_serial(self):
        try:
            arduino = serial.Serial('COM5', 9600)  # Cambia 'COM3' si tu Arduino usa otro puerto
            while self.running:
                if arduino.in_waiting:
                    data = arduino.readline().decode().strip()
                    if data.isdigit():
                        code = int(data)
                        QtCore.QTimer.singleShot(0, lambda c=code: self.handle_input(c))
        except Exception as e:
            print(f"[ERROR SERIAL]: {e}")

    def handle_input(self, code):
        if code == 8:
            self.current_index = (self.current_index + 1) % len(self.buttons)
            self.highlight_selection()
        elif code == 7:
            self.current_index = (self.current_index - 1) % len(self.buttons)
            self.highlight_selection()
        elif code == 0:
            self.buttons[self.current_index].click()

    def launch_S_D(self):
        import S_D
        self.window_sd = QtWidgets.QMainWindow()
        self.ui_sd = S_D.Ui_Form()
        self.ui_sd.setupUi(self.window_sd)
        self.window_sd.show()

    def launch_M_A(self):
        import M_A
        self.window_ma = QtWidgets.QMainWindow()
        self.ui_ma = M_A.Ui_Form()
        self.ui_ma.setupUi(self.window_ma)
        self.window_ma.show()

    def launch_E_L(self):
        import E_L
        self.window_el = QtWidgets.QMainWindow()
        self.ui_el = E_L.Ui_Form()
        self.ui_el.setupUi(self.window_el)
        self.window_el.show()

    def stop(self):
        self.running = False


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)

    def on_close():
        ui.stop()
        sys.exit()

    Form.show()
    app.aboutToQuit.connect(on_close)
    sys.exit(app.exec_())