import json

from PyQt5 import QtWidgets, QtCore


class StartMenuWindow(QtWidgets.QMainWindow):
    strategy_selected = QtCore.pyqtSignal(str)
    cancel_orders_requested = QtCore.pyqtSignal()
    fetch_positions_requested = QtCore.pyqtSignal()

    def __init__(self):
        super(StartMenuWindow, self).__init__()
        self.cancel_orders_button = QtWidgets.QPushButton("Cancel All Orders")
        self.buttons = {}
        self.setWindowTitle("Trading Bot")
        self.current_strategy = None  # Initialize current_strategy to None

        # Adjust the size of the PnL button to a more standard size
        self.pnl_button = QtWidgets.QPushButton("Fetch Closed PnL")
        self.pnl_button.setMinimumSize(100, 30)  # Adjust to a more standard size
        self.pnl_button.clicked.connect(self.fetch_pnl_clicked)

        # Strategy buttons are made bigger and moved to the beginning
        self.positions_button = QtWidgets.QPushButton("Fetch Open Positions")
        self.positions_button.setMinimumSize(100, 30)
        self.positions_button.clicked.connect(self.fetch_positions_clicked)

        self.initializeUI()

    def initializeUI(self):
        try:
            self.cancel_orders_button.setMinimumSize(100, 30)
            self.cancel_orders_button.clicked.connect(self.cancel_orders_clicked)

            central_widget = QtWidgets.QWidget(self)
            self.setCentralWidget(central_widget)
            layout = QtWidgets.QVBoxLayout(central_widget)

            # Add strategy buttons dynamically with larger size at the beginning
            strategy_names = ["Conservative Strategy", "Moderate Strategy", "Aggressive Strategy"]
            for name in strategy_names:
                btn = QtWidgets.QPushButton(name)
                btn.setCheckable(True)
                btn.setMinimumSize(150, 50)  # Larger size for better visibility
                btn.clicked.connect(self.handle_button_click)
                layout.addWidget(btn)
                self.buttons[name] = btn

            # Add other operational buttons after strategy buttons
            layout.addWidget(self.pnl_button)
            layout.addWidget(self.positions_button)
            layout.addWidget(self.cancel_orders_button)
        except Exception as e:
            print(f"Error during UI initialization: {e}")

    def handle_button_click(self):
        try:
            sender = self.sender()
            for btn in self.buttons.values():
                if btn != sender:
                    btn.setChecked(False)
                    btn.setText(btn.text().replace(" - Running", ""))
            if sender.isChecked():
                self.current_strategy = sender.text().replace(" - Running", "")
                new_text = f"{self.current_strategy} - Running"
                sender.setText(new_text)
            else:
                self.current_strategy = None
                sender.setText(sender.text().replace(" - Running", ""))
            self.strategy_selected.emit(self.current_strategy)
        except Exception as e:
            print(f"Error handling button click: {e}")

    def update_button_text(self, running_strategy=None):
        try:
            self.current_strategy = running_strategy
            for name, btn in self.buttons.items():
                if running_strategy == name:
                    btn.setChecked(True)
                    btn.setText(f"{name} - Running")
                else:
                    btn.setChecked(False)
                    btn.setText(name.replace(" - Running", ""))
        except Exception as e:
            print(f"Error updating button text: {e}")

    def fetch_pnl_clicked(self):
        try:
            self.strategy_selected.emit('fetch_pnl')  # Emitting signal to fetch PnL
        except Exception as e:
            self.display_error(f"Failed to initiate PnL fetch: {str(e)}")  # Display error if signal emit fails

    def display_pnl(self, pnl):
        try:
            message = f"Total Closed PnL: ${pnl:.2f}"  # Formats the number to two decimal places
            QtWidgets.QMessageBox.information(self, "Closed PnL", message)
        except Exception as e:
            self.display_error(
                f"Failed to display PnL: {str(e)}")  # Display error if there's an issue in showing the message

    def display_error(self, message):
        try:
            QtWidgets.QMessageBox.critical(self, "Error", message)
        except Exception as e:
            print(f"Failed to display error message: {str(e)}")  # Logging to console if the message box fails

    def cancel_orders_clicked(self):
        try:
            self.cancel_orders_requested.emit()  # Emitting signal to cancel orders
        except Exception as e:
            self.display_error(f"Failed to cancel orders: {str(e)}")

    def show_message(self, message):
        try:
            QtWidgets.QMessageBox.information(self, "Message", message)
        except Exception as e:
            self.display_error(f"Failed to show message: {str(e)}")

    def fetch_positions_clicked(self):
        # When the button is clicked, emit a signal to the controller to fetch open positions
        self.fetch_positions_requested.emit()

    # Add a method to display positions
    def display_positions(self, positions):
        try:
            # Ensure that positions is not just a string representation but an actual dictionary
            if isinstance(positions, str):
                positions = json.loads(positions)  # Convert string to dictionary if needed

            positions_list = positions.get('list', [])  # Get the list of position dictionaries

            if positions_list:
                # Start an HTML table with headers
                message = '<table border="1" style="border-collapse: collapse;">'
                message += ('<tr>'
                            '<th>ID</th>'
                            '<th>Symbol</th>'
                            '<th>Size</th>'
                            '<th>Leverage</th>'
                            '<th>Avg Price</th>'
                            '<th>Mark Price</th>'
                            '<th>Side</th>'
                            '<th>Stop Loss</th>'
                            '<th>Take Profit</th>'
                            '<th>Unrealised PnL</th>'
                            '</tr>')

                # Fill the table rows with data from each position
                for pos in positions_list:
                    message += ('<tr>'
                                f'<td>{pos.get("id", "N/A")}</td>'
                                f'<td>{pos.get("symbol", "N/A")}</td>'
                                f'<td>{pos.get("size", "N/A")}</td>'
                                f'<td>{pos.get("leverage", "N/A")}</td>'
                                f'<td>{pos.get("avgPrice", "N/A")}</td>'
                                f'<td>{pos.get("markPrice", "N/A")}</td>'
                                f'<td>{pos.get("side", "N/A")}</td>'
                                f'<td>{pos.get("stopLoss", "N/A")}</td>'
                                f'<td>{pos.get("takeProfit", "N/A")}</td>'
                                f'<td>{pos.get("unrealisedPnl", "N/A")}</td>'
                                '</tr>')

                message += '</table>'  # Close the table tag
            else:
                message = "No open positions."

            QtWidgets.QMessageBox.information(self, "Open Positions", message)
        except Exception as e:
            self.display_error(f"Failed to display open positions: {str(e)}")

    # Assuming other parts of the code for StartMenuController and other classes remain the same.
