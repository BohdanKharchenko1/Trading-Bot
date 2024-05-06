from PyQt5.QtWidgets import QApplication

from src.controller.account_controller import AccountController
from src.controller.instruction_controller import InstructionController
from src.controller.main_window_controller import MainWindowController
from src.controller.start_menu_controller import StartMenuController
from src.controller.web_controller import WebController
from src.model.account_interaction_model import AccountInteractionModel
from src.model.account_model import AccountModel
from src.model.config_model import ConfigModel
from src.model.instruction_model import InstructionModel
from src.model.main_window_model import MainWindowModel
from src.model.start_menu_model import StartMenuModel
from src.model.trading_data_fetcher import TradingDataFetcher
from src.model.web_model import WebModel
from src.view.account_window import AccountWindow
from src.view.instruction_window import InstructionWindow
from src.view.main_window import MainWindow
from src.view.start_menu_window import StartMenuWindow
from src.view.web_window import WebWindow


def main():
    try:
        # Redirect stderr

        app = QApplication([])

        model = ConfigModel(api_key="", api_secret="")
        model_main = MainWindowModel(model)
        trading_data_fetcher = TradingDataFetcher(model)
        start_menu_model = StartMenuModel(model)
        account_model = AccountInteractionModel(model)
        web_model = WebModel()
        user_account_model = AccountModel()
        instruction_model = InstructionModel()

        main_window = MainWindow()
        start_menu_window = StartMenuWindow()
        web_window = WebWindow()
        account_window = AccountWindow()
        instruction_window = InstructionWindow()

        main_window_controller = MainWindowController(main_window, model, model_main, start_menu_window, web_window,
                                                      account_window, instruction_window)
        start_menu_controller = StartMenuController(start_menu_window, start_menu_model, trading_data_fetcher,
                                                    account_model, model)
        web_controller = WebController(web_window, web_model, model)

        user_account_controller = AccountController(account_window, user_account_model)
        instruction_controller = InstructionController(instruction_window, instruction_model)

        main_window.show()
        app.exec_()
    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()
