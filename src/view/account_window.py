from PyQt5 import QtWidgets, QtCore


class AccountWindow(QtWidgets.QMainWindow):
    user_created_signal = QtCore.pyqtSignal(str)

    def __init__(self):
        super(AccountWindow, self).__init__()
        self.delete_button = QtWidgets.QPushButton("Delete Account")
        self.create_button = QtWidgets.QPushButton("Create Account")
        self.password_line_edit = QtWidgets.QLineEdit()
        self.password_label = QtWidgets.QLabel("Password:")
        self.username_line_edit = QtWidgets.QLineEdit()
        self.username_label = QtWidgets.QLabel("Username:")
        self.initializeUI()

    def initializeUI(self):
        self.setWindowTitle('Create Account')
        self.setGeometry(100, 100, 400, 200)
        self.setFixedSize(self.size())

        # Set central widget and layout
        central_widget = QtWidgets.QWidget(self)
        self.setCentralWidget(central_widget)
        layout = QtWidgets.QVBoxLayout(central_widget)

        # Create username and password labels and line edits
        self.password_line_edit.setEchoMode(QtWidgets.QLineEdit.Password)

        # Create a button to submit the create account form

        # Add widgets to layout
        layout.addWidget(self.username_label)
        layout.addWidget(self.username_line_edit)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_line_edit)
        layout.addWidget(self.create_button)
        layout.addWidget(self.delete_button)
