import unittest
from unittest.mock import mock_open, patch
from src.model.instruction_model import InstructionModel


class TestInstructionModel(unittest.TestCase):
    def setUp(self):
        self.model = InstructionModel()

    @patch('builtins.open', new_callable=mock_open, read_data="Follow these steps to set up your device.")
    def test_read_instructions_success(self, mock_file):
        # Test reading instructions successfully
        instructions = self.model.read_instructions()
        mock_file.assert_called_once_with(self.model.instruction_file_path, 'r', encoding='utf-8')
        self.assertEqual(instructions, "Follow these steps to set up your device.")

    @patch('builtins.open', mock_open(read_data="Follow these steps to set up your device."))
    def test_read_instructions_file_not_found(self, mock_file):
        # Test handling of FileNotFoundError
        instructions = self.model.read_instructions()
        self.assertEqual(instructions, "Instruction file not found.")

    @patch('builtins.open', mock_open(read_data="Follow these steps to set up your device."))
    def test_read_instructions_general_exception(self, mock_file):
        # Test handling of a general exception
        instructions = self.model.read_instructions()
        self.assertEqual(instructions, "An error occurred: Unexpected error")

