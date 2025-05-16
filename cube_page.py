# cube_page.py
from PyQt5.QtWidgets import QWidget, QVBoxLayout
from PyQt5.QtOpenGL import QGLWidget
from OpenGL.GL import *
from OpenGL.GLU import *
from PyQt5.QtCore import Qt

class CubeGLWidget(QGLWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.last_pos = None
        self.x_rot = 0
        self.y_rot = 0

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

    def mouseMoveEvent(self, event):
        if self.last_pos is not None:
            dx = event.x() - self.last_pos.x()
            dy = event.y() - self.last_pos.y()

            self.x_rot += dy
            self.y_rot += dx
            self.x_rot %= 360
            self.y_rot %= 360

            self.last_pos = event.pos()
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.last_pos = None

class CubePage(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.addWidget(CubeGLWidget())
        self.setLayout(layout)
