from PyQt5 import QtWidgets

class WebController:
    """
    A controller class that handles user interactions from the GUI for managing web server configurations
    and operations.

    Attributes:
        view (QtWidgets.QMainWindow): The main window view which contains the GUI elements.
        model (object): The model used for starting and managing the web server.
        config_model (object): The configuration model used for saving and loading web server settings.
    """

    def __init__(self, view, model, config_model):
        """
        Initializes the WebController with the main view, the model for web server operations, and the
        configuration model for handling settings.

        Parameters:
            view (QtWidgets.QMainWindow): The main window view which contains the GUI elements.
            model (object): The model used for starting and managing the web server.
            config_model (object): The configuration model used for saving and loading web server settings.
        """
        self.view = view
        self.model = model
        self.config_model = config_model
        self.connect_signals()
        self.load_and_display_web_configuration()

    def connect_signals(self):
        """
        Connects GUI elements with the corresponding methods to handle events like button clicks.
        """
        self.view.start_web_button.clicked.connect(self.start_web_server)
        self.view.save_button.clicked.connect(self.save_configuration)

    def load_and_display_web_configuration(self):
        """
        Loads web configuration settings from the configuration model and displays them in the GUI.
        """
        # Attempt to load existing configuration and display it
        ip_address, port = self.config_model.load_web_configuration()
        if ip_address and port:
            self.view.ip_input.setText(ip_address)
            self.view.port_input.setText(str(port))

    def start_web_server(self):
        """
        Starts the web server using the IP address and port specified in the GUI input fields.
        Displays a message box indicating the success or failure of the operation.
        """
        ip_address = self.view.ip_input.text()
        port = self.view.port_input.text()
        if not ip_address or not port:  # If fields are empty, try loading the configuration
            ip_address, port = self.config_model.load_web_configuration()
        if self.validate_ip_port(ip_address, port):
            self.model.start_web_server(ip_address, int(port))  # Assuming the model has this method
            QtWidgets.QMessageBox.information(self.view, "Server Starting", f"Starting server at {ip_address}:{port}")

    def save_configuration(self):
        """
        Saves the IP address and port configuration entered in the GUI to the configuration model.
        Displays a message box indicating the success or failure of the save operation.
        """
        ip_address = self.view.ip_input.text()
        port = self.view.port_input.text()
        if self.validate_ip_port(ip_address, port):
            if self.config_model.save_web_configuration(ip_address, int(port)):
                QtWidgets.QMessageBox.information(self.view, "Success", "Configuration saved successfully.")
            else:
                QtWidgets.QMessageBox.warning(self.view, "Failed", "Failed to save configuration.")

    def validate_ip_port(self, ip, port):
        """
        Validates the IP address and port number provided in the GUI.

        Parameters:
            ip (str): The IP address as input by the user.
            port (str): The port number as input by the user.

        Returns:
            bool: True if both the IP and port are valid, False otherwise.
        """
        if not ip:
            QtWidgets.QMessageBox.warning(self.view, "Input Error", "Please enter a valid IP address.")
            return False
        try:
            port = int(port)
            if port < 1 or port > 65535:
                raise ValueError("Port out of range")
        except ValueError:
            QtWidgets.QMessageBox.warning(self.view, "Input Error", "Please enter a valid port number.")
            return False
        return True
