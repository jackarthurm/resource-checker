from typing import Callable

from PySide2.QtCore import QModelIndex, QRect, QEvent, Qt, QAbstractItemModel
from PySide2.QtGui import QPainter
from PySide2.QtWidgets import (
    QStyledItemDelegate,
    QStyle,
    QStyleOptionViewItem,
    QStyleOptionButton,
    QApplication,
)

from resource_checker_ui.view.resource_table.model import (
    ResourceItemColumn,
    ResourceTableModel,
)


class ButtonStyleStateFlagManager(object):
    """State machine that keeps track of QStyleOptionButton state flags
    Supports
        - sinking (pressed style)
        - raising (opposite of sinking or "un-press")
        - mouse in (hover style)
        - mouse out (opposite of hover or "un-hover")
    """

    def __init__(
        self,
        initial_state: int = QStyle.State_Enabled | QStyle.State_Raised
    ) -> None:
        self._flags: int = initial_state

    def sink(self) -> None:

        if self._flags & QStyle.State_Raised:
            self._flags ^= QStyle.State_Raised

        if not self._flags & QStyle.State_Sunken:
            self._flags |= QStyle.State_Sunken

    def raise_(self) -> None:

        if self._flags & QStyle.State_Sunken:
            self._flags ^= QStyle.State_Sunken

        if not self._flags & QStyle.State_Raised:
            self._flags |= QStyle.State_Raised

    def mouse_in(self) -> None:
        if not self._flags & QStyle.State_MouseOver:
            self._flags |= QStyle.State_MouseOver

    def mouse_out(self) -> None:
        if self._flags & QStyle.State_MouseOver:
            self._flags ^= QStyle.State_MouseOver

    def disable(self) -> None:
        if self._flags & QStyle.State_Enabled:
            self._flags ^= QStyle.State_Enabled

    def enable(self) -> None:
        if not self._flags & QStyle.State_Enabled:
            self._flags |= QStyle.State_Enabled

    @property
    def flags(self) -> int:
        return self._flags


class ButtonDelegate(QStyledItemDelegate):

    def __init__(self, *args, button_text: str, **kwargs):

        super(ButtonDelegate, self).__init__(*args, **kwargs)

        self._button_text: str = button_text
        self._button_style = ButtonStyleStateFlagManager()

    def paint(self, painter: QPainter, option: QStyleOptionViewItem, _index: QModelIndex):

        button: QStyleOptionButton = QStyleOptionButton()
        button.rect: QRect = option.rect
        button.text: str = self._button_text

        if option.state & QStyle.State_Enabled:

            self._button_style.enable()

            if option.state & QStyle.State_MouseOver:
                self._button_style.mouse_in()

            else:
                self._button_style.mouse_out()

        else:
            self._button_style.disable()

        button.state = self._button_style.flags

        QApplication.style().drawControl(QStyle.CE_PushButton, button, painter)

    def editorEvent(
        self,
        evt: QEvent,
        model: QAbstractItemModel,
        option: QStyleOptionViewItem,
        index: QModelIndex
    ) -> bool:

        if evt.button() != Qt.LeftButton:
            return False

        if evt.type() == QEvent.MouseButtonPress:
            self._button_style.sink()

        if evt.type() == QEvent.MouseButtonRelease:
            self._button_style.raise_()

        return True


class CheckNowButtonDelegate(ButtonDelegate):

    def __init__(self, *args, **kwargs):
        super(CheckNowButtonDelegate, self).__init__(*args, button_text='Check', **kwargs)

    def editorEvent(
        self,
        evt: QEvent,
        model: ResourceTableModel,
        option: QStyleOptionViewItem,
        model_index: QModelIndex
    ) -> bool:

        event_handled: bool = super(CheckNowButtonDelegate, self).editorEvent(
            evt,
            model,
            option,
            model_index
        )

        if evt.button() != Qt.LeftButton or evt.type() != QEvent.MouseButtonRelease:
            return event_handled

        check: Callable[[], bool] = model.data(model_index)
        result: bool = check()

        model.setData(
            model_index.siblingAtColumn(
                model.col_index(ResourceItemColumn.CHECK_RESULT)
            ),
            result,
            Qt.DisplayRole
        )

        return True
