import sys
from PySide6 import QtCore, QtWidgets
import openpyxl
from PySide6.QtWidgets import QSpacerItem, QSizePolicy, QVBoxLayout, QPushButton, QFileDialog, QLineEdit, QSplitter, QListWidget, QListWidgetItem,QTextEdit, QTableWidgetItem, QHBoxLayout,QComboBox,QLabel

from PySide6.QtCore import Signal

class SettingsLayout(QtWidgets.QWidget):
    file_loaded = Signal(list)
    prompt_ready = Signal(list, list, str)

    def __init__(self):
        super().__init__()
        self.settings_layout = QVBoxLayout(self)
        spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        # Load File Button
        self.load_button = QPushButton('Załaduj plik')
        self.load_button.setFixedSize(100, 50)
        self.load_button.clicked.connect(self.load_file)

        # Delimiter Selection
        delimiterbox_layout = QVBoxLayout()
        delimiter_label = QLabel("Wybierz delimiter:")
        self.delimiterBox = QComboBox()
        self.delimiterBox.addItems([',', ';', '|'])
        delimiterbox_layout.addWidget(delimiter_label)
        delimiterbox_layout.addWidget(self.delimiterBox)

        # File Load Buttons Layout
        self.file_load_buttons_layout = QHBoxLayout()
        self.file_load_buttons_layout.addWidget(self.load_button)
        self.file_load_buttons_layout.addLayout(delimiterbox_layout)
        self.settings_layout.addLayout(self.file_load_buttons_layout)

        self.prompt_label = QLabel("Wprowadź prompt:")
        self.prompt_text_edit = QTextEdit()
        self.prompt_text_edit.setPlaceholderText("Wpisz swój prompt tutaj...")

        self.placeholder_label = QLabel("Wstaw zmienne:")
        self.placeholder_list_widget = QListWidget()
        self.placeholder_list_widget.setMaximumHeight(100)
        self.placeholder_list_widget.itemDoubleClicked.connect(self.insert_placeholder)

        self.mode_label = QLabel("Wybierz tryb:")
        self.mode_box = QComboBox()
        self.mode_box.addItems(['na podstawie url', 'wyszukaj url', 'to do'])

        self.build_prompt_button = QPushButton("Generuj Prompt")
        self.build_prompt_button.clicked.connect(self.build_prompt)
        self.build_prompt_button.setEnabled(False)

        self.settings_layout.addItem(spacer)
        self.settings_layout.addWidget(self.prompt_label)
        self.settings_layout.addWidget(self.prompt_text_edit)
        self.settings_layout.addWidget(self.placeholder_label)
        self.settings_layout.addWidget(self.placeholder_list_widget)
        self.settings_layout.addWidget(self.mode_label)
        self.settings_layout.addWidget(self.mode_box)
        self.settings_layout.addItem(spacer)
        self.settings_layout.addWidget(self.build_prompt_button)
        self.settings_layout.addStretch(1)



        # Initialize data
        self.my_list = []
        self.available_fields = []

    def load_file(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "Wybierz plik", "", 
                                                   "Pliki tekstowe (*.txt);;Pliki Excel (*.xlsx);;Wszystkie pliki (*)", 
                                                   options=options)
        if file_path:
            if file_path.endswith('.xlsx'):
                workbook = openpyxl.load_workbook(file_path)
                sheet = workbook.active
                list_values = list(sheet.values)
                self.my_list = [list(row) for row in list_values]
            elif file_path.endswith('.txt'):
                with open(file_path, mode='r', encoding='utf-8-sig') as file:
                    lines = file.readlines()
                self.my_list = [
                    [i.strip() for i in line.strip().split(self.delimiterBox.currentText())]
                    for line in lines
                ]

    
            if self.my_list:
                self.available_fields = self.my_list[0]
                self.update_placeholder_list()
                self.build_prompt_button.setEnabled(True)
                self.file_loaded.emit(self.my_list)

    def update_placeholder_list(self):
        self.placeholder_list_widget.clear()
        for field in self.available_fields:
            item = QListWidgetItem(f"{{{field}}}")
            self.placeholder_list_widget.addItem(item)

    def insert_placeholder(self, item):
        cursor = self.prompt_text_edit.textCursor()
        cursor.insertText(item.text())

    def build_prompt(self):
        prompt_template = self.prompt_text_edit.toPlainText()
        data_rows = self.my_list[1:] 
        prompts = []

        for row in data_rows:
            data_dict = dict(zip(self.available_fields, row))
            try:
                prompt = prompt_template.format(**data_dict)
                prompts.append(prompt)
            except KeyError as e:
                QtWidgets.QMessageBox.warning(
                    self, "Błąd", f"Brak klucza w danych: {e}"
                )
                return
        mode = self.mode_box.currentText()
        self.prompt_ready.emit(prompts, data_rows, mode)
        
                 

                 
                

