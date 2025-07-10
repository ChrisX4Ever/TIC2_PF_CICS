# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtMultimedia import QSound
import os

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(916, 752)
        MainWindow.setStyleSheet("background-color: rgb(0, 0, 127);")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(410, 500, 161, 171))
        self.label.setPixmap(QtGui.QPixmap("../../Downloads/Daco_31286.png"))
        self.label.setScaledContents(True)

        self.splitter = QtWidgets.QSplitter(self.centralwidget)
        self.splitter.setGeometry(QtCore.QRect(90, 10, 651, 511))
        self.splitter.setOrientation(QtCore.Qt.Vertical)

        self.textBrowser = QtWidgets.QTextBrowser(self.splitter)
        self.textBrowser.setMaximumSize(QtCore.QSize(16777215, 100))
        self.textBrowser.setHtml('<p align="center" style=" font-size:26pt; font-weight:600; color:#ffff00;">ESTILO LIBRE</p>')

        self.label_2 = QtWidgets.QLabel(self.splitter)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setStyleSheet("font-size: 28pt; font-weight: bold; color: yellow;")

        self.horizontalFrame = QtWidgets.QFrame(self.splitter)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.horizontalFrame)
        self.horizontalLayout_4.setContentsMargins(10, 10, 10, 10)
        self.horizontalLayout_4.setSpacing(0)

        self.buttons = []
        for i in range(7):
            button = QtWidgets.QPushButton(self.horizontalFrame)
            button.setStyleSheet("background-color: rgb(255, 255, 0);")
            button.setText("")
            button.setSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
            self.horizontalLayout_4.addWidget(button)
            self.buttons.append(button)

        self.b1, self.b2, self.b3, self.b4, self.b5, self.b6, self.b7 = self.buttons

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        MainWindow.setStatusBar(self.statusbar)

        self.current_octave = 1
        self.max_octave = 3
        self.min_octave = 1

        self.button_sounds = [
            (self.b1, "C", "Do"),
            (self.b2, "D", "Re"),
            (self.b3, "E", "Mi"),
            (self.b4, "F", "Fa"),
            (self.b5, "G", "Sol"),
            (self.b6, "A", "La"),
            (self.b7, "B", "Si"),
        ]

    def handle_serial(self, code):
        if code in range(7):
            button, note, text = self.button_sounds[code]
            self.highlight_button(button)
            self.play_sound(note)
            self.label_2.setText(text)

        elif code == 7:  # Botón 8: retroceder octava
            self.current_octave -= 1
            if self.current_octave < self.min_octave:
                self.current_octave = self.max_octave
            print(f"[E_L] Octava actual: {self.current_octave}")

        elif code == 8:  # Botón 9: avanzar octava
            self.current_octave += 1
            if self.current_octave > self.max_octave:
                self.current_octave = self.min_octave
            print(f"[E_L] Octava actual: {self.current_octave}")

        elif isinstance(code, str) and code.upper() == "A":
            print("[E_L] Cierre solicitado por botón prolongado.")
            parent_window = self.centralwidget.parent()
            if hasattr(parent_window, "destroyed") and parent_window:
                parent_window.close()
                if hasattr(parent_window, "parent") and parent_window.parent():
                    main_parent = parent_window.parent()
                    if hasattr(main_parent, "on_subwindow_closed"):
                        main_parent.on_subwindow_closed()

    def highlight_button(self, button):
        original = button.styleSheet()
        button.setStyleSheet("background-color: rgb(0, 255, 0);")
        QtCore.QTimer.singleShot(200, lambda: button.setStyleSheet(original))

    def play_sound(self, note):
        path = f"D:/Program Files/TIC2_PF_CICS/sounds/{self.current_octave}{note}.wav"
        if os.path.exists(path):
            QSound.play(path)
        else:
            print(f"[E_L] Archivo no encontrado: {path}")

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())