import unittest
from unittest.mock import MagicMock, patch
from src.controller.instruction_controller import InstructionController

class TestInstructionController(unittest.TestCase):
    def setUp(self):
        # Mock the view and model
        self.mock_view = MagicMock()
        self.mock_model = MagicMock()

        # Instantiate the controller with mocked components
        self.controller = InstructionController(view=self.mock_view, model=self.mock_model)

    def test_setup_connections(self):
        # Test that signals are connected correctly
        self.mock_view.load_instructions_signal.connect.assert_called_with(self.controller.display_instructions)

    @patch('builtins.print')  # Mock print to verify error handling output
    def test_display_instructions(self, mock_print):
        # Set up model to return some instructions
        self.mock_model.read_instructions.return_value = "Step 1: Connect power cable."

        # Execute the method
        self.controller.display_instructions()

        # Verify the instructions are displayed correctly
        self.mock_view.display_instructions.assert_called_once_with("Step 1: Connect power cable.")

    @patch('builtins.print')  # Mock print to verify error handling output
    def test_display_instructions_failure(self, mock_print):
        # Set up model to raise an exception
        self.mock_model.read_instructions.side_effect = Exception("File not found")

        # Execute the method
        self.controller.display_instructions()

        # Verify error handling
        mock_print.assert_called_with("Failed to load instructions: File not found")
        self.mock_view.display_instructions.assert_called_once_with(
            "An error occurred while loading instructions. Please check the log for details.")
