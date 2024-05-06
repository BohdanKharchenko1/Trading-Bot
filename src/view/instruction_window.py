from PyQt5 import QtWidgets, QtCore, QtGui


class InstructionWindow(QtWidgets.QDialog):
    load_instructions_signal = QtCore.pyqtSignal()

    def __init__(self):
        super().__init__()
        self.textEdit = QtWidgets.QTextEdit(self)
        self.initializeUI()

    def initializeUI(self):
        self.setWindowTitle("Instructions")
        self.setGeometry(300, 300, 700, 800)  # x, y, width, height
        self.textEdit.setReadOnly(True)

        # Set a default font for the QTextEdit
        default_font = QtGui.QFont("Times", 14)
        self.textEdit.setFont(default_font)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.textEdit)
        self.setLayout(layout)

        # Ensure the window has been fully set up before emitting the signal
        QtCore.QTimer.singleShot(0, self.load_instructions_signal.emit)

    def display_instructions(self, instructions):
        """
        Sets the text of the QTextEdit widget to the provided instructions, using HTML for formatting.
        """
        try:
            # Replace newlines with HTML paragraph tags to create paragraphs
            formatted_text = instructions.replace('\n', '<br>')  # Replace line breaks with HTML line breaks
            self.textEdit.setHtml(formatted_text)
        except Exception as e:
            error_message = f"Error displaying instructions: {str(e)}"
            print(error_message)  # Optionally log the error message
            self.textEdit.setText("Failed to display instructions due to an internal error.")
