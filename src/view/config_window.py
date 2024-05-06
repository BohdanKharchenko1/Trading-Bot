from PyQt5 import QtWidgets, QtCore


class ConfigWindow(QtWidgets.QDialog):
    fileChosen = QtCore.pyqtSignal(str)

    def __init__(self, parent=None):
        super(ConfigWindow, self).__init__(parent)
        self.buttonBox = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel,
                                                    self)
        self.file_button = QtWidgets.QPushButton("Choose File", self)
        self.test_button = QtWidgets.QPushButton("Test Connection", self)
        self.save_button = QtWidgets.QPushButton("Save Configuration", self)
        self.api_key = QtWidgets.QLineEdit(self)
        self.api_secret = QtWidgets.QLineEdit(self)
        self.layout = QtWidgets.QVBoxLayout()
        self.setWindowTitle('Configurations')
        self.setGeometry(100, 100, 400, 200)
        self.initializeUI()

    def initializeUI(self):
        # Input field 1
        self.api_key.setPlaceholderText("API Key")
        self.layout.addWidget(self.api_key)

        # Input field 2
        self.api_secret.setPlaceholderText("API Secret")
        self.layout.addWidget(self.api_secret)

        # Save Configuration button
        self.save_button.clicked.connect(self.saveConfiguration)
        self.layout.addWidget(self.save_button)

        # Test Connection button
        self.test_button.clicked.connect(self.testConnection)
        self.layout.addWidget(self.test_button)

        # File selection button
        self.file_button.clicked.connect(self.openFileNameDialog)
        self.layout.addWidget(self.file_button)

        # OK and Cancel buttons
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        self.layout.addWidget(self.buttonBox)

        self.setLayout(self.layout)

    def openFileNameDialog(self):
        options = QtWidgets.QFileDialog.Options()
        # Set the filter to Text Files (*.txt) and All Files (*)
        file_name, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Select Configuration File", "",
                                                             "Text Files (*.txt);;All Files (*)", options=options)
        if fileName:
            self.fileChosen.emit(file_name)

    def get_file_from_user(self):
        # Call this function to open the dialog and get the file path
        self.openFileNameDialog()
        # After the dialog is closed, return the selected file path
        return getattr(self, 'file_path', None)

    def saveConfiguration(self):
        # Save the configuration to a file or settings
        print("Configuration saved!")

    def testConnection(self):
        # Code to test the connection
        print("Testing connection...")
