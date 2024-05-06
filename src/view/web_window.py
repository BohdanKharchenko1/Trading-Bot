from PyQt5 import QtWidgets


class WebWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(WebWindow, self).__init__()

        # Initialize the UI
        self.save_button = QtWidgets.QPushButton("Save Configuration")
        self.port_input = QtWidgets.QLineEdit(self)
        self.ip_input = QtWidgets.QLineEdit(self)
        self.start_web_button = QtWidgets.QPushButton("Start Web")
        self.initializeUI()

    def initializeUI(self):
        """ Initialize the window and display its contents to the screen. """
        self.setWindowTitle('Start Web')
        self.setFixedSize(275, 150)

        # Set central widget and layout
        central_widget = QtWidgets.QWidget(self)
        self.setCentralWidget(central_widget)

        layout = QtWidgets.QVBoxLayout()
        central_widget.setLayout(layout)

        # Create a button
        self.start_web_button.clicked.connect(self.start_web_clicked)  # Connect the button to its function
        layout.addWidget(self.start_web_button)

        self.ip_input.setPlaceholderText("Enter IP Address")
        layout.addWidget(self.ip_input)

        # Create Port input
        self.port_input.setPlaceholderText("Enter Port Number")
        layout.addWidget(self.port_input)

        layout.addWidget(self.save_button)

    def start_web_clicked(self):
        print("Web server starting...")
