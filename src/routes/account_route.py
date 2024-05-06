from quart import Blueprint, jsonify, request, render_template, abort, session, redirect, url_for

from src.model.account_interaction_model import AccountInteractionModel
from src.model.automated_trader import AutomatedTrader
from src.model.config_model import ConfigModel
from src.model.start_menu_model import StartMenuModel
from src.model.trading_data_fetcher import TradingDataFetcher

account_blueprint = Blueprint('account', __name__, url_prefix='/account', template_folder='../templates',
                              static_folder='../static')

# Global model instances
config_model = ConfigModel()
account_interaction_model = AccountInteractionModel(config_model)
trading_data_fetcher = TradingDataFetcher(config_model)
start_menu_model = StartMenuModel(config_model)
automated_trader = None  # This will hold the AutomatedTrader thread object


@account_blueprint.route('/')
async def account():
    try:
        if not session.get('logged_in'):
            return redirect(url_for('login.login'))
        return await render_template('account.html')
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@account_blueprint.route('/positions/<string:symbol>')
async def positions(symbol):
    try:
        positions = account_interaction_model.get_positions(symbol)
        return jsonify(positions)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@account_blueprint.route('/strategies', methods=['GET'])
async def get_strategies():
    try:
        strategies = config_model.load_trading_config()
        return jsonify(strategies) if strategies else (jsonify([]), 204)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@account_blueprint.route('/start_strategy', methods=['POST'])
async def start_strategy():
    global automated_trader
    try:
        data = await request.get_json()
        strategy_name = data.get('strategy')
        strategies = config_model.load_trading_config()
        strategy = next((s for s in strategies if s['name'] == strategy_name), None)
        if not strategy:
            abort(404, description="Strategy not found")

        if automated_trader:
            automated_trader.stop_trading()
            automated_trader.join()

        start_menu_model.set_current_strategy(strategy)
        automated_trader = AutomatedTrader(
            start_menu_model=start_menu_model,
            trading_data_fetcher=trading_data_fetcher,
            account_interaction_model=account_interaction_model
        )
        automated_trader.start()
        return jsonify({'message': f'Started strategy: {strategy_name}'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@account_blueprint.route('/stop_strategy', methods=['POST'])
async def stop_strategy():
    global automated_trader
    try:
        if automated_trader:
            automated_trader.stop_trading()
            automated_trader.join()
            response_message = 'Strategy stopped successfully.'
            automated_trader = None
        else:
            response_message = 'No strategy is currently running'
            return jsonify({'message': response_message}), 400
        return jsonify({'message': response_message}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@account_blueprint.route('/close_positions', methods=['POST'])
async def close_positions():
    try:
        data = await request.get_json()
        symbol = data.get('symbol', 'BTCUSDT')  # Default to BTCUSDT if not specified
        success = start_menu_model.close_all_positions(account_interaction_model)
        if success:
            return jsonify({'message': 'All positions closed successfully'})
        else:
            return jsonify({'message': 'Failed to close positions'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500
