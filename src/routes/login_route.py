from quart import Blueprint, request, jsonify, redirect, url_for, session, render_template, make_response, current_app

from src.model.account_model import AccountModel
from src.model.config_model import ConfigModel

login_blueprint = Blueprint('login', __name__, url_prefix='/login', template_folder='../templates',
                            static_folder='../static')


@login_blueprint.route('/', methods=['GET', 'POST'])
async def login():
    current_app.logger.debug("Login route hit with method: %s", request.method)
    try:
        if request.method == 'GET':
            # Simply render the login page if the request method is GET.
            return await render_template('login.html')

        elif request.method == 'POST':
            # Process the login credentials when a POST request is made.
            data = await request.form
            username = data.get('username')
            password = data.get('password')
            current_app.logger.debug("Processing form data: %s", username)

            account_model = AccountModel()

            if account_model.user_exists(username) and account_model.verify_user(username, password):
                # Load configurations (if needed) and set session variables.
                config_model = ConfigModel()
                config_model.load_configuration()

                session['api_key'] = config_model.api_key
                session['api_secret'] = config_model.api_secret
                session['logged_in'] = True  # Important: Set a session flag for logged-in status.

                # Redirect to the account page.
                return redirect(url_for('account.account'))

            elif account_model.user_exists(username):
                # Handle invalid credentials.
                return jsonify({'message': 'Invalid credentials'}), 401

            else:
                # Handle non-existent username.
                return jsonify({'message': 'Username does not exist'}), 404

    except Exception as e:
        current_app.logger.error("An error occurred: %s", str(e))
        return make_response(f"An error occurred: {str(e)}", 500)

    current_app.logger.error("Reached unexpected point in login function")
    return make_response("Unknown error", 500)
