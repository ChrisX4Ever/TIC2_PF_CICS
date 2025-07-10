import sys
import threading
import serial
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtMultimedia import QSound

# RUTA BASE PARA LOS SONIDOS
SOUND_PATH = "D:/Program Files/TIC2_PF_CICS/sounds"

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(916, 752)
        MainWindow.setStyleSheet("background-color: rgb(0, 0, 127);")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(410, 500, 161, 171))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap("../../Downloads/Daco_31286.png"))
        self.label.setScaledContents(True)
        self.label.setObjectName("label")

        self.splitter = QtWidgets.QSplitter(self.centralwidget)
        self.splitter.setGeometry(QtCore.QRect(90, 10, 651, 511))
        self.splitter.setOrientation(QtCore.Qt.Vertical)
        self.splitter.setObjectName("splitter")

        self.textBrowser = QtWidgets.QTextBrowser(self.splitter)
        self.textBrowser.setMaximumSize(QtCore.QSize(16777215, 100))
        self.textBrowser.setObjectName("textBrowser")

        self.label_2 = QtWidgets.QLabel(self.splitter)
        self.label_2.setObjectName("label_2")

        self.horizontalFrame = QtWidgets.QFrame(self.splitter)
        self.horizontalFrame.setStyleSheet("color: rgb(0, 0, 127);")
        self.horizontalFrame.setObjectName("horizontalFrame")

        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.horizontalFrame)
        self.horizontalLayout_4.setContentsMargins(10, 10, 10, 10)
        self.horizontalLayout_4.setSpacing(0)

        self.buttons = []
        for i in range(7):
            btn = QtWidgets.QPushButton(self.horizontalFrame)
            btn.setStyleSheet("background-color: rgb(255, 255, 0);")
            btn.setText("")
            self.horizontalLayout_4.addWidget(btn)
            self.buttons.append(btn)

        (self.b1, self.b2, self.b3, self.b4, self.b5, self.b6, self.b7) = self.buttons

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 916, 21))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.octava = 1
        self.octavas_disponibles = [1, 2, 3]
        self.menu_ref = None

    def set_parent_menu(self, menu_ref):
        self.menu_ref = menu_ref

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.textBrowser.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
            "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
            "p, li { white-space: pre-wrap; }\n"
            "</style></head><body style=\" font-family:'MS Shell Dlg 2'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
            "<p align=\"center\"><span style=\" font-size:26pt; font-weight:600; color:#ffff00;\">ESTILO LIBRE</span></p></body></html>"))
        self.label_2.setText("TextLabel")

    def handle_serial(self, code):
        notas = ["C", "D", "E", "F", "G", "A", "B"]
        nombres = ["Do", "Re", "Mi", "Fa", "Sol", "La", "Si"]

        if isinstance(code, int):
            if 0 <= code <= 6:
                btn = self.buttons[code]
                self.iluminar_boton(btn)
                nota = notas[code]
                nombre = nombres[code]
                archivo = f"{SOUND_PATH}/{self.octava}{nota}.wav"
                QSound.play(archivo)
                self.label_2.setText(f"<h1 style='color: yellow'>{nombre}</h1>")

            elif code == 7:
                idx = self.octavas_disponibles.index(self.octava)
                self.octava = self.octavas_disponibles[idx - 1] if idx > 0 else self.octavas_disponibles[-1]
                print(f"[E_L] Octava actual: {self.octava}")

            elif code == 8:
                idx = self.octavas_disponibles.index(self.octava)
                self.octava = self.octavas_disponibles[(idx + 1) % len(self.octavas_disponibles)]
                print(f"[E_L] Octava actual: {self.octava}")

        elif isinstance(code, str) and code.upper() == "A":
            print("[E_L] Cierre remoto recibido desde botón físico")
            if self.menu_ref:
                self.menu_ref.on_subwindow_closed()
            QtWidgets.QApplication.instance().activeWindow().close()

    def iluminar_boton(self, boton):
        original_color = "background-color: rgb(255, 255, 0);"
        highlight_color = "background-color: rgb(0, 255, 0);"

        boton.setStyleSheet(highlight_color)
        QtCore.QTimer.singleShot(500, lambda: boton.setStyleSheet(original_color))

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())