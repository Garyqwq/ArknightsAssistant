import os
import platform
import time
from threading import Thread

from PySide2.QtCore import QCoreApplication, Signal, QObject
from PySide2.QtGui import Qt
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QApplication

from source.tools import stop_thread, log

path = os.path.realpath(os.curdir)


# class LogPrint(QThread):
#     signal = Signal(str)
#
#     def __init__(self, case, msg):
#         super().__init__()
#         self.case = case
#         self.msg = msg
#
#     def log(self):
#         if self.case == 0:
#             pass
#         elif self.case == 1:
#             self.msg = "当前执行: " + self.msg
#         elif self.case == 2:
#             msg = "完成执行: " + self.msg
#         elif self.case == 3:
#             msg = "发生错误: " + self.msg
#         cur_time = time.strftime("%m-%d %H:%M:%S", time.localtime(time.time()))
#         self.msg = cur_time + ": " + self.msg
#
#     def run(self):
#         self.log()
#         self.signal.emit(self.msg)


class LogPrint(QObject):
    log_print = Signal(str)


global_logprint = LogPrint()


def program_start(global_logprint):
    i = 0
    while True:
        global_logprint.log_print.emit("开始" + str(i))
        time.sleep(1)


class Win_Main:

    def __init__(self):
        self.thread = None
        self.ui = QUiLoader().load(path + '/resource/windows/mainwindow.ui')

        # 信号收集
        self.ui.drugcomboBox.currentIndexChanged.connect(self.drugcbox)
        self.ui.stonecomboBox.currentIndexChanged.connect(self.stonecbox)
        self.ui.startbutton.clicked.connect(self.start)
        self.ui.stopbutton.clicked.connect(self.stop)

        global_logprint.log_print.connect(self.printlog)

    def printlog(self, msg):
        self.ui.logBrowser.append(msg)

    def stonecbox(self):
        stone = self.ui.stonecomboBox.currentText()
        msg = log(0, "选择源石：" + stone)
        global_logprint.log_print.emit(msg)

    def drugcbox(self):
        drug = self.ui.drugcomboBox.currentText()
        msg = log(0, "选择理智药：" + drug)
        global_logprint.log_print.emit(msg)

    def startthread(self):
        program_start(global_logprint)

    def start(self):
        self.ui.startbutton.setEnabled(False)
        self.ui.stopbutton.setEnabled(True)
        self.thread = Thread(target=self.startthread)
        self.thread.start()
        print(self.thread.isAlive())

    def stop(self):
        self.ui.stopbutton.setEnabled(False)
        self.ui.startbutton.setEnabled(True)
        # self.thread.join()
        stop_thread(self.thread)
        print(self.thread.isAlive())


def start_ready():
    platforms = platform.platform()
    print(platform.platform())
    if "Darwin" in platforms:
        QCoreApplication.setAttribute(Qt.AA_ShareOpenGLContexts)
        os.environ['QT_MAC_WANTS_LAYER'] = '1'
    elif "Windows" in platforms:
        pass
    elif "Linux" in platforms:
        pass
    else:
        pass


# def info_check():


if __name__ == '__main__':
    start_ready()
    # info_check()
    app = QApplication([])
    mainWin = Win_Main()
    mainWin.ui.show()
    app.exec_()
