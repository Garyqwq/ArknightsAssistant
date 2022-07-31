import os
import pickle

from PySide2.QtCore import QObject, Signal

path = os.path.realpath(os.curdir)


class MySignal(QObject):
    log_print = Signal(str)

    error = Signal()


class Settings_Info:
    # 软件平台和模拟器平台
    sys_platform = 0
    game_platform = 0


class Assistant_Info:

    def __init__(self):
        self.todo_list = [False, False, False, False, False, False, False, False]
        self.drug = 0
        self.stone = 0
        self.activity = ""
        self.game = 0

    def pickle_set(self):
        with open(file=path + '/resource/data/assistant.pickle', mode="wb") as f:
            assistant = {'todo_list': self.todo_list,
                         'drug': self.drug,
                         'stone': self.stone,
                         'activity': self.activity,
                         'game': self.game}
            pickle.dump(assistant, f)

    def pickle_get(self):
        with open(file=path + '/resource/data/assistant.pickle', mode="rb") as f:
            assistant = pickle.load(f)
            # assistant = pickle.loads(assistant_b)
        return assistant
