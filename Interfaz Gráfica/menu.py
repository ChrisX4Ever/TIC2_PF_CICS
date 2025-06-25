import sys
import threading
import serial
from PyQt5 import QtCore, QtGui, QtWidgets
import S_D, M_A, E_L  # Asegúrate de tener estos archivos con clase Ui_Form

class MenuApp(QtWidgets.QWidget):
    serial_signal = QtCore.pyqtSignal(int)

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.buttons = [self.J1, self.J2, self.J3]
        self.current_index = 0
        self.highlight_selection()
        self.subwindow_open = False  # 👈 Pausar entrada serial si hay ventana abierta

        self.J1.clicked.connect(self.launch_S_D)
        self.J2.clicked.connect(self.launch_M_A)
        self.J3.clicked.connect(self.launch_E_L)

        self.serial_signal.connect(self.handle_input)

        self.running = True
        self.serial_thread = threading.Thread(target=self.read_serial, daemon=True)
        self.serial_thread.start()

    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(913, 805)
        Form.setStyleSheet("background-color: rgb(0, 0, 127);")

        self.verticalLayoutWidget = QtWidgets.QWidget(Form)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(230, 220, 471, 281))
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(10, 10, 10, 10)

        self.J1 = QtWidgets.QPushButton("Simon dice", self.verticalLayoutWidget)
        self.J2 = QtWidgets.QPushButton("Modo aventura", self.verticalLayoutWidget)
        self.J3 = QtWidgets.QPushButton("Estilo libre", self.verticalLayoutWidget)

        for btn in [self.J1, self.J2, self.J3]:
            btn.setStyleSheet("background-color: rgb(255, 255, 0);")
            self.verticalLayout.addWidget(btn)

        self.textBrowser = QtWidgets.QTextBrowser(Form)
        self.textBrowser.setGeometry(QtCore.QRect(230, 120, 471, 101))
        self.textBrowser.setFocusPolicy(QtCore.Qt.NoFocus)
        self.textBrowser.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.textBrowser.setHtml(
            '<p align="center"><span style=" font-size:18pt; font-weight:600; color:#ffff00;">🎮Welcome to Game Center 🎮</span></p>'
        )

        for x, y, path in [
            (720, 470, "imagenes/Daco_31286.png"),
            (30, 50, "imagenes/pngwing.com.png"),
            (720, 60, "imagenes/584df3ad6a5ae41a83ddee08.png"),
            (40, 510, "imagenes/pngwing.com (1).png")
        ]:
            label = QtWidgets.QLabel(Form)
            label.setGeometry(QtCore.QRect(x, y, 161, 151))
            label.setPixmap(QtGui.QPixmap(path))
            label.setScaledContents(True)

    def highlight_selection(self):
        for i, btn in enumerate(self.buttons):
            if i == self.current_index:
                btn.setStyleSheet("background-color: rgb(0, 255, 0);")
            else:
                btn.setStyleSheet("background-color: rgb(255, 255, 0);")

    def handle_input(self, code):
        if self.subwindow_open:
            print("[INFO] Entrada ignorada: ventana secundaria abierta.")
            return

        print(f"[INFO] Código recibido: {code}")
        if code == 8:
            self.current_index = (self.current_index + 1) % len(self.buttons)
            self.highlight_selection()
        elif code == 7:
            self.current_index = (self.current_index - 1) % len(self.buttons)
            self.highlight_selection()
        elif code == 0:
            self.buttons[self.current_index].click()

    def read_serial(self):
        try:
            arduino = serial.Serial('COM5', 9600, timeout=1)
            print("[INFO] Puerto COM5 abierto correctamente.")
            while self.running:
                if arduino.in_waiting:
                    line = arduino.readline().decode(errors='ignore').strip()
                    if line.isdigit():
                        code = int(line)
                        print(f"[SERIAL] Recibido: '{code}'")
                        self.serial_signal.emit(code)
        except Exception as e:
            print(f"[ERROR SERIAL]: {e}")

    def launch_S_D(self):
        print("[INFO] Lanzando Simon Dice...")
        self.window_sd = QtWidgets.QMainWindow()
        self.ui_sd = S_D.Ui_Form()
        self.ui_sd.setupUi(self.window_sd)
        self.subwindow_open = True
        self.window_sd.show()
        self.window_sd.destroyed.connect(self.on_subwindow_closed)

    def launch_M_A(self):
        print("[INFO] Lanzando Modo Aventura...")
        self.window_ma = QtWidgets.QMainWindow()
        self.ui_ma = M_A.Ui_Form()
        self.ui_ma.setupUi(self.window_ma)
        self.subwindow_open = True
        self.window_ma.show()
        self.window_ma.destroyed.connect(self.on_subwindow_closed)

    def launch_E_L(self):
        print("[INFO] Lanzando Estilo Libre...")
        self.window_el = QtWidgets.QMainWindow()
        self.ui_el = E_L.Ui_Form()
        self.ui_el.setupUi(self.window_el)
        self.subwindow_open = True
        self.window_el.show()
        self.window_el.destroyed.connect(self.on_subwindow_closed)

    def on_subwindow_closed(self):
        print("[INFO] Ventana secundaria cerrada. Se reanuda el control.")
        self.subwindow_open = False

    def closeEvent(self, event):
        self.running = False
        event.accept()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MenuApp()
    window.show()
    sys.exit(app.exec_())