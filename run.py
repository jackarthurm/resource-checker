import logging
import sys

from PySide2.QtWidgets import QMainWindow, QApplication

from resource_checker.model.resource import HTMLWebResource
from resource_checker.model.rules import HTMLContainsTextRule, RuleIntersect
from resource_checker_ui.app import Application
from resource_checker_ui.view.resource_table.delegate import CheckNowButtonDelegate
from resource_checker_ui.view.resource_table.model import ResourceTableModel
from resource_checker_ui.view.resource_table.view import ResourceItemTableView


if __name__ == '__main__':

    logging.basicConfig(level=logging.WARNING)

    app: QApplication = Application(sys.argv)

    switch_dock_resource: HTMLWebResource = HTMLWebResource(
        'Switch dock in stock at nintendo.co.uk?',
        'https://store.nintendo.co.uk/nintendo-switch-accessory/nintendo-switch-dock-set/11'
        '469708.html',
        RuleIntersect(
            HTMLContainsTextRule('Sorry, this product is currently out of stock.'),
            HTMLContainsTextRule('Out of Stock')
        ).negated(),
        'Checks if phrases that indicate the item is out of stock have been removed from the page'
    )

    resource_item_model: ResourceTableModel = ResourceTableModel([switch_dock_resource])

    resource_table_view: ResourceItemTableView = ResourceItemTableView()
    resource_table_view.setModel(resource_item_model)
    resource_table_view.setItemDelegateForColumn(2, CheckNowButtonDelegate())

    main_window: QMainWindow = QMainWindow()
    main_window.setCentralWidget(resource_table_view)

    main_window.show()

    sys.exit(app.exec_())
