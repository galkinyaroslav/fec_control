from PySide6.QtCore import QObject, Signal, QRunnable, Slot


class WorkerSignals(QObject):
    finished = Signal(object, object, object, object)


class Worker(QRunnable):
    def __init__(self, *args, **kwargs):
        super().__init__()
        self.args = args
        self.kwargs = kwargs
        self.run_func = kwargs['run_func']
        self.button_name = kwargs['button_name']
        self.kwargs.pop('button_name')
        self.kwargs.pop('run_func')
        # self.command = command
        self.signals = WorkerSignals()
        # print(f'{args=},{kwargs=}')

    @Slot()
    def run(self):
        result = self.run_func(*self.args, **self.kwargs)
        self.signals.finished.emit(self.run_func, self.button_name, result, self.kwargs)
