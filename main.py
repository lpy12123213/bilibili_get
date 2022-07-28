import re
import pyperclip
import os
import subprocess
import requests
import time
# from open1 import*
from download import *
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QUrl, pyqtSignal
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineProfile
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton
import json
import sys
import threading as thread  # 导入线程模块, 之后要用

# 变量提前定义
path = os.getcwd()
os.chdir(path)
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) \
        Chrome/100.0.4896.127 Safari/537.36 Edg/100.0.1185.44',
}


# 变量提前定义


class Window1(QWidget):
    def __init__(self):
        self.cookie = ''
        super().__init__()
        self.setup()

    def setup(self):
        self.box = QVBoxLayout(self)  # 创建一个垂直布局来放控件
        self.btn_get = QPushButton('点击获取cookies')  # 创建一个按钮涌来了点击获取cookie
        self.btn_get.clicked.connect(self.get_cookie)  # 绑定按钮点击事件
        self.web = MyWebEngineView()  # 创建浏览器组件对象
        self.web.resize(800, 600)  # 设置大小
        self.web.load(QUrl("https://www.bilibili.com"))  # 打开百度页面来测试
        self.box.addWidget(self.btn_get)  # 将组件放到布局内，先在顶部放一个按钮
        self.box.addWidget(self.web)  # 再放浏览器
        self.web.show()  # 最后让页面显示出来

    def get_cookie(self):
        cookie = self.web.get_cookie()
        self.cookie = cookie


# 创建自己的浏览器控件，继承自QWebEngineView
class MyWebEngineView(QWebEngineView):
    # web
    # it's one of sub windows
    # 自 https://blog.csdn.net/yueguangMaNong/article/details/81146816 修改
    # 自 https://blog.csdn.net/he_yang_/article/details/103788918 修改
    show_main_win_signal = pyqtSignal()

    def __init__(self, *args, **kwargs):
        super(MyWebEngineView, self).__init__(*args, **kwargs)
        # 绑定cookie被添加的信号槽
        QWebEngineProfile.defaultProfile().cookieStore().cookieAdded.connect(self.onCookieAdd)
        self.cookies = {}  # 存放cookie字典

    def onCookieAdd(self, cookie):  # 处理cookie添加的事件
        name = cookie.name().data().decode('utf-8')  # 先获取cookie的名字，再把编码处理一下
        value = cookie.value().data().decode('utf-8')  # 先获取cookie值，再把编码处理一下
        self.cookies[name] = value  # 将cookie保存到字典里

    def go_main(self):
        self.show_main_win_signal.emit()

    # 获取cookie
    def get_cookie(self):
        cookie_str = ''
        for key, value in self.cookies.items():  # 遍历字典
            cookie_str += (key + '=' + value + ';')  # 将键值对拿出来拼接一下
        return cookie_str


# def doit_():
#     # my_application = QApplication(sys.argv)  # 创建QApplication类的实例
#     main_demo = Window1()
#     main_demo.show()
#     app.exec_()
#     self.cookie = main_demo.cookie


