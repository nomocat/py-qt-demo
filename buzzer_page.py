# buzzer_page.py
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QHBoxLayout
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
        label = QLabel("蜂鸣器音调测试", self)
        layout.addWidget(label)

        # 多个音调按钮
        btn_layout = QHBoxLayout()

        self.btn_low = QPushButton("低音 (500Hz)")
        self.btn_low.clicked.connect(lambda: self.play_beep(500))
        btn_layout.addWidget(self.btn_low)

        self.btn_mid = QPushButton("中音 (1000Hz)")
        self.btn_mid.clicked.connect(lambda: self.play_beep(1000))
        btn_layout.addWidget(self.btn_mid)

        self.btn_high = QPushButton("高音 (2000Hz)")
        self.btn_high.clicked.connect(lambda: self.play_beep(2000))
        btn_layout.addWidget(self.btn_high)

        layout.addLayout(btn_layout)
        self.setLayout(layout)

    def init_audio(self):
        pygame.mixer.init(frequency=44100, size=-16, channels=1)

    def play_beep(self, frequency=1000):
        threading.Thread(target=lambda: self._play_beep_sound(frequency), daemon=True).start()

    def _play_beep_sound(self, frequency):
        duration = 0.5     # 秒
        sample_rate = 44100

        n_samples = int(sample_rate * duration)
        t = np.linspace(0, duration, n_samples, False)
        tone = 0.5 * np.sin(2 * np.pi * frequency * t)
        audio = (tone * 32767).astype(np.int16)

        sound = pygame.sndarray.make_sound(audio)
        sound.play()
        time.sleep(duration)
