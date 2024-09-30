import sys
from PySide6 import QtWidgets, QtCore
from PySide6.QtWidgets import QVBoxLayout, QTableWidget, QLabel, QTextEdit
from PySide6.QtCore import Signal

class ResultLayout(QtWidgets.QWidget):
    

    def __init__(self):
        super().__init__()
        self.result_layout = QVBoxLayout(self)

        self.label_result_table = QLabel("Podgląd wyników")
        self.result_layout.addWidget(self.label_result_table)

        self.result_table_widget = QTableWidget()
        self.result_layout.addWidget(self.result_table_widget)

        self.label_result_text = QLabel("Tekst wynikow")
        self.result_layout.addWidget(self.label_result_text)
        self.result_text_widget = QTextEdit()
        self.result_layout.addWidget(self.result_text_widget)

    def get_result_table_widget(self):
        return self.result_table_widget
    
    def get_text_widget(self):
        return self.result_text_widget