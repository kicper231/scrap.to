import os

import openpyxl
from PySide6 import QtWidgets
from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QPushButton,
    QSizePolicy,
    QSpacerItem,
    QTextEdit,
    QVBoxLayout,
)

from enums import ChatModel, Mode
from scraper_engine import SmartScraper
from scraper_thread import ScraperThread


class SettingsLayout(QtWidgets.QWidget):
    file_loaded = Signal(list)
    prompt_ready = Signal(list, list, list, str)
    result_ready = Signal(list)
    result_partial_ready = Signal(dict)
    result_reset = Signal()
    test_ready = Signal()
    is_scrapping = False
    is_parrarel = False
    chat_model = ChatModel.GTP4oMini

    def __init__(self):
        super().__init__()
        self.settings_layout = QVBoxLayout(self)
        spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        api_key = os.getenv("OPEN_API_KEY")

        if api_key == None:
            file = open("apiKey.txt", "r")
            content = file.read()
            api_key = content
            file.close()

        self.scrapper = SmartScraper(api_key)

        self.load_button = QPushButton("Załaduj plik")
        self.load_button.setFixedSize(100, 50)
        self.load_button.clicked.connect(self.load_file)

        self.test_button = QPushButton()
        self.test_button.clicked.connect(self.emit_test)

        # Delimiter Selection
        delimiterbox_layout = QVBoxLayout()
        delimiter_label = QLabel("Wybierz delimiter:")
        self.delimiterBox = QComboBox()
        self.delimiterBox.addItems([",", ";", "|"])
        delimiterbox_layout.addWidget(delimiter_label)
        delimiterbox_layout.addWidget(self.delimiterBox)

        # File Load Buttons Layout
        self.file_load_buttons_layout = QHBoxLayout()
        self.file_load_buttons_layout.addWidget(self.load_button)
        self.file_load_buttons_layout.addLayout(delimiterbox_layout)
        self.settings_layout.addLayout(self.file_load_buttons_layout)

        self.mode_label = QLabel("Wybierz tryb:")
        self.mode_box = QComboBox()
        self.mode_box.addItems(["Find url", "Url", "to do"])
        self.mode_box.currentTextChanged.connect(self.change_mode)

        self.query_label = QLabel("Wprowadz query:")
        self.query_text_edit = QTextEdit()
        self.query_text_edit.setPlaceholderText("Wpisz swoje query tutaj...")
        self.query_text_edit.setMaximumHeight(60)
        self.query_text_edit.focusInEvent = self.create_focus_in_event(
            self.query_text_edit
        )

        self.url_label = QLabel("Wybierz która kolumna ma być url:")
        self.url_label.setVisible(False)
        self.url_box = QComboBox()
        self.url_box.setVisible(False)
        self.url_box.addItems([])

        self.prompt_label = QLabel("Wprowadź prompt:")
        self.prompt_text_edit = QTextEdit()
        self.prompt_text_edit.setPlaceholderText("Wpisz swój prompt tutaj...")
        self.prompt_text_edit.focusInEvent = self.create_focus_in_event(
            self.prompt_text_edit
        )

        self.placeholder_label = QLabel("Wstaw zmienne:")
        self.placeholder_list_widget = QListWidget()
        self.placeholder_list_widget.setMaximumHeight(100)
        self.placeholder_list_widget.itemClicked.connect(self.insert_placeholder)

        self.checkbox_label = QLabel("Dodatkowe ustawienia:")
        self.parrarel_checkbox = QCheckBox("Równoległe wykonanie")
        self.parrarel_checkbox.toggled.connect(self.parrarel_toggle)
        self.chatmodel_combobox = QComboBox()
        self.chatmodel_label = QLabel("Model czata")
        self.chatmodel_combobox.addItems(["gpt-4o-mini", "gpt-4o", "gtp-3.5-turbo"])

        self.build_prompt_button = QPushButton("Generuj")
        self.build_prompt_button.clicked.connect(self.build_query_prompt)
        self.build_prompt_button.setEnabled(False)

        self.settings_layout.addItem(spacer)
        self.settings_layout.addWidget(self.url_label)
        self.settings_layout.addWidget(self.url_box)

        self.settings_layout.addWidget(self.query_label)
        self.settings_layout.addWidget(self.query_text_edit)

        self.settings_layout.addWidget(self.prompt_label)
        self.settings_layout.addWidget(self.prompt_text_edit)

        self.settings_layout.addWidget(self.placeholder_label)
        self.settings_layout.addWidget(self.placeholder_list_widget)

        self.settings_layout.addWidget(self.mode_label)
        self.settings_layout.addWidget(self.mode_box)

        self.settings_layout.addWidget(self.checkbox_label)
        self.settings_layout.addWidget(self.parrarel_checkbox)

        self.settings_layout.addWidget(self.chatmodel_label)
        self.settings_layout.addWidget(self.chatmodel_combobox)

        self.settings_layout.addWidget(self.test_button)

        self.settings_layout.addItem(spacer)
        self.settings_layout.addItem(spacer)
        self.settings_layout.addItem(spacer)
        self.settings_layout.addWidget(self.build_prompt_button)

        self.settings_layout.addStretch(1)

        self.my_list = []
        self.available_fields = []

    def load_file(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Wybierz plik",
            "",
            "Pliki tekstowe (*.txt);;Pliki Excel (*.xlsx);;Wszystkie pliki (*)",
            options=options,
        )
        if file_path:
            if file_path.endswith(".xlsx"):
                workbook = openpyxl.load_workbook(file_path)
                sheet = workbook.active
                list_values = list(sheet.values)
                self.my_list = [list(row) for row in list_values]
            elif file_path.endswith(".txt"):
                with open(file_path, mode="r", encoding="utf-8-sig") as file:
                    lines = file.readlines()
                self.my_list = [
                    [
                        i.strip()
                        for i in line.strip().split(self.delimiterBox.currentText())
                    ]
                    for line in lines
                ]

            if self.my_list:
                self.available_fields = self.my_list[0]
                self.update_placeholder_list()
                self.build_prompt_button.setEnabled(True)
                self.file_loaded.emit(self.my_list)

    def create_focus_in_event(self, widget):
        def focus_in_event(event):
            widget.setFocus()
            self.last_focused_widget = widget
            return super(widget.__class__, widget).focusInEvent(event)

        return focus_in_event

    def update_placeholder_list(self):
        self.placeholder_list_widget.clear()
        self.url_box.clear()
        for field in self.available_fields:
            item = QListWidgetItem(f"{{{field}}}")
            self.url_box.addItem(field)
            self.placeholder_list_widget.addItem(item)

    def insert_placeholder(self, item):
        if self.last_focused_widget:
            cursor = self.last_focused_widget.textCursor()
            cursor.insertText(item.text())

    def change_mode(self):
        if self.mode_box.currentText() == "Url":
            self.url_box.setVisible(True)
            self.url_label.setVisible(True)
            self.query_label.setVisible(False)
            self.query_text_edit.setVisible(False)
        elif self.mode_box.currentText() == "Find url":
            self.url_box.setVisible(False)
            self.url_label.setVisible(False)
            self.query_label.setVisible(True)
            self.query_text_edit.setVisible(True)

    def build_query_prompt(self):

        if not self.is_scrapping:
            prompt_template = self.prompt_text_edit.toPlainText()
            query_template = self.query_text_edit.toPlainText()
            self.chatmodel = ChatModel(self.chatmodel_combobox.currentText())
            mode = Mode(self.mode_box.currentText())

            self.is_scrapping = True
            self.build_prompt_button.setText("Zatrzymaj scrapowanie")

            keys = self.my_list[0]
            data_rows = self.my_list[1:]
            prompts = []
            queries = []
            urls = []
            index = 0

            for i, elem in enumerate(keys):
                if elem == self.url_box.currentText():
                    index = i

            for row in data_rows:
                data_dict = dict(zip(self.available_fields, row))
                try:
                    prompt = prompt_template.format(**data_dict)
                    prompts.append(prompt)

                    if mode == Mode.FIND_URL:
                        query = query_template.format(**data_dict)
                        queries.append(query)

                    if mode == Mode.URL:
                        urls.append(row[index])

                except KeyError as e:
                    QtWidgets.QMessageBox.warning(
                        self, "Błąd", f"Brak klucza w danych: {e}"
                    )
                    return

            self.result_reset.emit()
            self.is_scrapping = True
            self.scraper_thread = ScraperThread(
                self.scrapper,
                queries,
                prompts,
                urls,
                mode,
                self.is_parrarel,
                self.chat_model.value,
            )
            self.scraper_thread.result_partial_ready.connect(self.result_partial_ready)
            self.scraper_thread.result_ready.connect(self.result_ready.emit)
            self.scraper_thread.start()

        else:
            self.scraper_thread.stop_flag = True
            self.is_scrapping = False
            self.build_prompt_button.setText("Generuj")

    def emit_partial_result(self, result):
        self.result_partial_ready.emit(result)

    def emit_test(self):
        self.test_ready.emit()

    def parrarel_toggle(self):
        self.is_parrarel = not self.is_parrarel
