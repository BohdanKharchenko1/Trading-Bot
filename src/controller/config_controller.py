from PyQt5 import QtWidgets


class ConfigController:
    def __init__(self, view, model):
        self.view = view
        self.model = model
        self.connect_signals()

    def connect_signals(self):
        self.view.test_button.clicked.connect(self._test_connection)
        self.view.save_button.clicked.connect(self._save_configuration)
        self.view.file_button.clicked.connect(self._load_credentials_from_file)

    def _test_connection(self):
        try:
            result = self.model.test_connection()
            if result is None:
                QtWidgets.QMessageBox.information(self.view, "Success", "Connection successful!")
            else:
                QtWidgets.QMessageBox.critical(self.view, "Error", f"Connection failed: {result}")
        except Exception as e:
            QtWidgets.QMessageBox.critical(self.view, "Error", f"Unexpected error: {e}")

    def _save_configuration(self):
        try:
            self.model.api_key = self.view.api_key.text()
            self.model.api_secret = self.view.api_secret.text()
            if self.model.save_configuration():
                QtWidgets.QMessageBox.information(self.view, "Success", "Configuration saved successfully.")
            else:
                QtWidgets.QMessageBox.critical(self.view, "Error", "Failed to save configuration.")
        except Exception as e:
            QtWidgets.QMessageBox.critical(self.view, "Error", f"Unexpected error while saving: {e}")

    def _load_credentials_from_file(self):
        try:
            options = QtWidgets.QFileDialog.Options()
            file_name, _ = QtWidgets.QFileDialog.getOpenFileName(self.view, "Select Configuration File", "",
                                                                 "Text Files (*.txt);;All Files (*)", options=options)
            if file_name:
                self.model.load_credentials_from_file(fileName)
                self.view.api_key.setText(self.model.api_key)
                self.view.api_secret.setText(self.model.api_secret)
                QtWidgets.QMessageBox.information(self.view, "Info", "API Key and Secret loaded successfully.")
        except Exception as e:
            QtWidgets.QMessageBox.critical(self.view, "Error", f"Unexpected error while loading file: {e}")
