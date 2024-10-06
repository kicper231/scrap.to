from PySide6 import QtWidgets
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel, QProgressBar, QTableWidget, QTextEdit, QVBoxLayout


class ResultLayout(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()
        self.result_layout = QVBoxLayout(self)

        self.progress = QProgressBar(self)
        self.progress.setMaximum(100)
        self.progress_value = 0
        self.result_layout.addWidget(self.progress)

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

    def reset_result(self):
        self.progress.setValue(0)
        self.result_table_widget.reset()
        self.result_table_widget.setRowCount(0)
        self.result_table_widget.setColumnCount(0)
        self.result_text_widget.setText("")

    def update_progress_value(self, current, max):
        self.progress.setValue(int((current / max) * 100))

        if current == max:
            self.progress.setValue(100)

    def keyPressEvent(self, event):
        super().keyPressEvent(event)
        if event.key() == Qt.Key.Key_C and (
            event.modifiers() & Qt.KeyboardModifier.ControlModifier
        ):
            copied_cells = sorted(self.table_widget.selectedIndexes())

            copy_text = ""
            max_column = copied_cells[-1].column()
            for c in copied_cells:
                copy_text += self.table_widget.item(c.row(), c.column()).text()
                if c.column() == max_column:
                    copy_text += "\n"
                else:
                    copy_text += "\t"

            QtWidgets.QApplication.clipboard().setText(copy_text)
