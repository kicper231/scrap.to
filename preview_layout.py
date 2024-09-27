import sys
from PySide6 import QtWidgets, QtCore
from PySide6.QtWidgets import QVBoxLayout, QTableWidget, QLabel

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
