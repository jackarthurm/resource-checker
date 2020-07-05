from dataclasses import dataclass
from enum import IntEnum, auto
from typing import List, Optional, Union, Any, Tuple, Callable

from PySide2.QtCore import QModelIndex, Qt, QAbstractTableModel

from resource_checker.model.resource import Resource


class ResourceItemColumn(IntEnum):
    NAME = auto()
    DESCRIPTION = auto()
    CHECK_ACTION = auto()
    CHECK_RESULT = auto()


@dataclass
class ResourceItem(object):
    resource: Resource
    cached_result: Optional[bool] = None


ItemColumn = int


class AbstractTableModel(QAbstractTableModel):

    COLUMNS: List[Tuple[str, ItemColumn]]

    def col_index(self, col: ItemColumn) -> int:

        idx: int = list(zip(*self.COLUMNS))[1].index(col)

        if idx >= 0:
            return idx

        raise IndexError('Invalid column')


class ResourceTableModel(AbstractTableModel):

    COLUMNS: List[Tuple[str, ResourceItemColumn]] = [
        ('Name', ResourceItemColumn.NAME),
        ('Description', ResourceItemColumn.DESCRIPTION),
        ('', ResourceItemColumn.CHECK_ACTION),
        ('Result', ResourceItemColumn.CHECK_RESULT),
    ]

    def __init__(self, resources: List[Resource]) -> None:
        super(ResourceTableModel, self).__init__()
        self._resources: List[ResourceItem] = [ResourceItem(r) for r in resources]

    def rowCount(self, *args, **kwargs) -> int:
        return len(self._resources)

    def columnCount(self, *args, **kwargs) -> int:
        return len(self.COLUMNS)

    def headerData(
        self,
        section: int,
        orientation: Qt.Orientation,
        role: Qt.ItemDataRole = Qt.DisplayRole
    ) -> Optional[str]:

        if orientation == Qt.Vertical or role != Qt.DisplayRole:
            return

        return self.COLUMNS[section][0]

    def data(
        self,
        index: QModelIndex = QModelIndex(),
        role: Qt.ItemDataRole = Qt.DisplayRole
    ) -> Union[Optional[str], Callable[[], bool]]:

        if not index.isValid() or role != Qt.DisplayRole:
            return

        item: ResourceItem = self._resources[index.row()]

        column: ResourceItemColumn = self.COLUMNS[index.column()][1]

        if column == ResourceItemColumn.NAME:
            return item.resource.name

        if column == ResourceItemColumn.DESCRIPTION:
            return item.resource.description or ''

        if column == ResourceItemColumn.CHECK_ACTION:
            return item.resource.check

        if column == ResourceItemColumn.CHECK_RESULT:
            if item.cached_result is None:
                return

            return 'true' if item.cached_result else 'false'

    def setData(
        self,
        index: QModelIndex = QModelIndex(),
        value: Any = None,
        role: Qt.ItemDataRole = Qt.DisplayRole
    ) -> bool:

        if not index.isValid() or role != Qt.DisplayRole:
            return False

        column: ResourceItemColumn = self.COLUMNS[index.column()][1]

        if column != ResourceItemColumn.CHECK_RESULT:
            return False

        self._resources[index.row()].cached_result = value

        self.dataChanged.emit(index, index)
        return True
