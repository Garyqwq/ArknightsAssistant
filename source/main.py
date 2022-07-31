import os
import platform
from threading import Thread

from PySide2.QtCore import QCoreApplication
from PySide2.QtGui import Qt
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QApplication

from source.Assistant import assistant_start
from source.InfoClass import Assistant_Info, MySignal
from source.Tools import stop_thread, log

path = os.path.realpath(os.curdir)

global_signal = MySignal()
assistant_info = Assistant_Info()


class Win_Main:

    def __init__(self):
        self.thread = None
        self.ui = QUiLoader().load(path + '/resource/windows/mainwindow.ui')

        # 信号收集
        # 左上
        self.ui.wakeup.stateChanged.connect(self.wakeup_check)
        self.ui.fighting.stateChanged.connect(self.fighting_check)

        # 左下
        self.ui.startbutton.clicked.connect(self.start)
        self.ui.stopbutton.clicked.connect(self.stop)

        # 中部
        self.ui.drugcomboBox.currentIndexChanged.connect(self.drugcbox)
        self.ui.stonecomboBox.currentIndexChanged.connect(self.stonecbox)


        # 外部信号槽
        global_signal.log_print.connect(self.printlog)
        global_signal.error.connect(self.error)

    def error(self):
        stop_thread(self.thread)

    def printlog(self, msg):
        self.ui.logBrowser.append(msg)

    def checkbox(self, ui):
        check = ui.text()
        if ui.checkState() == Qt.CheckState.Unchecked:
            msg = log(0, "取消任务：" + check)
        else:
            msg = log(0, "选择任务：" + check)
        global_signal.log_print.emit(msg)

    def wakeup_check(self):
        self.checkbox(self.ui.wakeup)

    def fighting_check(self):
        self.checkbox(self.ui.fighting)

    def stonecbox(self):
        stone = self.ui.stonecomboBox.currentText()
        msg = log(0, "选择源石：" + stone)
        global_signal.log_print.emit(msg)

    def drugcbox(self):
        drug = self.ui.drugcomboBox.currentText()
        msg = log(0, "选择理智药：" + drug)
        global_signal.log_print.emit(msg)

    def startthread(self):
        assistant_info.pickle_set()
        assistant_start(global_signal)

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
