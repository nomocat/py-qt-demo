import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QListWidget, QStackedWidget, QWidget, QHBoxLayout
from placeholder_page import PlaceholderPage  # 可将原 PlaceholderPage 拆出
from cube_page import CubePage  # ✅ 引入新的页面
from draggable_page import DraggablePage  # ✅ 导入新页面
from buzzer_page import BuzzerPage

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("导航栏 Demo")
        self.setGeometry(100, 100, 800, 600)

        # 主布局
        main_widget = QWidget()
        main_layout = QHBoxLayout()

        # 导航栏（左侧）
        self.nav_list = QListWidget()
        self.nav_list.addItems([
            "主页",
            "功能一",
            "功能二",
            "cube",   # ✅ 新页面
            "drag",
            "buzzer",
            "设置",
            "关于"
        ])
        self.nav_list.currentRowChanged.connect(self.switch_page)
        self.nav_list.setFixedWidth(120)

        # 页面区域（右侧）
        self.stack = QStackedWidget()
        self.pages = {
            "主页": PlaceholderPage("主页"),
            "功能一": PlaceholderPage("功能一"),
            "功能二": PlaceholderPage("功能二"),
            "cube": CubePage(),
            "drag": DraggablePage(),
            "buzzer": BuzzerPage(),
            "设置": PlaceholderPage("设置"),
            "关于": PlaceholderPage("关于")
        }

        for page in self.pages.values():
            self.stack.addWidget(page)

        # 添加到主布局
        main_layout.addWidget(self.nav_list)
        main_layout.addWidget(self.stack)
        main_widget.setLayout(main_layout)

        self.setCentralWidget(main_widget)
        self.nav_list.setCurrentRow(0)

    def switch_page(self, index):
        self.stack.setCurrentIndex(index)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
