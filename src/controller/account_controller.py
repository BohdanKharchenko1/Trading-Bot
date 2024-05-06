from PyQt5 import QtWidgets


class AccountController:
    def __init__(self, view, model):
        self.view = view
        self.model = model
        self.connect_signals()

    def connect_signals(self):
        # Connect the "Create Account" button's clicked signal to the create_account method
        self.view.create_button.clicked.connect(self.create_account)
        self.view.delete_button.clicked.connect(self.delete_account)

    def create_account(self):
        username = self.view.username_line_edit.text().strip()
        password = self.view.password_line_edit.text().strip()

        if not username or not password:
            QtWidgets.QMessageBox.warning(self.view, 'Error', 'Username and password cannot be empty.')
            return

        try:
            # Additional validation can be performed here
            if " " in username:
                raise ValueError("Username should not contain spaces.")
            if len(password) < 6:
                raise ValueError("Password must be at least 6 characters long.")

            self.model.create_user(username, password)
            self.view.user_created_signal.emit(username)  # Emit a signal with the username
            QtWidgets.QMessageBox.information(self.view, 'Success', 'Account created successfully.')
            self.view.close()  # Optionally close the window after successful account creation
        except ValueError as e:
            QtWidgets.QMessageBox.critical(self.view, 'Error', str(e))
            print(f"Error creating user: {e}")
        except Exception as e:
            QtWidgets.QMessageBox.critical(self.view, 'Unexpected Error', 'An unexpected error occurred.')
            print(f"Unexpected error: {e}")

    def delete_account(self):
        username = self.view.username_line_edit.text().strip()

        if not username:
            QtWidgets.QMessageBox.warning(self.view, 'Error', 'Username cannot be empty.')
            return

        try:
            self.model.delete_user(username)
            QtWidgets.QMessageBox.information(self.view, 'Success', 'Account deleted successfully.')
        except ValueError as e:
            QtWidgets.QMessageBox.critical(self.view, 'Error', str(e))
        except Exception as e:
            QtWidgets.QMessageBox.critical(self.view, 'Unexpected Error',
                                           'An unexpected error occurred during deletion.')

    def verify_user(self):
        username = self.view.username_line_edit.text().strip()
        password = self.view.password_line_edit.text().strip()

        try:
            if self.model.verify_user(username, password):
                QtWidgets.QMessageBox.information(self.view, 'Success', 'Login successful.')
            else:
                QtWidgets.QMessageBox.warning(self.view, 'Error', 'Invalid username or password.')
        except Exception as e:
            QtWidgets.QMessageBox.critical(self.view, 'Error', 'Failed to verify user.')
            print(f"Error verifying user: {e}")
