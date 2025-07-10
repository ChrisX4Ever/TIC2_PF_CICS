import sys
import threading
import serial
from PyQt5 import QtCore, QtGui, QtWidgets
import S_D, M_A, E_L

class MenuApp(QtWidgets.QWidget):
    serial_signal = QtCore.pyqtSignal(object)  # Aceptar tanto int como str

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.buttons = [self.J1, self.J2, self.J3]
        self.current_index = 0
        self.highlight_selection()
        self.subwindow_open = False
        self.active_subwindow = None  # Guardar referencia a la ventana activa
        self.active_ui = None         # Guardar referencia al objeto UI

        self.J1.clicked.connect(self.launch_S_D)
        self.J2.clicked.connect(self.launch_M_A)
        self.J3.clicked.connect(self.launch_E_L)

        self.serial_signal.connect(self.handle_input)

        self.running = True
        self.arduino = None
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
            print("[INFO] Entrada secundaria enviada a subinterfaz")
            if hasattr(self.active_ui, "handle_serial"):
                self.active_ui.handle_serial(code)
            else:
                print("[INFO] Subinterfaz no tiene 'handle_serial'")
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
            self.arduino = serial.Serial('COM5', 9600, timeout=1)
            print("[INFO] Puerto COM5 abierto correctamente.")
        except Exception as e:
            print(f"[ERROR] No se pudo abrir el puerto COM5: {e}")
            return

        while self.running:
            try:
                if self.arduino.in_waiting:
                    line = self.arduino.readline().decode(errors='ignore').strip()
                    if line:
                        print(f"[SERIAL] Recibido: '{line}'")
                        if line.isdigit():
                            self.serial_signal.emit(int(line))
                        else:
                            self.serial_signal.emit(line)
            except Exception as e:
                print(f"[ERROR SERIAL]: {e}")
                continue

    def launch_subinterface(self, Module):
        self.subwindow_open = True
        window = QtWidgets.QMainWindow()
        ui = Module.Ui_MainWindow()
        ui.setupUi(window)
        window.ui = ui  # Guardar referencia del objeto ui
        self.active_subwindow = window
        self.active_ui = ui
        window.show()
        window.destroyed.connect(self.on_subwindow_closed)
        return window

    def launch_S_D(self):
        print("[INFO] Lanzando Simon Dice...")
        self.window_sd = self.launch_subinterface(S_D)

    def launch_M_A(self):
        print("[INFO] Lanzando Modo Aventura...")
        self.window_ma = self.launch_subinterface(M_A)

    def launch_E_L(self):
        print("[INFO] Lanzando Estilo Libre...")
        self.window_el = self.launch_subinterface(E_L)

    def on_subwindow_closed(self):
        print("[INFO] Ventana secundaria cerrada. Se reanuda el control.")
        self.subwindow_open = False
        self.active_subwindow = None
        self.active_ui = None

    def closeEvent(self, event):
        self.running = False
        if self.arduino and self.arduino.is_open:
            self.arduino.close()
        event.accept()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MenuApp()
    window.show()
    sys.exit(app.exec_())