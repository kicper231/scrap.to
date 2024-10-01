import sys
from PySide6 import QtCore, QtWidgets
import openpyxl
from PySide6.QtWidgets import QVBoxLayout, QPushButton, QFileDialog, QLineEdit, QSplitter, QTableWidgetItem, QHBoxLayout
from preview_layout import PreviewLayout
from settings_layout import SettingsLayout
from result_layout import ResultLayout
from scraper_engine import SmartScraper
import os 
import json
import csv
import io




class MyWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Scrap io")

        self.max_rows = 0
        self.current_row = 1

        self.splitter = QSplitter(QtCore.Qt.Horizontal)
        self.main_layout = QtWidgets.QVBoxLayout(self)
        
        self.main_layout.addWidget(self.splitter)

        self.preview_layout_widget = PreviewLayout()
        self.settings_layout_widget = SettingsLayout()
        self.result_layout_widget = ResultLayout()
        self.test_button = QPushButton()
        self.test_button.clicked.connect(self.test_action)
        
        self.settings_layout_widget.file_loaded.connect(self.update_preview_table)
        self.settings_layout_widget.result_ready.connect(self.update_result_table)
        self.settings_layout_widget.result_partial_ready.connect(self.result_partial_ready)
        self.settings_layout_widget.result_reset.connect(self.result_reset)
        
        self.splitter.addWidget(self.preview_layout_widget)
        self.splitter.addWidget(self.settings_layout_widget)
        self.splitter.addWidget(self.result_layout_widget)
        self.splitter.addWidget(self.test_button)

        self.splitter.setStretchFactor(0, 1)
        self.splitter.setStretchFactor(1, 1)
        self.splitter.setStretchFactor(2, 1)
        self.splitter.setStretchFactor(3, 1)

    def update_preview_table(self, list_values):
        self.settings_layout_widget.result_reset.emit()
        self.settings_layout_widget.prompt_text_edit.setText('')
        self.settings_layout_widget.query_text_edit.setText('')
        table_widget = self.preview_layout_widget.get_table_widget()
        
        table_widget.setColumnCount(len(list_values[0]))
        table_widget.setHorizontalHeaderLabels(list_values[0])

        table_widget.setRowCount(0) 
        for row_index, value_tuple in enumerate(list_values[1:]):
            table_widget.insertRow(row_index)
            for column_index, value in enumerate(value_tuple):
                table_widget.setItem(row_index, column_index, QTableWidgetItem(str(value)))

        self.max_rows = len(list_values)-1


    def update_result_table(self, result):
        text_result_widget = self.result_layout_widget.get_text_widget()
        table_result_widget = self.result_layout_widget.get_result_table_widget()
        parsed_json_list = result
        table_result_widget.setColumnCount(0)

        if parsed_json_list:
            keys = parsed_json_list[0].keys()
        
            table_result_widget.setColumnCount(len(keys))
            table_result_widget.setHorizontalHeaderLabels(keys)

            csv_rows=[]
            csv_rows.append(keys)

            for row_index, data_item in enumerate(parsed_json_list):
                table_result_widget.insertRow(row_index)
                row_values = []
                for column_index, key in enumerate(keys):
                    value = data_item.get(key, "")
                    if isinstance(value, list):
                        value = ', '.join(map(str, value))
                    table_result_widget.setItem(row_index, column_index, QTableWidgetItem(str(value)))
                    row_values.append(value)
                csv_rows.append(row_values)
                


    def result_partial_ready(self, result):
        self.result_layout_widget.update_progress_value(self.current_row,self.max_rows)
        text_result_widget = self.result_layout_widget.get_text_widget()
        text_result_widget.setText(text_result_widget.toPlainText() +'\n'+ json.dumps(result))
        self.current_row += 1

    def test_action(self):
        data = [
             ['Surname', 'Name', 'Occupation'],
             ['Król', 'Kacper', 'itsquad'],
             ['Kopernik', 'Mikołaj', 'astronom'],
             ['Konopnicka', 'Maria', 'pisarka']
                ]
        
        
        self.result_layout_widget.reset_result()
        self.update_preview_table(data)
        self.settings_layout_widget.my_list = data
        self.settings_layout_widget.available_fields = self.settings_layout_widget.my_list[0]
        self.settings_layout_widget.update_placeholder_list()
        self.settings_layout_widget.build_prompt_button.setEnabled(True)
        

        self.settings_layout_widget.query_text_edit.setText('{Surname} {Name} {Occupation}')
        self.settings_layout_widget.prompt_text_edit.setText('Znajdz informacje o wieku, miejscu zamieszkania, ciekawostka o tej osobie')
        self.settings_layout_widget.build_query_prompt()
        
    def result_reset(self):
        self.result_layout_widget.reset_result()
        self.current_row = 1

if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = MyWidget()
    # widget.resize(1000, 600)
    # widget.setFixedSize(1200, 700)
    widget.show()

    sys.exit(app.exec())
