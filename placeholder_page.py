from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel

class PlaceholderPage(QWidget):
    def __init__(self, title):
        super().__init__()
        layout = QVBoxLayout()
        label = QLabel(title)
        label.setStyleSheet("font-size: 24px;")
        layout.addWidget(label)
        layout.addStretch()
        self.setLayout(layout)