import sys
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from PIL import Image
import numpy as np


translate_x, translate_y = 0, 0
click_x, click_y = 0,0
angle = 0
zoom_x, zoom_y, zoom_z = 1, 1, 1
def draw():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    #沿z轴平移
    glTranslate(translate_x,translate_y,-5)
    glRotated(angle, translate_x,translate_y,-5)
    glScaled(zoom_x, zoom_y, zoom_z)
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
    glutSwapBuffers()

def LoadTexture():
    img = Image.open('with angle.bmp')
    width, height = img.size
    img = img.tobytes('raw', 'RGBX', 0, -1)
    
    glGenTextures(2)
    glBindTexture(GL_TEXTURE_2D, 1)
    glTexImage2D(GL_TEXTURE_2D, 0, 4, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE,img)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)


def mouseclick(button, state, x, y):
    global click_x, click_y, zoom_x, zoom_y, zoom_z
    click_x, click_y = x, y
    zoom_x, zoom_y, zoom_z = 2, 2, 2
    glutPostRedisplay()
    print('mouse click!!!')
    
def mousemotion(x, y):
    global angle, translate_x, translate_y, click_x, click_y
    translate_x += ((x - click_x) * 0.005)
    translate_y -= ((y - click_y) * 0.005)
    angle = 45
    glutPostRedisplay()

    click_x, click_y = x , y

if __name__ == "__main__":

    glClearColor(0.0, 0.0, 0.0, 1.0) # 设置画布背景色。注意：这里必须是4个参数
    glEnable(GL_DEPTH_TEST)          # 开启深度测试，实现遮挡关系
    glDepthFunc(GL_LEQUAL)           # 设置深度测试函数（GL_LEQUAL只是选项之一）
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT) # clear session
    glutInit()                           # 1. 初始化glut库
    glutInitWindowSize(500, 500)
    glutCreateWindow('OpenGL')           # 2. 创建glut窗口
    glutDisplayFunc(draw)                # 3. 注册回调函数draw()
    glutMouseFunc(mouseclick)           # 注册响应鼠标点击的函数mouseclick()
    glutMotionFunc(mousemotion)         # 注册响应鼠标拖拽的函数mousemotion()

    
    LoadTexture()
    glEnable(GL_TEXTURE_2D)
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

    glutMainLoop()                       # 4. 进入glut主循环