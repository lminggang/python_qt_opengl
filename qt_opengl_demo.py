import sys
from PySide2 import QtCore, QtGui, QtWidgets, QtOpenGL

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

from PIL import Image
import numpy as np

class GLWidget(QtOpenGL.QGLWidget):
    def __init__(self, parent=None, file_path=''):
        QtOpenGL.QGLWidget.__init__(self, parent)
        self.file_path = file_path
        self.translate_x, self.translate_y = 0, 0
        self.click_x, self.click_y = 0, 0
        self.angle = 0
        # x,y,z zoom Number
        self.zoom_x, self.zoom_y, self.zoom_z = 1, 1, 1
        # now zoom Number
        self.zoom_num = 0

        # 图片被点住(鼠标左键)标志位
        self.isLeftPressed = bool(False)
        # Moving speed
        self.movingSpeed = 0.001
    
    def loadGLTextures(self):
        img = Image.open(self.file_path)
        width, height = img.size
        img = img.tobytes('raw', 'RGBX', 0, -1)

        glGenTextures(2)
        glBindTexture(GL_TEXTURE_2D, 1)
        glTexImage2D(GL_TEXTURE_2D, 0, 4, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, img)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)

    # QT 初始化方法
    def initializeGL(self):
        self.loadGLTextures()
        glEnable(GL_TEXTURE_2D)
        glEnable(GL_DEPTH_TEST)
        glClearDepth(1.0)
        glDepthFunc(GL_LESS)
        glShadeModel(GL_SMOOTH)
        glEnable(GL_CULL_FACE)

        glCullFace(GL_BACK)
        glEnable(GL_POINT_SMOOTH)
        glEnable(GL_LINE_SMOOTH)
        glEnable(GL_POLYGON_SMOOTH)
        glMatrixMode(GL_PROJECTION)
        glHint(GL_POINT_SMOOTH_HINT,GL_NICEST)
        glHint(GL_LINE_SMOOTH_HINT,GL_NICEST)
        glHint(GL_POLYGON_SMOOTH_HINT,GL_FASTEST)
        glLoadIdentity()
        gluPerspective(45.0, float(500)/float(500), 0.1, 100.0)
        glMatrixMode(GL_MODELVIEW)

    # QT 画图方法
    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()

        #沿z轴平移
        glTranslate(self.translate_x, self.translate_y,-5)
        glRotated(self.angle, self.translate_x, self.translate_y,-5)
        glScaled(self.zoom_x, self.zoom_y, self.zoom_z)
        #分别绕x,y,z轴旋转
        glRotatef(0.0, 1.0, 0.0, 0.0)
        glRotatef(0.0, 0.0, 1.0, 0.0)
        glRotatef(0.0, 0.0, 0.0, 1.0)

        #开始绘制立方体的每个面，同时设置纹理映射
        glBindTexture(GL_TEXTURE_2D, 1)
        #绘制四边形
        glBegin(GL_QUADS)        
        #设置纹理坐标
        glTexCoord2f(0.0, 0.0)
        #绘制顶点
        glVertex3f(-1.0, -1.0, 1.0)
        glTexCoord2f(1.0, 0.0)
        glVertex3f(1.0, -1.0, 1.0)
        glTexCoord2f(1.0, 1.0)
        glVertex3f(1.0, 1.0, 1.0)
        glTexCoord2f(0.0, 1.0)
        glVertex3f(-1.0, 1.0, 1.0)
        glEnd()
    
    def resizeGL(self, w, h):
        glViewport(0, 0, self.width(), self.height())

    '''重载一下鼠标按下事件(单击)'''
    def mousePressEvent(self, event):
        if event.buttons() == QtCore.Qt.LeftButton:                            # 左键按下
            print("鼠标左键单击")  # 响应测试语句
            self.isLeftPressed = True;                                         # 左键按下(图片被点住),置Ture
            self.click_x, self.click_y = event.x(), event.y()                  # 获取鼠标当前位置
        elif event.buttons() == QtCore.Qt.RightButton:                         # 右键按下
            print("鼠标右键单击")  # 响应测试语句
        elif event.buttons() == QtCore.Qt.MidButton:                           # 中键按下
            print("鼠标中键单击")  # 响应测试语句
        elif event.buttons() == QtCore.Qt.LeftButton | QtCore.Qt.RightButton:  # 左右键同时按下
            print("鼠标左右键同时单击")  # 响应测试语句
        elif event.buttons() == QtCore.Qt.LeftButton | QtCore.Qt.MidButton:    # 左中键同时按下
            print("鼠标左中键同时单击")  # 响应测试语句
        elif event.buttons() == QtCore.Qt.MidButton | QtCore.Qt.RightButton:   # 右中键同时按下
            print("鼠标右中键同时单击")  # 响应测试语句
        elif event.buttons() == QtCore.Qt.LeftButton | QtCore.Qt.MidButton \
             | QtCore.Qt.RightButton:                                          # 左中右键同时按下
            print("鼠标左中右键同时单击")  # 响应测试语句

    '''重载一下鼠标键公开事件'''
    def mouseReleaseEvent(self, event):
        print("into mouseReleaseEvent")
        if event.button() == QtCore.Qt.LeftButton:                            # 左键释放
            self.isLeftPressed = False;  # 左键释放(图片被点住),置False
            print("鼠标左键松开")  # 响应测试语句
        elif event.button() == QtCore.Qt.RightButton:                                 # 右键释放
            self.emptyPaint()
            print("鼠标右键松开")  # 响应测试语句
    
    '''重载一下鼠标移动事件'''
    def mouseMoveEvent(self,event):
        if self.isLeftPressed:                                                   # 左键按下
            self.translate_x += ((event.x() - self.click_x) * self.movingSpeed)             # 更新偏移量 x 
            self.translate_y -= ((event.y() - self.click_y) * self.movingSpeed)             # 更新偏移量 y
            self.updateGL()                                                      # 重绘
            self.click_x, self.click_y = event.x(), event.y()                    # 更新当前鼠标在窗口上的位置，下次移动用
    

    '''重载一下滚轮滚动事件'''
    def wheelEvent(self, event):
        angle=event.angleDelta() / 8                                           # 返回QPoint对象，为滚轮转过的数值，单位为1/8度
        angleY=angle.y()                                                       # 竖直滚过的距离

        if angleY > 0:                                                        # 滚轮上
            self.zoomInPicture(event)
        else:                                                                  # 滚轮下滚
            self.zoomOutPicture(event)
    
    def zoomInPicture(self, event=None):
        if self.zoom_x < 4:
            self.zoom_x += 0.1
            self.zoom_y += 0.1
            self.zoom_z += 0.1
            self.updateGL()

    def zoomOutPicture(self, event=None):
        if self.zoom_x > 0.5:
            self.zoom_x -= 0.1
            self.zoom_y -= 0.1
            self.zoom_z -= 0.1
            self.updateGL()
    

    def rotatePicture(self, angle):
        self.angle = angle
        self.updateGL()
        print("鼠标右键松开")  # 响应测试语句
    
    def updatePicture(self, old_picture):
        print('updatePicture')
        self.translate_x, self.translate_y = old_picture.translate_x, old_picture.translate_y
        self.click_x, self.click_y = old_picture.click_x, old_picture.click_y
        self.angle = old_picture.angle
        # x,y,z zoom Number
        self.zoom_x, self.zoom_y, self.zoom_z = old_picture.zoom_x, old_picture.zoom_y, old_picture.zoom_z
        self.updateGL()
    
    def emptyPaint(self):
        self.translate_x, self.translate_y = 0, 0
        self.click_x, self.click_y = 0, 0
        self.angle = 0
        # x,y,z zoom Number
        self.zoom_x, self.zoom_y, self.zoom_z = 1, 1, 1
        # now zoom Number
        self.zoom_num = 0
        # 图片被点住(鼠标左键)标志位
        self.isLeftPressed = bool(False)
        self.updateGL()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = GLWidget(file_path='../test_data/123.jpg')
    window.show()
    sys.exit(app.exec_())
