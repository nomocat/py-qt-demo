# cube_page.py
from PyQt5.QtWidgets import QWidget, QVBoxLayout
from PyQt5.QtOpenGL import QGLWidget
from OpenGL.GL import *
from OpenGL.GLU import *
from PyQt5.QtCore import Qt, QTimer

class CubeGLWidget(QGLWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.last_pos = None
        self.x_rot = 0
        self.y_rot = 0
        self.zoom = -6 # 视距

        # 旋转速度（阻尼惯性用）
        self.x_speed = 0
        self.y_speed = 0

        # 阻尼系数（0~1之间，越接近0减速越快）
        self.damping = 0.90

        # 定时器更新动画
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_animation)
        self.timer.start(16)  # ~60fps

    def initializeGL(self):
        glClearColor(0.1, 0.1, 0.1, 1.0)
        glEnable(GL_DEPTH_TEST)

    def resizeGL(self, w, h):
        glViewport(0, 0, w, h)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45, w / h if h != 0 else 1, 1, 100)
        glMatrixMode(GL_MODELVIEW)

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        glTranslatef(0, 0, -6)

        # 视距根据缩放变化
        glTranslatef(0, 0, self.zoom)

        # 根据拖拽更新旋转角度
        glRotatef(self.x_rot, 1, 0, 0)
        glRotatef(self.y_rot, 0, 1, 0)

        self.draw_cube()

    def draw_cube(self):
        vertices = [
            [1, 1, -1],
            [1, -1, -1],
            [-1, -1, -1],
            [-1, 1, -1],
            [1, 1, 1],
            [1, -1, 1],
            [-1, -1, 1],
            [-1, 1, 1]
        ]

        edges = [
            [0, 1], [1, 2], [2, 3], [3, 0],
            [4, 5], [5, 6], [6, 7], [7, 4],
            [0, 4], [1, 5], [2, 6], [3, 7]
        ]

        glBegin(GL_LINES)
        for edge in edges:
            for vertex in edge:
                glColor3f(0.8, 0.8, 1.0)
                glVertex3fv(vertices[vertex])
        glEnd()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.last_pos = event.pos()
            # 拖拽开始，清除速度
            self.x_speed = 0
            self.y_speed = 0

    def mouseMoveEvent(self, event):
        if self.last_pos is not None:
            dx = event.x() - self.last_pos.x()
            dy = event.y() - self.last_pos.y()

            self.x_rot += dy
            self.y_rot += dx
            self.x_rot %= 360
            self.y_rot %= 360

            # 记录速度，越快速度越大
            self.x_speed = dy
            self.y_speed = dx

            self.last_pos = event.pos()
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.last_pos = None
            # 释放鼠标，保持当前速度，继续动画

    def wheelEvent(self, event):
        # 滚轮滚动，delta为正向前（放大），负向后（缩小）
        delta = event.angleDelta().y() / 120  # 一个滚动刻度为120
        self.zoom += delta * 0.5  # 缩放速度

        # 限制缩放范围，避免摄像机穿透立方体或过远
        self.zoom = min(-2, max(-20, self.zoom))

        self.update()

    def update_animation(self):
        # 如果没有拖拽，执行惯性旋转和阻尼减速
        if self.last_pos is None:
            # 更新角度
            self.x_rot += self.x_speed
            self.y_rot += self.y_speed
            self.x_rot %= 360
            self.y_rot %= 360

            # 速度乘以阻尼系数逐渐减小
            self.x_speed *= self.damping
            self.y_speed *= self.damping

            # 当速度很小时停止旋转（防止一直慢慢转）
            if abs(self.x_speed) < 0.01 and abs(self.y_speed) < 0.01:
                self.x_speed = 0
                self.y_speed = 0

            self.update()

class CubePage(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.addWidget(CubeGLWidget())
        self.setLayout(layout)
