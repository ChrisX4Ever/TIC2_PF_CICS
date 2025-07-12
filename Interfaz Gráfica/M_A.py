# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtMultimedia import QSound
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtCore import QUrl
import os

from M_A_ui import Ui_MainWindow  # Importa desde el archivo generado por pyuic5

SOUND_PATH = "D:/Program Files/TIC2_PF_CICS/sounds"
IMAGE_PATH = "D:/Program Files/TIC2_PF_CICS/Interfaz Gráfica/imagenes"
VIDEO_PATH = "D:/Program Files/TIC2_PF_CICS/videos"

MODES = ["SUPER MARIO", "ZELDA", "POKEMON"]

SEQUENCES = {
    "SUPER MARIO": {
        (3, 3, 3, 1, 3, 3): "marioStarman.mkv",
        (0, 1, 2, 0, 1, 2, 5, 4): "marioStageClear.mkv",
        (2, 0, 2, 2, 0, 2): "marioUnderground.mkv",
        (2, 4, 6): "marioPowerUp.mkv",
        (5, 5, 5): "marioWarpPipe.mkv"
    },
    "ZELDA": {
        (4, 5, 4, 2, 3, 4, 5, 4): "zeldaLullaby.mkv",
        (3, 5, 6, 3, 5, 6): "zeldaSariaSong.mkv",
        (0, 1, 6, 0, 1, 6): "zeldaSongOfStorms.mkv",
        (5, 1, 3, 5, 1): "zeldaSongOfTime.mkv"
    },
    "POKEMON": {
        (2, 2, 2, 6): "pokemonLevelUp.mkv",
        (5, 4, 2, 1, 5, 4, 2, 1): "pokemonTrainerEncounter.mkv",
        (5, 3, 1): "pokemonCapture.mkv",
        (6, 6, 6): "pokemonCenterHealing.mkv",
        (4, 4, 4, 5, 4, 4): "pokemonGymBattle.mkv"
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
        self.video_player = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.video_widget = QVideoWidget(self.ui.label_3)
        self.video_widget.setGeometry(0, 0, self.ui.label_3.width(), self.ui.label_3.height())
        self.video_player.setVideoOutput(self.video_widget)
        self.video_widget.hide()

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
            pixmap = QtGui.QPixmap(os.path.join(IMAGE_PATH, "MiniMario.png"))
            self.ui.label_3.setPixmap(pixmap.scaled(self.ui.label_3.size(), QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation))
            pixmap2 = QtGui.QPixmap(os.path.join(IMAGE_PATH, "SecuenciasMario.png"))
            self.ui.label_2.setPixmap(pixmap2.scaled(self.ui.label_2.size(), QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation))
        elif mode == "ZELDA":
            pixmap = QtGui.QPixmap(os.path.join(IMAGE_PATH, "ZeldaLink.png"))
            self.ui.label_3.setPixmap(pixmap.scaled(self.ui.label_3.size(), QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation))
            pixmap2 = QtGui.QPixmap(os.path.join(IMAGE_PATH, "SecuenciasZelda.png"))
            self.ui.label_2.setPixmap(pixmap2.scaled(self.ui.label_2.size(), QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation))
        elif mode == "POKEMON":
            pixmap = QtGui.QPixmap(os.path.join(IMAGE_PATH, "Pikachu.png"))
            self.ui.label_3.setPixmap(pixmap.scaled(self.ui.label_3.size(), QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation))
            pixmap2 = QtGui.QPixmap(os.path.join(IMAGE_PATH, "SecuenciasPokemon.png"))
            self.ui.label_2.setPixmap(pixmap2.scaled(self.ui.label_2.size(), QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation))

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
        self.video_widget.show()
        self.video_player.setMedia(QMediaContent(QUrl.fromLocalFile(path)))
        self.video_player.play()
        self.video_player.mediaStatusChanged.connect(self.restore_image_after_video)

    def restore_image_after_video(self, status):
        if status == QMediaPlayer.EndOfMedia:
            self.video_widget.hide()
            self.set_mode(self.mode_index)
            self.video_player.stop()
            self.video_player.setMedia(QMediaContent())

    def closeEvent(self, event):
        if self.menu_ref:
            self.menu_ref.on_subwindow_closed()
        event.accept()