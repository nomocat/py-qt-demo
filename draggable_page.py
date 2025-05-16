# draggable_page.py
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QColor

class DraggableBox(QLabel):
    def __init__(self):
        super().__init__()
        self.setFixedSize(100, 100)
        self.setStyleSheet("background-color: red; border-radius: 8px;")
        self.setText("cube 1")
        self.setAlignment(Qt.AlignCenter)
        self.setAttribute(Qt.WA_TransparentForMouseEvents, False)
        self.setMouseTracking(True)
        self.dragging = False

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragging = True
            self.drag_start_position = event.globalPos() - self.pos()

    def mouseMoveEvent(self, event):
        if self.dragging:
            self.move(event.globalPos() - self.drag_start_position)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragging = False

class DraggablePage(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("拖动方块 Demo")
        self.setMinimumSize(600, 400)

        self.box = DraggableBox()
        self.box.setParent(self)
        self.box.move(100, 100)  # 初始位置
