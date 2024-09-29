import sys
from PySide6 import QtCore, QtWidgets
import openpyxl
from PySide6.QtWidgets import QVBoxLayout, QPushButton, QFileDialog, QLineEdit, QSplitter, QTableWidgetItem, QHBoxLayout
from preview_layout import PreviewLayout
from settings_layout import SettingsLayout
from result_layout import ResultLayout

class MyWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Scrap io")

        self.splitter = QSplitter(QtCore.Qt.Horizontal)
        self.main_layout = QtWidgets.QVBoxLayout(self)
        
        self.main_layout.addWidget(self.splitter)

        self.preview_layout_widget = PreviewLayout()
        self.settings_layout_widget = SettingsLayout()
        self.result_layout_widget = ResultLayout()

       
        self.settings_layout_widget.file_loaded.connect(self.update_table)
        self.settings_layout_widget.prompt_ready.connect(self.submit)

        self.splitter.addWidget(self.preview_layout_widget)
        self.splitter.addWidget(self.settings_layout_widget)
        self.splitter.addWidget(self.result_layout_widget)

        self.splitter.setStretchFactor(0, 1)
        self.splitter.setStretchFactor(1, 1)
        self.splitter.setStretchFactor(2, 1)

    def update_table(self, list_values):
        table_widget = self.preview_layout_widget.get_table_widget()
        
        table_widget.setColumnCount(len(list_values[0]))
        table_widget.setHorizontalHeaderLabels(list_values[0])

        table_widget.setRowCount(0) 
        for row_index, value_tuple in enumerate(list_values[1:]):
            table_widget.insertRow(row_index)
            for column_index, value in enumerate(value_tuple):
                table_widget.setItem(row_index, column_index, QTableWidgetItem(str(value)))


    def submit(self, queries, prompts, data_rows, mode):
       if mode=='Url':
            print('a')
       elif mode == 'Find url':
           print('b')
           print(prompts,data_rows,mode, queries)



if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = MyWidget()
    widget.resize(1000, 600)
    widget.setFixedSize(1200, 700)
    widget.show()

    sys.exit(app.exec())
