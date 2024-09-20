from PySide6.QtCore import Qt
from PySide6.QtGui import QStandardItemModel, QStandardItem
from PySide6.QtWidgets import QComboBox


class MultiSelectComboBox(QComboBox):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.parent = parent

        self.setModel(QStandardItemModel(self))

        self.view().pressed.connect(self.handle_item_pressed)

        self.selected_items = []

    def add_checkable_item(self, text):
        item = QStandardItem(text)
        item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
        item.setCheckState(Qt.Unchecked)
        self.model().appendRow(item)

    def handle_item_pressed(self, index):
        item = self.model().itemFromIndex(index)
        if item.checkState() == Qt.Checked:
            item.setCheckState(Qt.Unchecked)
        else:
            item.setCheckState(Qt.Checked)

        self.update_selected_items()
        self.parent.on_option_selected(self.parent.items[item.text()])

    def update_selected_items(self):
        selected_texts = []
        for i in range(self.model().rowCount()):
            item = self.model().item(i)
            if item.checkState() == Qt.Checked:
                selected_texts.append(item.text())

        self.selected_items = selected_texts
        self.setEditText(", ".join(selected_texts))
