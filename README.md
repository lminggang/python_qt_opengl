# Linux 下，使用 Python + Qt + OpenGL实现图像渲染
## 环境安装
```
系统环境: Linux 各种版本应该都可以 我用的是 Debian
运行环境: python3.65 + qt for python + opengl
ui界面处理: qt designer(这个自行百度吧，文档很多)

QT官方地址: https://www.qt.io/
QT下载地址: http://download.qt.io/snapshots/ci/pyside/
QT文档地址: https://doc.qt.io/qtforpython/index.html
```
- 注: 别问我为什么用这个系统。这是系统是平时学习时下载的，在我去学习QT时mac环境很难装我就转到了linux虚拟机当时我的centOS、Ubuntu都不能用了...不是不能开机就是缺文件，我也不知道他们经历了什么。
### !!!最后注意一点!!! 如果是用虚拟机开发的朋友，记得关掉图像设置里的 """3D加速、垂直同步""" 如果找不到那就不影响，如果看见了一定要关掉。
```
Traceback (most recent call last):
  File "demo11.py", line 60, in initializeGL
    glEnable(GL_DEPTH_TEST)
  File "/home/super/anaconda3/lib/python3.6/site-packages/OpenGL/platform/baseplatform.py", line 402, in __call__
    return self( *args, **named )
  File "errorchecker.pyx", line 53, in OpenGL_accelerate.errorchecker._ErrorChecker.glCheckError (src/errorchecker.c:1218)
OpenGL.error.GLError: GLError(
        err = 1280,
        description = b'invalid enumerant',
        baseOperation = glEnable,
        cArguments = (GL_DEPTH_TEST,)
)
```
### 如果你也出现了以上问题，记得回来关掉。这个问题，我找了半天时间，各种重装环境差点儿就要重装个虚拟机！

## 最后讲解，该项目中存放了两个文件
opengl_demo.py 该文件是纯opengl编写的demo文件<br>
qt_opengl_demo.py 该文件时qt + opengl编写的文件