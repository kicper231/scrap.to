import logging

from PySide6.QtWidgets import QMessageBox, QWidget


class ErrorHandler(QWidget):

    def show_error_message(self, message):
        logging.error(message)
        button = QMessageBox.critical(
            self,
            "Error!",
            str(message),
            buttons=QMessageBox.StandardButton.Discard,
            defaultButton=QMessageBox.StandardButton.Discard,
        )
