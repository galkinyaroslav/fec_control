from PySide6.QtCore import QObject, Signal, QRunnable, Slot


class WorkerSignals(QObject):
    finished = Signal(object, object, object, object)
    end = Signal(object)
    broken = Signal()


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
        self._stop_flag = False  #

        # print(f'{args=},{kwargs=}')
    def stop(self):
        """Выставляет флаг остановки"""
        self._stop_flag = True
        self.signals.broken.emit()

    @Slot()
    def run(self):
        result = self.run_func(*self.args, **self.kwargs)
        if not self._stop_flag:
            self.signals.finished.emit(self.run_func, self.button_name, result, self.kwargs)
        else:
            self.signals.end.emit(self.button_name)
        self._stop_flag = False

