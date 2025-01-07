from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *

class WorkerSignals(QObject):
    """
    sig = sig(arg type)
    when connect with self.sig.connect(func)
    then func will be invoke if self.sig.emit(arg) is invoke and arg is pass to func
    """
    finished = pyqtSignal()
    error = pyqtSignal(object)
    result = pyqtSignal(object)
    progress = pyqtSignal(int)

class Worker(QRunnable):
    def __init__(self, func, data_tuple: tuple):
        super(Worker, self).__init__()

        # Store constructor arguments (re-used for processing)
        self.func = func
        self.data_tuple = data_tuple
        self.signals = WorkerSignals()

    def run(self):
        result = self.func(self.data_tuple)
