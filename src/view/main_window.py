import pandas as pd
from PyQt5 import QtWidgets
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.figure = Figure(figsize=(5, 3))  # Adjust the figure size
        self.refresh_button = QtWidgets.QPushButton("Refresh Data")
        self.start_menu_button = QtWidgets.QPushButton("Start Trading")
        self.config_button = QtWidgets.QPushButton("Config")
        self.instruction_button = QtWidgets.QPushButton("Instructions")
        self.account_button = QtWidgets.QPushButton("Account")
        self.web_button = QtWidgets.QPushButton("Web")

        self.setWindowTitle("Trading Bot")
        self.initializeUI()

    def initializeUI(self):
        self.showFullScreen()
        central_widget = QtWidgets.QWidget(self)
        self.setCentralWidget(central_widget)

        # Main layout is horizontal: side menu | graph
        main_layout = QtWidgets.QHBoxLayout(central_widget)

        # Side menu layout with buttons
        side_menu_layout = QtWidgets.QVBoxLayout()

        # Add buttons to the side menu layout
        side_menu_layout.addWidget(self.start_menu_button)

        side_menu_layout.addWidget(self.web_button)

        side_menu_layout.addWidget(self.account_button)
        # Refresh Data button
        side_menu_layout.addWidget(self.config_button)

        side_menu_layout.addWidget(self.refresh_button)

        side_menu_layout.addWidget(self.instruction_button)

        # Add stretch to push everything up
        side_menu_layout.addStretch()

        main_layout.addLayout(side_menu_layout, 1)  # Add side menu layout to main layout

        # Setup for the graph
        self.canvas = FigureCanvas(self.figure)
        self.canvas.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)

        # Add the graph canvas to the main layout
        main_layout.addWidget(self.canvas, 4)  # Stretch factor 4 to give more space to graph

        central_widget.setLayout(main_layout)

    def plot_data(self, data):
        if data.empty or 'close' not in data.columns:
            QtWidgets.QMessageBox.critical(self, "Error", "No data to plot or missing 'close' column.")
            return

        try:
            # Ensure data is in the correct format
            data['close'] = pd.to_numeric(data['close'], errors='coerce')

            self.figure.clear()
            ax = self.figure.add_subplot(111)
            data['close'].dropna().plot(ax=ax, legend=True)
            ax.set_title('Bitcoin Prices Over the Last 7 Days')
            ax.set_ylabel('Price (USD)')
            ax.grid(True)
            self.canvas.draw()
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Plotting Error", str(e))
