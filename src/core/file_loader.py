import openpyxl
from PySide6.QtWidgets import QFileDialog


class FileLoader:
    def __init__(self, delimiterBox):
        self.delimiterBox = delimiterBox

    def load_file(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(
            None,
            "Wybierz plik",
            "",
            "Pliki tekstowe (*.txt);;Pliki Excel (*.xlsx);;Wszystkie pliki (*)",
            options=options,
        )
        if file_path:
            return self.read_file(file_path)

    def read_file(self, file_path):
        if file_path.endswith(".xlsx"):
            workbook = openpyxl.load_workbook(file_path)
            sheet = workbook.active
            return [list(row) for row in sheet.values]
        elif file_path.endswith(".txt"):
            with open(file_path, mode="r", encoding="utf-8-sig") as file:
                return [
                    [
                        i.strip()
                        for i in line.strip().split(self.delimiterBox.currentText())
                    ]
                    for line in file.readlines()
                ]
