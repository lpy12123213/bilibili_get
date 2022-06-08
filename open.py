import sys
 
from PyQt5.QtCore import QUrl
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineProfile
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton
 
 
# 先来个窗口
class window(QWidget):
    def __init__(self):
        super().__init__()
        self.setup()
 
    def setup(self):
        self.box = QVBoxLayout(self)                      # 创建一个垂直布局来放控件
        self.btn_get = QPushButton('点击获取cookies')   # 创建一个按钮涌来了点击获取cookie
        self.btn_get.clicked.connect(self.get_cookie)     # 绑定按钮点击事件
        self.web = MyWebEngineView()                      # 创建浏览器组件对象
        self.web.resize(800, 600)                         # 设置大小
        self.web.load(QUrl("https://www.bilibili.com"))  # 打开百度页面来测试
        self.box.addWidget(self.btn_get)                  # 将组件放到布局内，先在顶部放一个按钮
        self.box.addWidget(self.web)                      # 再放浏览器
        self.web.show()                                   # 最后让页面显示出来
 
    def get_cookie(self):
        cookie = self.web.get_cookie()
        self.cookie = cookie
 
 
# 创建自己的浏览器控件，继承自QWebEngineView
class MyWebEngineView(QWebEngineView):
    def __init__(self, *args, **kwargs):
        super(MyWebEngineView, self).__init__(*args, **kwargs)
        # 绑定cookie被添加的信号槽
        QWebEngineProfile.defaultProfile().cookieStore().cookieAdded.connect(self.onCookieAdd)
        self.cookies = {}          # 存放cookie字典
 
    def onCookieAdd(self, cookie):                       # 处理cookie添加的事件
        name = cookie.name().data().decode('utf-8')     # 先获取cookie的名字，再把编码处理一下
        value = cookie.value().data().decode('utf-8')   # 先获取cookie值，再把编码处理一下
        self.cookies[name] = value                       # 将cookie保存到字典里
 
    # 获取cookie
    def get_cookie(self):
        cookie_str = ''
        for key, value in self.cookies.items():         # 遍历字典
            cookie_str += (key + '=' + value + ';')     # 将键值对拿出来拼接一下
        return cookie_str                               # 返回拼接好的字符串
 
 
if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = window()
    w.show()
    sys.exit(app.exec_())
'''————————————————
版权声明：本文为CSDN博主「做我的code吧」的原创文章，遵循CC 4.0 BY-SA版权协议，转载请附上原文出处链接及本声明。
原文链接：https://blog.csdn.net/yueguangMaNong/article/details/81146816'''