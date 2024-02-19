from PySide6.QtCore import QObject, Signal, QRunnable, Slot


class WorkerSignals(QObject):
    finished = Signal(object, object, object)


class Worker(QRunnable):
    def __init__(self, *args, **kwargs):
        super().__init__()
        self.args = args
        self.kwargs = kwargs
        self.fec_func = kwargs['fec_func']
        self.kwargs.pop('fec_func')
        # self.command = command
        self.signals = WorkerSignals()
        # print(f'{args=},{kwargs=}')

    @Slot()
    def run(self):
        result = self.fec_func(*self.args, **self.kwargs)
        self.signals.finished.emit(self.fec_func, result, self.kwargs)