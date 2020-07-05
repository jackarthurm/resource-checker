from PySide2.QtWidgets import QMainWindow


class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs) -> None:
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setWindowTitle('Resource checker')
