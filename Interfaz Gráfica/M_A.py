# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtMultimedia import QSound
import os
import threading
import vlc
import sys

from M_A_ui import Ui_MainWindow  # Interfaz generada con pyuic5

SOUND_PATH = "D:/Program Files/TIC2_PF_CICS/sounds"
IMAGE_PATH = "D:/Program Files/TIC2_PF_CICS/Interfaz Gráfica/imagenes"
VIDEO_PATH = "D:/Program Files/TIC2_PF_CICS/videos"

MODES = ["SUPER MARIO", "ZELDA", "POKEMON"]

SEQUENCES = {
    "SUPER MARIO": {
        (3, 3, 3, 1, 3, 3): "marioStarman.mp4",
        (0, 1, 2, 0, 1, 2, 5, 4): "marioStageClear.mp4",
        (2, 0, 2, 2, 0, 2): "marioUnderground.mp4",
        (2, 4, 6): "marioPowerUp.mp4",
        (5, 5, 5): "marioWarpPipe.mp4"
    },
    "ZELDA": {
        (4, 5, 4, 2, 3, 4, 5, 4): "zeldaLullaby.mp4",
        (3, 5, 6, 3, 5, 6): "zeldaSariaSong.mp4",
        (0, 1, 6, 0, 1, 6): "zeldaSongOfStorms.mp4",
        (5, 1, 3, 5, 1): "zeldaSongOfTime.mp4"
    },
    "POKEMON": {
        (2, 2, 2, 6): "pokemonLevelUp.mp4",
        (5, 4, 2, 1, 5, 4, 2, 1): "pokemonTrainerEncounter.mp4",
        (5, 3, 1): "pokemonCapture.mp4",
        (6, 6, 6): "pokemonCenterHealing.mp4",
        (4, 4, 4, 5, 4, 4): "pokemonGymBattle.mp4"
    }
}

class MainWindowLogic(QtWidgets.QMainWindow):
    def __init__(self, parent_menu=None):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.menu_ref = parent_menu
        self.mode_index = 0
        self.recent_signals = []

        # VLC Widget encima de label_3
        self.vlc_widget = QtWidgets.QFrame(self.ui.label_3)
        self.vlc_widget.setGeometry(0, 0, self.ui.label_3.width(), self.ui.label_3.height())
        self.vlc_widget.setStyleSheet("background-color: black;")
        self.vlc_widget.hide()

        # Configurar VLC
        self.vlc_instance = vlc.Instance()
        self.vlc_player = self.vlc_instance.media_player_new()

        self.buttons = [self.ui.b1, self.ui.b2, self.ui.b3, self.ui.b4, self.ui.b5, self.ui.b6, self.ui.b7]
        self.special_buttons = [self.ui.b8, self.ui.b9]

        self.ui.combobox_games.currentIndexChanged.connect(self.set_mode_from_combobox)

        if self.menu_ref:
            self.menu_ref.subwindow_open = True
            self.menu_ref.active_subwindow = self
            self.menu_ref.active_ui = self

        self.set_mode(0)

    def handle_serial(self, code):
        if isinstance(code, int):
            if 0 <= code <= 6:
                self.play_note(code)
                self.recent_signals.append(code)
                if len(self.recent_signals) > 12:
                    self.recent_signals.pop(0)
                self.check_sequence()
            elif code == 7:
                self.highlight_button(self.ui.b8)
                self.mode_index = (self.mode_index - 1) % len(MODES)
                self.set_mode(self.mode_index)
            elif code == 8:
                self.highlight_button(self.ui.b9)
                self.mode_index = (self.mode_index + 1) % len(MODES)
                self.set_mode(self.mode_index)
        elif isinstance(code, str) and code.upper() == "A":
            print("[M_A] Cierre remoto recibido desde botón físico")
            if self.menu_ref:
                self.menu_ref.on_subwindow_closed()
            self.close()

    def highlight_button(self, button):
        original_color = button.styleSheet()
        button.setStyleSheet("background-color: rgb(0, 255, 0);")
        QtCore.QTimer.singleShot(500, lambda: button.setStyleSheet(original_color))

    def play_note(self, index):
        notes = ["C", "D", "E", "F", "G", "A", "B"]
        note = notes[index]
        button = self.buttons[index]
        self.highlight_button(button)
        file = os.path.join(SOUND_PATH, f"3{note}.wav")
        QSound.play(file)

    def set_mode(self, index):
        self.mode_index = index
        self.ui.combobox_games.blockSignals(True)
        self.ui.combobox_games.setCurrentIndex(index)
        self.ui.combobox_games.blockSignals(False)

        mode = MODES[index]
        if mode == "SUPER MARIO":
            self.set_pixmap(self.ui.label_3, "MiniMario.png")
            self.set_pixmap(self.ui.label_2, "SecuenciasMario.png")
        elif mode == "ZELDA":
            self.set_pixmap(self.ui.label_3, "ZeldaLink.png")
            self.set_pixmap(self.ui.label_2, "SecuenciasZelda.png")
        elif mode == "POKEMON":
            self.set_pixmap(self.ui.label_3, "Pikachu.png")
            self.set_pixmap(self.ui.label_2, "SecuenciasPokemon.png")

    def set_pixmap(self, label, filename):
        pixmap = QtGui.QPixmap(os.path.join(IMAGE_PATH, filename))
        label.setPixmap(pixmap.scaled(label.size(), QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation))

    def set_mode_from_combobox(self, index):
        self.set_mode(index)

    def check_sequence(self):
        current_mode = MODES[self.mode_index]
        signals = tuple(self.recent_signals[-12:])
        for sequence, video_file in SEQUENCES[current_mode].items():
            if tuple(signals[-len(sequence):]) == sequence:
                self.play_video(video_file)
                break

    def play_video(self, filename):
        path = os.path.join(VIDEO_PATH, filename)
        if not os.path.exists(path):
            print(f"[ERROR] Video no encontrado: {path}")
            return

        print(f"[VIDEO] Reproduciendo: {path}")

        # Mostrar el widget antes de usar winId
        self.vlc_widget.show()
        self.vlc_widget.raise_()  # Asegura que esté encima de label_3
        QtWidgets.QApplication.processEvents()  # Fuerza actualización

        # Establecer el widget como salida de video
        if sys.platform.startswith("win"):
            self.vlc_player.set_hwnd(int(self.vlc_widget.winId()))
        else:
            self.vlc_player.set_xwindow(int(self.vlc_widget.winId()))  # Para Linux

        media = self.vlc_instance.media_new(path)
        self.vlc_player.set_media(media)
        
        # Usar timer en vez de thread para monitorear el estado
        self.vlc_player.play()
        QtCore.QTimer.singleShot(500, self.monitor_video_end)

    def monitor_video_end(self):
        if not self.vlc_player.is_playing():
            self.on_video_finished()
        else:
            QtCore.QTimer.singleShot(500, self.monitor_video_end)

    def on_video_finished(self):
        self.vlc_widget.hide()
        self.set_mode(self.mode_index)

    def closeEvent(self, event):
        if self.menu_ref:
            self.menu_ref.on_subwindow_closed()
        if self.vlc_player:
            self.vlc_player.stop()
        event.accept()