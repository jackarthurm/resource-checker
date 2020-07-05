from PySide2.QtWidgets import QTableView


class HorizontalHeaderTableView(QTableView):

    def __init__(self, *args, **kwargs) -> None:
        super(HorizontalHeaderTableView, self).__init__(*args, **kwargs)

        self.setCornerButtonEnabled(False)
        self.verticalHeader().hide()


class ResourceItemTableView(QTableView):

    def __init__(self, *args, **kwargs) -> None:
        super(ResourceItemTableView, self).__init__(*args, **kwargs)

        self.setMouseTracking(True)
