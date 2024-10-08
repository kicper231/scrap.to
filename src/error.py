from PySide6.QtWidgets import QMessageBox, QWidget


class Error(QWidget):

    def show_error_message(self, message):

        print(message)
        button = QMessageBox.critical(
            self,
            "Error!",
            str(message),
            buttons=QMessageBox.StandardButton.Discard,
            defaultButton=QMessageBox.StandardButton.Discard,
        )