class Ui_bilibili_get(object):
    # main window
    show_main_win_signal = pyqtSignal()
    header = headers

    def setupUi(self, bilibili_get):
        bilibili_get.setObjectName("bilibili_get")
        bilibili_get.resize(1072, 652)
        bilibili_get.setStyleSheet("QPushButton {\n"
                                   "    color: red;\n"
                                   "    font-size: 20;\n"
                                   "}\n"
                                   "QLineEdit {\n"
                                   "    color: blue;\n"
                                   "    font-size: 20;\n"
                                   "}\n"
                                   "tabWidget{\n"
                                   "    color: green;\n"
                                   "    font-size: 15px;\n"
                                   "}")
        self.tabWidget = QtWidgets.QTabWidget(bilibili_get)
        self.tabWidget.setGeometry(QtCore.QRect(0, 0, 1071, 651))
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.bv_line = QtWidgets.QLineEdit(self.tab)
        self.bv_line.setGeometry(QtCore.QRect(110, 90, 761, 31))
        self.bv_line.setObjectName("bv_line")
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.tab)
        self.horizontalLayoutWidget.setGeometry(
            QtCore.QRect(100, 200, 781, 81))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(
            self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.sure_button = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.sure_button.setStyleSheet("")
        self.sure_button.setFlat(True)
        self.sure_button.setObjectName("sure_button")
        self.horizontalLayout.addWidget(self.sure_button)
        self.unsure_button = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.unsure_button.setStyleSheet("")
        self.unsure_button.setFlat(True)
        self.unsure_button.setObjectName("unsure_button")
        self.horizontalLayout.addWidget(self.unsure_button)
        self.cookie_button = QtWidgets.QPushButton(self.tab)
        self.cookie_button.setGeometry(QtCore.QRect(110, 150, 141, 41))
        self.cookie_button.setFlat(True)
        self.cookie_button.setObjectName("cookie_button")
        self.ztl = QtWidgets.QTextEdit(self.tab)
        self.ztl.setGeometry(QtCore.QRect(110, 310, 771, 241))
        self.ztl.setObjectName("ztl")
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.label_2 = QtWidgets.QLabel(self.tab_2)
        self.label_2.setGeometry(QtCore.QRect(340, 10, 69, 20))
        self.label_2.setObjectName("label_2")
        self.bv_num = QtWidgets.QLabel(self.tab_2)
        self.bv_num.setGeometry(QtCore.QRect(420, 10, 271, 20))
        self.bv_num.setObjectName("bv_num")
        self.jiexi = QtWidgets.QLabel(self.tab_2)
        self.jiexi.setGeometry(QtCore.QRect(30, 130, 69, 20))
        self.jiexi.setObjectName("jiexi")
        self.horizontalLayoutWidget_2 = QtWidgets.QWidget(self.tab_2)
        self.horizontalLayoutWidget_2.setGeometry(
            QtCore.QRect(500, 520, 271, 31))
        self.horizontalLayoutWidget_2.setObjectName("horizontalLayoutWidget_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(
            self.horizontalLayoutWidget_2)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.downchoice = QtWidgets.QPushButton(self.horizontalLayoutWidget_2)
        self.downchoice.setStyleSheet("*{\n"
                                      "    color: #13FF09;\n"
                                      "}")
        self.downchoice.setFlat(True)
        self.downchoice.setObjectName("downchoice")
        self.horizontalLayout_2.addWidget(self.downchoice)
        self.downall = QtWidgets.QPushButton(self.horizontalLayoutWidget_2)
        self.downall.setStyleSheet("*{\n"
                                   "    color: #13FF09;\n"
                                   "}")
        self.downall.setFlat(True)
        self.downall.setObjectName("downall")
        self.horizontalLayout_2.addWidget(self.downall)
        self.textEdit = QtWidgets.QTextEdit(self.tab_2)
        self.textEdit.setGeometry(QtCore.QRect(30, 160, 1031, 351))
        self.textEdit.setObjectName("textEdit")
        self.gridLayoutWidget = QtWidgets.QWidget(self.tab_2)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(30, 40, 1021, 80))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 1, 0, 1, 1)
        self.Title = QtWidgets.QLabel(self.gridLayoutWidget)
        self.Title.setObjectName("Title")
        self.gridLayout.addWidget(self.Title, 0, 0, 1, 1)
        self.Title_name = QtWidgets.QLabel(self.gridLayoutWidget)
        self.Title_name.setObjectName("Title_name")
        self.gridLayout.addWidget(self.Title_name, 0, 1, 1, 1)
        self.desc_info = QtWidgets.QLabel(self.gridLayoutWidget)
        self.desc_info.setObjectName("desc_info")
        self.gridLayout.addWidget(self.desc_info, 1, 1, 1, 1)
        self.tabWidget.addTab(self.tab_2, "")
        self.tab_3 = QtWidgets.QWidget()
        self.tab_3.setObjectName("tab_3")
        self.label_3 = QtWidgets.QLabel(self.tab_3)
        self.label_3.setGeometry(QtCore.QRect(320, 0, 69, 20))
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.wvideo = QtWidgets.QLabel(self.tab_3)
        self.wvideo.setGeometry(QtCore.QRect(0, 110, 69, 20))
        self.wvideo.setObjectName("wvideo")
        self.verticalLayoutWidget_2 = QtWidgets.QWidget(self.tab_3)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(0, 20, 791, 85))
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(
            self.verticalLayoutWidget_2)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.writer_id = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        self.writer_id.setObjectName("writer_id")
        self.verticalLayout_3.addWidget(self.writer_id)
        self.writer_info = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        self.writer_info.setObjectName("writer_info")
        self.verticalLayout_3.addWidget(self.writer_info)
        self.goto_writer = QtWidgets.QPushButton(self.verticalLayoutWidget_2)
        self.goto_writer.setStyleSheet("*{\n"
                                       "color: #0913FA\n"
                                       "}")
        self.goto_writer.setFlat(True)
        self.goto_writer.setObjectName("goto_writer")
        self.verticalLayout_3.addWidget(self.goto_writer)
        self.horizontalLayoutWidget_3 = QtWidgets.QWidget(self.tab_3)
        self.horizontalLayoutWidget_3.setGeometry(
            QtCore.QRect(490, 530, 291, 31))
        self.horizontalLayoutWidget_3.setObjectName("horizontalLayoutWidget_3")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(
            self.horizontalLayoutWidget_3)
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.dchoice = QtWidgets.QPushButton(self.horizontalLayoutWidget_3)
        self.dchoice.setObjectName("dchoice")
        self.horizontalLayout_5.addWidget(self.dchoice)
        self.dall = QtWidgets.QPushButton(self.horizontalLayoutWidget_3)
        self.dall.setObjectName("dall")
        self.horizontalLayout_5.addWidget(self.dall)
        self.tableWidget_3 = QtWidgets.QTableWidget(self.tab_3)
        self.tableWidget_3.setGeometry(QtCore.QRect(10, 140, 1051, 371))
        self.tableWidget_3.setObjectName("tableWidget_3")
        self.tableWidget_3.setColumnCount(2)
        self.tableWidget_3.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_3.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_3.setHorizontalHeaderItem(1, item)
        self.tabWidget.addTab(self.tab_3, "")
        self.tab_4 = QtWidgets.QWidget()
        self.tab_4.setObjectName("tab_4")
        self.tableWidget = QtWidgets.QTableWidget(self.tab_4)
        self.tableWidget.setGeometry(QtCore.QRect(0, 0, 1061, 601))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(8)
        self.tableWidget.setRowCount(60)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(6, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(7, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(8, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(9, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(10, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(11, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(12, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(13, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(14, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(15, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(16, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(17, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(18, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(19, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(20, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(21, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(22, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(23, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(24, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(25, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(26, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(27, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(28, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(29, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(30, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(31, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(32, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(33, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(34, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(35, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(36, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(37, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(38, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(39, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(40, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(41, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(42, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(43, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(44, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(45, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(46, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(47, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(48, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(49, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(50, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(51, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(52, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(53, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(54, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(55, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(56, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(57, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(58, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(59, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(6, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(7, item)
        self.tabWidget.addTab(self.tab_4, "")
        self.tab_5 = QtWidgets.QWidget()
        self.tab_5.setStyleSheet("pushButton{\n"
                                 "    color: #070608;\n"
                                 "};")
        self.tab_5.setObjectName("tab_5")
        self.pushButton = QtWidgets.QPushButton(self.tab_5)
        self.pushButton.setGeometry(QtCore.QRect(960, 10, 93, 29))
        self.pushButton.setStyleSheet("*{\n"
                                      "    color: #070608;\n"
                                      "}")
        self.pushButton.setFlat(True)
        self.pushButton.setObjectName("pushButton")
        self.lineEdit = QtWidgets.QLineEdit(self.tab_5)
        self.lineEdit.setGeometry(QtCore.QRect(790, 10, 158, 21))
        self.lineEdit.setFrame(False)
        self.lineEdit.setDragEnabled(False)
        self.lineEdit.setReadOnly(False)
        self.lineEdit.setClearButtonEnabled(True)
        self.lineEdit.setObjectName("lineEdit")
        self.tableWidget_2 = QtWidgets.QTableWidget(self.tab_5)
        self.tableWidget_2.setGeometry(QtCore.QRect(0, 40, 1071, 511))
        self.tableWidget_2.setObjectName("tableWidget_2")
        self.tableWidget_2.setColumnCount(0)
        self.tableWidget_2.setRowCount(0)
        self.horizontalLayoutWidget_4 = QtWidgets.QWidget(self.tab_5)
        self.horizontalLayoutWidget_4.setGeometry(
            QtCore.QRect(750, 550, 311, 41))
        self.horizontalLayoutWidget_4.setObjectName("horizontalLayoutWidget_4")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(
            self.horizontalLayoutWidget_4)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.pushButton_2 = QtWidgets.QPushButton(
            self.horizontalLayoutWidget_4)
        self.pushButton_2.setFlat(True)
        self.pushButton_2.setObjectName("pushButton_2")
        self.horizontalLayout_3.addWidget(self.pushButton_2)
        self.pushButton_3 = QtWidgets.QPushButton(
            self.horizontalLayoutWidget_4)
        self.pushButton_3.setFlat(True)
        self.pushButton_3.setObjectName("pushButton_3")
        self.horizontalLayout_3.addWidget(self.pushButton_3)
        self.tabWidget.addTab(self.tab_5, "")

        self.retranslateUi(bilibili_get)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(bilibili_get)
        self.cookie_button.clicked.connect(self.open_web)
        self.sure_button.clicked.connect(self.d)
        self.unsure_button.clicked.connect(self.killer)

    def open_web(self):
        if os.path.exists('.\\cookie.json'):
            with open('.\\cookie.json') as f:
                try:
                    self.cookie = json.load(f)
                except:
                    self.ztl.append("cookie.json文件错误，请重新获取cookie")
                    return
                self.header['cookie'] = self.cookie
            self.ztl.append("已获取cookie")
            if self.cookie != '':
                return
        def _():
            self.ztl.append("！！请关闭此程序后打开open1.py文件并获得cookie，之后重新打开此文件！！")
            sys.exit()
        t = thread.Thread(target=_)
        t.start()

    # def go_sub(self):
    #     self.show_sub_win_signal.emit()

    def d(self):
        def _():
            self.bv = self.bv_line.text()
            p = download_video(self.bv, headers=self.header)
            if self.bv[:2].lower() == 'av':
                mode = "AV"
            else:
                mode = "BV"
            if p == 0:
                self.ztl.append(f"{mode}号为{self.bv}的视频下载完成")
            else:
                self.ztl.append(f"{mode}号为{self.bv}的视频下载失败")

        do = thread.Thread(target=_)
        do.start()
        del _
    def killer(self):
        def _():
            kill()
        t = thread.Thread(target=_)
        t.start()

    def retranslateUi(self, bilibili_get):
        _translate = QtCore.QCoreApplication.translate
        bilibili_get.setWindowTitle(_translate("bilibili_get", "Widget"))
        self.bv_line.setText(_translate("bilibili_get", "bv号"))
        self.sure_button.setText(_translate("bilibili_get", "确定"))
        self.unsure_button.setText(_translate("bilibili_get", "取消"))
        self.cookie_button.setText(_translate("bilibili_get", "获得cookie"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(
            self.tab), _translate("bilibili_get", "主页"))
        self.label_2.setText(_translate("bilibili_get", "解析"))
        self.bv_num.setText(_translate("bilibili_get", "bv_num"))
        self.jiexi.setText(_translate("bilibili_get", "解析列表"))
        self.downchoice.setText(_translate("bilibili_get", "下载选中"))
        self.downall.setText(_translate("bilibili_get", "下载全部"))
        self.label.setText(_translate("bilibili_get", "Desc"))
        self.Title.setText(_translate("bilibili_get", "Title:"))
        self.Title_name.setText(_translate("bilibili_get", "Title"))
        self.desc_info.setText(_translate("bilibili_get", "Desc"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(
            self.tab_2), _translate("bilibili_get", "解析"))
        self.label_3.setText(_translate("bilibili_get", "作者"))
        self.wvideo.setText(_translate("bilibili_get", "视频列表"))
        self.writer_id.setText(_translate("bilibili_get", "id："))
        self.writer_info.setText(_translate("bilibili_get", "简介"))
        self.goto_writer.setText(_translate("bilibili_get", "去他主页"))
        self.dchoice.setText(_translate("bilibili_get", "下载选中"))
        self.dall.setText(_translate("bilibili_get", "下载所有"))
        item = self.tableWidget_3.horizontalHeaderItem(0)
        item.setText(_translate("bilibili_get", "标题"))
        item = self.tableWidget_3.horizontalHeaderItem(1)
        item.setText(_translate("bilibili_get", "状态"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(
            self.tab_3), _translate("bilibili_get", "作者"))
        item = self.tableWidget.verticalHeaderItem(0)
        item.setText(_translate("bilibili_get", "1"))
        item = self.tableWidget.verticalHeaderItem(1)
        item.setText(_translate("bilibili_get", "2"))
        item = self.tableWidget.verticalHeaderItem(2)
        item.setText(_translate("bilibili_get", "3"))
        item = self.tableWidget.verticalHeaderItem(3)
        item.setText(_translate("bilibili_get", "4"))
        item = self.tableWidget.verticalHeaderItem(4)
        item.setText(_translate("bilibili_get", "5"))
        item = self.tableWidget.verticalHeaderItem(5)
        item.setText(_translate("bilibili_get", "6"))
        item = self.tableWidget.verticalHeaderItem(6)
        item.setText(_translate("bilibili_get", "7"))
        item = self.tableWidget.verticalHeaderItem(7)
        item.setText(_translate("bilibili_get", "8"))
        item = self.tableWidget.verticalHeaderItem(8)
        item.setText(_translate("bilibili_get", "9"))
        item = self.tableWidget.verticalHeaderItem(9)
        item.setText(_translate("bilibili_get", "10"))
        item = self.tableWidget.verticalHeaderItem(10)
        item.setText(_translate("bilibili_get", "11"))
        item = self.tableWidget.verticalHeaderItem(11)
        item.setText(_translate("bilibili_get", "12"))
        item = self.tableWidget.verticalHeaderItem(12)
        item.setText(_translate("bilibili_get", "13"))
        item = self.tableWidget.verticalHeaderItem(13)
        item.setText(_translate("bilibili_get", "14"))
        item = self.tableWidget.verticalHeaderItem(14)
        item.setText(_translate("bilibili_get", "15"))
        item = self.tableWidget.verticalHeaderItem(15)
        item.setText(_translate("bilibili_get", "16"))
        item = self.tableWidget.verticalHeaderItem(16)
        item.setText(_translate("bilibili_get", "17"))
        item = self.tableWidget.verticalHeaderItem(17)
        item.setText(_translate("bilibili_get", "18"))
        item = self.tableWidget.verticalHeaderItem(18)
        item.setText(_translate("bilibili_get", "19"))
        item = self.tableWidget.verticalHeaderItem(19)
        item.setText(_translate("bilibili_get", "20"))
        item = self.tableWidget.verticalHeaderItem(20)
        item.setText(_translate("bilibili_get", "21"))
        item = self.tableWidget.verticalHeaderItem(21)
        item.setText(_translate("bilibili_get", "22"))
        item = self.tableWidget.verticalHeaderItem(22)
        item.setText(_translate("bilibili_get", "23"))
        item = self.tableWidget.verticalHeaderItem(23)
        item.setText(_translate("bilibili_get", "24"))
        item = self.tableWidget.verticalHeaderItem(24)
        item.setText(_translate("bilibili_get", "25"))
        item = self.tableWidget.verticalHeaderItem(25)
        item.setText(_translate("bilibili_get", "26"))
        item = self.tableWidget.verticalHeaderItem(26)
        item.setText(_translate("bilibili_get", "27"))
        item = self.tableWidget.verticalHeaderItem(27)
        item.setText(_translate("bilibili_get", "28"))
        item = self.tableWidget.verticalHeaderItem(28)
        item.setText(_translate("bilibili_get", "29"))
        item = self.tableWidget.verticalHeaderItem(29)
        item.setText(_translate("bilibili_get", "30"))
        item = self.tableWidget.verticalHeaderItem(30)
        item.setText(_translate("bilibili_get", "31"))
        item = self.tableWidget.verticalHeaderItem(31)
        item.setText(_translate("bilibili_get", "32"))
        item = self.tableWidget.verticalHeaderItem(32)
        item.setText(_translate("bilibili_get", "33"))
        item = self.tableWidget.verticalHeaderItem(33)
        item.setText(_translate("bilibili_get", "34"))
        item = self.tableWidget.verticalHeaderItem(34)
        item.setText(_translate("bilibili_get", "35"))
        item = self.tableWidget.verticalHeaderItem(35)
        item.setText(_translate("bilibili_get", "36"))
        item = self.tableWidget.verticalHeaderItem(36)
        item.setText(_translate("bilibili_get", "37"))
        item = self.tableWidget.verticalHeaderItem(37)
        item.setText(_translate("bilibili_get", "38"))
        item = self.tableWidget.verticalHeaderItem(38)
        item.setText(_translate("bilibili_get", "39"))
        item = self.tableWidget.verticalHeaderItem(39)
        item.setText(_translate("bilibili_get", "40"))
        item = self.tableWidget.verticalHeaderItem(40)
        item.setText(_translate("bilibili_get", "41"))
        item = self.tableWidget.verticalHeaderItem(41)
        item.setText(_translate("bilibili_get", "42"))
        item = self.tableWidget.verticalHeaderItem(42)
        item.setText(_translate("bilibili_get", "43"))
        item = self.tableWidget.verticalHeaderItem(43)
        item.setText(_translate("bilibili_get", "44"))
        item = self.tableWidget.verticalHeaderItem(44)
        item.setText(_translate("bilibili_get", "45"))
        item = self.tableWidget.verticalHeaderItem(45)
        item.setText(_translate("bilibili_get", "46"))
        item = self.tableWidget.verticalHeaderItem(46)
        item.setText(_translate("bilibili_get", "47"))
        item = self.tableWidget.verticalHeaderItem(47)
        item.setText(_translate("bilibili_get", "48"))
        item = self.tableWidget.verticalHeaderItem(48)
        item.setText(_translate("bilibili_get", "49"))
        item = self.tableWidget.verticalHeaderItem(49)
        item.setText(_translate("bilibili_get", "50"))
        item = self.tableWidget.verticalHeaderItem(50)
        item.setText(_translate("bilibili_get", "51"))
        item = self.tableWidget.verticalHeaderItem(51)
        item.setText(_translate("bilibili_get", "52"))
        item = self.tableWidget.verticalHeaderItem(52)
        item.setText(_translate("bilibili_get", "53"))
        item = self.tableWidget.verticalHeaderItem(53)
        item.setText(_translate("bilibili_get", "54"))
        item = self.tableWidget.verticalHeaderItem(54)
        item.setText(_translate("bilibili_get", "55"))
        item = self.tableWidget.verticalHeaderItem(55)
        item.setText(_translate("bilibili_get", "56"))
        item = self.tableWidget.verticalHeaderItem(56)
        item.setText(_translate("bilibili_get", "57"))
        item = self.tableWidget.verticalHeaderItem(57)
        item.setText(_translate("bilibili_get", "58"))
        item = self.tableWidget.verticalHeaderItem(58)
        item.setText(_translate("bilibili_get", "59"))
        item = self.tableWidget.verticalHeaderItem(59)
        item.setText(_translate("bilibili_get", "60"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("bilibili_get", "文件名"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("bilibili_get", "所需时间"))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("bilibili_get", "速度"))
        item = self.tableWidget.horizontalHeaderItem(3)
        item.setText(_translate("bilibili_get", "状态"))
        item = self.tableWidget.horizontalHeaderItem(4)
        item.setText(_translate("bilibili_get", "序号"))
        item = self.tableWidget.horizontalHeaderItem(5)
        item.setText(_translate("bilibili_get", "cid"))
        item = self.tableWidget.horizontalHeaderItem(6)
        item.setText(_translate("bilibili_get", "bv"))
        item = self.tableWidget.horizontalHeaderItem(7)
        item.setText(_translate("bilibili_get", "av"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(
            self.tab_4), _translate("bilibili_get", "下载列表"))
        self.pushButton.setText(_translate("bilibili_get", "确定"))
        self.lineEdit.setText(_translate("bilibili_get", "搜索内容"))
        self.pushButton_2.setText(_translate("bilibili_get", "下载全部"))
        self.pushButton_3.setText(_translate("bilibili_get", "下载选中"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(
            self.tab_5), _translate("bilibili_get", "搜索列表"))


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui=Ui_bilibili_get()

    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
