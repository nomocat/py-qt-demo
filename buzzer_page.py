# buzzer_page.py
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel
import pygame
import numpy as np
import time
import threading

class BuzzerPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
        self.init_audio()

    def init_ui(self):
        layout = QVBoxLayout()

        label = QLabel("蜂鸣器模拟器", self)
        layout.addWidget(label)

        self.btn_beep = QPushButton("播放蜂鸣器声")
        self.btn_beep.clicked.connect(self.play_beep)
        layout.addWidget(self.btn_beep)

        self.setLayout(layout)

    def init_audio(self):
        pygame.mixer.init(frequency=44100, size=-16, channels=1)

    def play_beep(self):
        # 用线程播放，防止卡 GUI
        threading.Thread(target=self._play_beep_sound, daemon=True).start()

    def _play_beep_sound(self):
        duration = 0.5     # 秒
        frequency = 1000   # Hz
        sample_rate = 44100

        n_samples = int(sample_rate * duration)
        t = np.linspace(0, duration, n_samples, False)
        tone = 0.5 * np.sin(2 * np.pi * frequency * t)
        audio = (tone * 32767).astype(np.int16)

        sound = pygame.sndarray.make_sound(audio)
        sound.play()
        time.sleep(duration)
