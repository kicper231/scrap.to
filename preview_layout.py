import sys
from PySide6 import QtWidgets, QtCore
from PySide6.QtWidgets import QVBoxLayout, QTableWidget, QLabel
from PySide6.QtCore import *
from PySide6.QtGui import *

class PreviewLayout(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.Preview_layout = QVBoxLayout(self)

        self.label_table = QLabel("Podgląd danych")
        self.Preview_layout.addWidget(self.label_table)

        self.table_widget = QTableWidget()
        self.table_widget.setRowCount(20)
        self.Preview_layout.addWidget(self.table_widget)

    def get_table_widget(self):
        return self.table_widget
    
    def keyPressEvent(self, event):
        super().keyPressEvent(event)
        if event.key() == Qt.Key.Key_C and (event.modifiers() & Qt.KeyboardModifier.ControlModifier):
            copied_cells = sorted(self.table_widget.selectedIndexes())

            copy_text = ''
            max_column = copied_cells[-1].column()
            for c in copied_cells:
                copy_text += self.table_widget.item(c.row(), c.column()).text()
                if c.column() == max_column:
                    copy_text += '\n'
                else:
                    copy_text += '\t'
                    
            QtWidgets.QApplication.clipboard().setText(copy_text)
