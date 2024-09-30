import sys
from PySide6 import QtCore, QtWidgets
import openpyxl
from PySide6.QtWidgets import QVBoxLayout, QPushButton, QFileDialog, QLineEdit, QSplitter, QTableWidgetItem, QHBoxLayout
from preview_layout import PreviewLayout
from settings_layout import SettingsLayout
from result_layout import ResultLayout
from scrap_engine import SmartScraper
import os 
import json




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
        
        # load_dotenv()
        # api_key = os.getenv("OPEN_API_KEY")
        # print(api_key)

        # os.environ['OPEN_API_KEY'] = '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'

        # Polaczenie sygnałów
        self.settings_layout_widget.file_loaded.connect(self.update_preview_table)
        self.settings_layout_widget.result_ready.connect(self.update_result_table)
        
        self.splitter.addWidget(self.preview_layout_widget)
        self.splitter.addWidget(self.settings_layout_widget)
        self.splitter.addWidget(self.result_layout_widget)

        self.splitter.setStretchFactor(0, 1)
        self.splitter.setStretchFactor(1, 1)
        self.splitter.setStretchFactor(2, 1)

    def update_preview_table(self, list_values):
        table_widget = self.preview_layout_widget.get_table_widget()
        
        table_widget.setColumnCount(len(list_values[0]))
        table_widget.setHorizontalHeaderLabels(list_values[0])

        table_widget.setRowCount(0) 
        for row_index, value_tuple in enumerate(list_values[1:]):
            table_widget.insertRow(row_index)
            for column_index, value in enumerate(value_tuple):
                table_widget.setItem(row_index, column_index, QTableWidgetItem(str(value)))

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

            csv_text = self.convert_rows_to_csv_text(csv_rows)

            text_result_widget.setPlainText(csv_text)

    def convert_rows_to_csv_text(self, rows):
        import csv
        import io

        output = io.StringIO()
        writer = csv.writer(output, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for row in rows:
            writer.writerow(row)
        csv_text = output.getvalue()
        output.close()
        return csv_text

if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = MyWidget()
    widget.resize(1000, 600)
    widget.setFixedSize(1200, 700)
    widget.show()

    sys.exit(app.exec())
