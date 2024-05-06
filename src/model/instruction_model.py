import os


class InstructionModel:
    """
    A class designed to manage and read instructional text from a file located in the project's documentation folder.

    Attributes:
        instruction_file_path (str): The file path to the instruction text file within the project structure.
    """

    def __init__(self):
        """
        Initializes the InstructionModel by setting the path to the instruction file based on the project structure.
        """
        # Establishing the directory paths relative to the current file location
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(os.path.dirname(current_dir))
        # Combining path components to form the full path to the instructions file
        self.instruction_file_path = os.path.join(project_root, 'docs', 'instructions.txt')

    def read_instructions(self):
        """
        Reads the contents of the instruction file and returns it as a string.

        Returns:
            str: The contents of the instruction file if it exists and is readable,
                 an error message if the file is not found or an error occurs during reading.
        """
        try:
            with open(self.instruction_file_path, 'r', encoding='utf-8') as file:
                instructions = file.read()
            return instructions
        except FileNotFoundError:
            return "Instruction file not found."
        except Exception as e:
            return f"An error occurred: {str(e)}"
