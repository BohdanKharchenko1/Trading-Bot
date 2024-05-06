import unittest
from unittest.mock import MagicMock, patch
from PyQt5 import QtWidgets
from src.controller.account_controller import AccountController


class TestAccountController(unittest.TestCase):
    def setUp(self):
        # Mock the view and model
        self.mock_view = MagicMock()
        self.mock_model = MagicMock()
        self.mock_view.create_button = MagicMock()
        self.mock_view.delete_button = MagicMock()
        self.mock_view.username_line_edit = MagicMock()
        self.mock_view.password_line_edit = MagicMock()
        self.mock_view.user_created_signal = MagicMock()

        # Instantiate the controller
        self.controller = AccountController(self.mock_view, self.mock_model)

    def test_connect_signals(self):
        # Test that signals are connected correctly
        self.mock_view.create_button.clicked.connect.assert_called_with(self.controller.create_account)
        self.mock_view.delete_button.clicked.connect.assert_called_with(self.controller.delete_account)

    @patch('PyQt5.QtWidgets.QMessageBox')
    def test_create_account(self, mock_message_box):
        # Setup
        self.mock_view.username_line_edit.text.return_value = "john"
        self.mock_view.password_line_edit.text.return_value = "pass1234"

        # Action
        self.controller.create_account()

        # Assert
        self.mock_model.create_user.assert_called_once_with("john", "pass1234")
        mock_message_box.information.assert_called_once()
        self.mock_view.close.assert_called_once()

    @patch('PyQt5.QtWidgets.QMessageBox')
    def test_create_account_failure(self, mock_message_box):
        # Setup invalid data
        self.mock_view.username_line_edit.text.return_value = "john"
        self.mock_view.password_line_edit.text.return_value = "pass"  # Password too short

        # Action
        self.controller.create_account()

        # Assert
        mock_message_box.critical.assert_called_once()
        self.mock_model.create_user.assert_not_called()
        self.mock_view.close.assert_not_called()

    @patch('PyQt5.QtWidgets.QMessageBox')
    def test_delete_account(self, mock_message_box):
        # Setup
        self.mock_view.username_line_edit.text.return_value = "john"

        # Action
        self.controller.delete_account()

        # Assert
        self.mock_model.delete_user.assert_called_once_with("john")
        mock_message_box.information.assert_called_once()

    @patch('PyQt5.QtWidgets.QMessageBox')
    def test_delete_account_failure(self, mock_message_box):
        # Setup
        self.mock_view.username_line_edit.text.return_value = ""

        # Action
        self.controller.delete_account()

        # Assert
        mock_message_box.warning.assert_called_once()
        self.mock_model.delete_user.assert_not_called()

    @patch('PyQt5.QtWidgets.QMessageBox')
    def test_verify_user(self, mock_message_box):
        # Setup
        self.mock_view.username_line_edit.text.return_value = "john"
        self.mock_view.password_line_edit.text.return_value = "pass1234"
        self.mock_model.verify_user.return_value = True

        # Action
        self.controller.verify_user()

        # Assert
        self.mock_model.verify_user.assert_called_once_with("john", "pass1234")
        mock_message_box.information.assert_called_once()

    @patch('PyQt5.QtWidgets.QMessageBox')
    def test_verify_user_failure(self, mock_message_box):
        # Setup
        self.mock_view.username_line_edit.text.return_value = "john"
        self.mock_view.password_line_edit.text.return_value = "wrongpass"
        self.mock_model.verify_user.return_value = False

        # Action
        self.controller.verify_user()

        # Assert
        mock_message_box.warning.assert_called_once()
