from typing import List

from PySide2.QtWidgets import QApplication


class Application(QApplication):

    def __init__(self, _argv: List[str]) -> None:
        super(Application, self).__init__()
        self.setApplicationName('Resource checker')
