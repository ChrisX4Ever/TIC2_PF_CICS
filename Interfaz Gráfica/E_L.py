import sys
import os
from PyQt5 import QtCore, QtGui, QtWidgets, QtMultimedia

class Ui_MainWindow(object):
    serial_signal = QtCore.pyqtSignal(str)  # Señales tipo str para incluir "A"

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
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setStyleSheet("color: white; font-size: 32pt; font-weight: bold;")

        self.horizontalFrame = QtWidgets.QFrame(self.splitter)
        self.horizontalFrame.setStyleSheet("color: rgb(0, 0, 127);")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.horizontalFrame)
        self.horizontalLayout_4.setContentsMargins(10, 10, 10, 10)

        self.buttons = []
        for i in range(7):
            button = QtWidgets.QPushButton(self.horizontalFrame)
            button.setStyleSheet("background-color: rgb(255, 255, 0);")
            button.setObjectName(f"b{i+1}")
            self.horizontalLayout_4.addWidget(button)
            self.buttons.append(button)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.octavas = ['1', '2', '3']
        self.octava_actual = 0
        self.nombres = ['Do', 'Re', 'Mi', 'Fa', 'Sol', 'La', 'Si']
        self.rutas = ['1C', '1D', '1E', '1F', '1G', '1A', '1B']

        # Conexión serial
        self.serial_thread = SerialThread(self)
        self.serial_thread.signal.connect(self.manejar_entrada)
        self.serial_thread.start()

    def manejar_entrada(self, entrada):
        if entrada.isdigit():
            num = int(entrada)
            if 0 <= num <= 6:
                self.activar_boton(num)
            elif num == 7:
                self.octava_actual = (self.octava_actual - 1) % 3
                print(f"[INFO] Octava actual: {self.octavas[self.octava_actual]}")
            elif num == 8:
                self.octava_actual = (self.octava_actual + 1) % 3
                print(f"[INFO] Octava actual: {self.octavas[self.octava_actual]}")
        elif entrada == 'A':
            QtWidgets.QApplication.quit()

    def activar_boton(self, indice):
        # Cambiar color
        for i, b in enumerate(self.buttons):
            b.setStyleSheet("background-color: rgb(255, 255, 0);")
        self.buttons[indice].setStyleSheet("background-color: rgb(0, 255, 0);")

        # Mostrar texto
        self.label_2.setText(self.nombres[indice])

        # Reproducir audio
        nombre_archivo = f"{self.octavas[self.octava_actual]}{self.rutas[indice][1]}.wav"
        ruta = os.path.join("D:/Program Files/TIC2_PF_CICS/sounds", nombre_archivo)
        if os.path.exists(ruta):
            QtMultimedia.QSound.play(ruta)
        else:
            print(f"[ERROR] No se encuentra: {ruta}")

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Estilo Libre"))
        self.textBrowser.setHtml(_translate("MainWindow",
            '<p align="center"><span style=" font-size:26pt; font-weight:600; color:#ffff00;">ESTILO LIBRE</span></p>'
        ))
        self.label_2.setText("")

class SerialThread(QtCore.QThread):
    signal = QtCore.pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.running = True

    def run(self):
        import serial
        try:
            arduino = serial.Serial('COM5', 9600, timeout=1)
            print("[INFO] Serial COM5 abierto correctamente.")
            while self.running:
                if arduino.in_waiting:
                    line = arduino.readline().decode().strip()
                    if line:
                        print(f"[SERIAL] Recibido: {line}")
                        self.signal.emit(line)
        except Exception as e:
            print(f"[ERROR SERIAL]: {e}")

    def stop(self):
        self.running = False
        self.quit()
        self.wait()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())