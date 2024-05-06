class InstructionController:
    def __init__(self, view, model):
        self.view = view
        self.model = model
        self.setup_connections()

    def setup_connections(self):
        """
        Connects the view's signal to fetch instructions to the controller's method.
        """
        self.view.load_instructions_signal.connect(self.display_instructions)

    def display_instructions(self):
        """
        Fetches instructions from the model and displays them in the view.
        """
        try:
            instructions = self.model.read_instructions()
            self.view.display_instructions(instructions)
        except Exception as e:
            error_message = f"Failed to load instructions: {str(e)}"
            print(error_message)  # Optionally log the error message to the console or a log file.
            self.view.display_instructions(
                "An error occurred while loading instructions. Please check the log for details.")
