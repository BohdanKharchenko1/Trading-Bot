from PyQt5 import QtWidgets

from src.controller.config_controller import ConfigController
from src.view.account_window import AccountWindow
from src.view.config_window import ConfigWindow
from src.view.instruction_window import InstructionWindow
from src.view.start_menu_window import StartMenuWindow
from src.view.web_window import WebWindow


class MainWindowController:
    """
    A controller class to manage interactions within the main window of an application, handling the opening and
    operations of various related sub-windows.

    Attributes:
        _main_window (QtWidgets.QMainWindow): The main application window.
        _model_main (object): The main model that provides data and functionalities directly associated with the main window.
        _model_conf (object): The configuration model used for managing settings.
        _web_window (WebWindow): The web window for web-related interactions.
        _account_window (AccountWindow): The account management window.
        _config_window (ConfigWindow): The configuration window.
        _start_menu_window (StartMenuWindow): The start menu window.
        _config_controller (ConfigController): The controller for the configuration window.
        _instruction_window (InstructionWindow): The instruction display window.
    """

    def __init__(self, main_window, model_conf, model_main, start_menu_window, web_window, account_window,
                 instruction_window):
        """
        Initializes the MainWindowController with the main window and all related sub-components.

        Parameters:
                   main_window (QtWidgets.QMainWindow): The main window of the application.
                   model_conf (object): The configuration model.
                   model_main (object): The main model associated with the main window.
                   start_menu_window (StartMenuWindow): The start menu window.
                   web_window (WebWindow): The web interface window.
                   account_window (AccountWindow): The account management window.
                   instruction_window (InstructionWindow): The instruction display window.
        """
        self._main_window = main_window
        self._model_main = model_main
        self._model_conf = model_conf
        self._web_window = web_window
        self._account_window = account_window
        self._config_window = None
        self._start_menu_window = start_menu_window
        self._config_controller = None
        self._instruction_window = instruction_window
        self.setup_signals()

    def setup_signals(self):
        # Connect the configuration button signal to the method to open the config window
        self._main_window.config_button.clicked.connect(self.open_config_window)
        # Connect the refresh button signal to the method to refresh data
        self._main_window.refresh_button.clicked.connect(self.refresh_data)
        self._main_window.start_menu_button.clicked.connect(self.open_start_menu_window)
        self._main_window.web_button.clicked.connect(self.open_web_window)
        self._main_window.account_button.clicked.connect(self.open_account_window)
        self._main_window.instruction_button.clicked.connect(self.open_instruction_window)

    def open_config_window(self):
        try:
            # Initialize the configuration window and its controller if not already done
            if not self._config_window:
                self._config_window = ConfigWindow()
                self._config_controller = ConfigController(view=self._config_window, model=self._model_conf)

            # Set the configuration window as modal and display it
            self._config_window.setModal(True)
            result = self._config_window.exec_()  # Capture the dialog result if needed
            if result == QtWidgets.QDialog.Accepted:
                QtWidgets.QMessageBox.information(self._main_window, "Configuration",
                                                  "Configuration updated successfully.")
        except Exception as e:
            QtWidgets.QMessageBox.critical(self._main_window, "Error",
                                           f"Unexpected error while opening configuration window: {e}")

    def open_start_menu_window(self):
        try:
            # Check if the start menu window instance already exists
            if self._start_menu_window is None:
                print("Initializing StartMenuWindow.")
                self._start_menu_window = StartMenuWindow()
            else:
                print("StartMenuWindow already initialized.")

            # Check if the start menu window has already been displayed
            if self._start_menu_window.isVisible():
                print("StartMenuWindow is already visible.")
            else:
                print("Displaying StartMenuWindow.")
                self._start_menu_window.show()

        except Exception as e:
            # If an exception occurs, print it to the console
            print(f"Error while opening StartMenuWindow: {e}")
            QtWidgets.QMessageBox.critical(self._main_window, "Error",
                                           f"Unexpected error while opening StartMenuWindow: {e}")

    def open_web_window(self):
        try:
            # Check if the web window instance already exists
            if self._web_window is None:
                print("Initializing WebWindow.")
                self._web_window = WebWindow()
            else:
                print("WebWindow already initialized.")

            # Check if the web window has already been displayed
            if self._web_window.isVisible():
                print("WebWindow is already visible.")
            else:
                print("Displaying WebWindow.")
                self._web_window.show()

        except Exception as e:
            # If an exception occurs, print it to the console
            print(f"Error while opening WebWindow: {e}")
            QtWidgets.QMessageBox.critical(self._main_window, "Error",
                                           f"Unexpected error while opening WebWindow: {e}")

    def open_instruction_window(self):
        """
        Displays the account management window.
        """
        try:
            # Check if the web window instance already exists
            if self._instruction_window is None:
                print("Initializing InstructionWindow.")
                self._instruction_window = InstructionWindow()
            else:
                print("InstructionWindow already initialized.")

            # Check if the web window has already been displayed
            if self._instruction_window.isVisible():
                print("InstructionWindow is already visible.")
            else:
                print("Displaying InstructionWindow.")
                self._instruction_window.show()

        except Exception as e:
            # If an exception occurs, print it to the console
            print(f"Error while opening InstructionWindow: {e}")
            QtWidgets.QMessageBox.critical(self._instruction_window, "Error",
                                           f"Unexpected error while opening InstructionWindow: {e}")

    def open_account_window(self):
        """
        Displays the instruction window.
        """
        try:
            # Check if the web window instance already exists
            if self._account_window is None:
                print("Initializing WebWindow.")
                self._account_window = AccountWindow()
            else:
                print("WebWindow already initialized.")

            # Check if the web window has already been displayed
            if self._account_window.isVisible():
                print("WebWindow is already visible.")
            else:
                print("Displaying WebWindow.")
                self._account_window.show()

        except Exception as e:
            # If an exception occurs, print it to the console
            print(f"Error while opening AccountWindow: {e}")
            QtWidgets.QMessageBox.critical(self._main_window, "Error",
                                           f"Unexpected error while opening AccountWindow: {e}")

    def refresh_data(self):
        """
        Refreshes data in the main window, typically by fetching new data and updating displays.
        """
        try:
            data = self._model_main.fetch_data()
            if not data.empty:
                self._main_window.plot_data(data)
                QtWidgets.QMessageBox.information(self._main_window, "Data Refresh", "Graph updated successfully.")
            else:
                QtWidgets.QMessageBox.warning(self._main_window, "Data Refresh", "No new data to display.")
        except Exception as e:
            QtWidgets.QMessageBox.critical(self._main_window, "Error", f"Error refreshing data: {e}")