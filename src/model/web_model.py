import secrets
from multiprocessing import Process

from quart import Quart, redirect, url_for

from src.routes.account_route import account_blueprint
from src.routes.login_route import login_blueprint

# Create an instance of the Quart web framework
app = Quart(__name__, template_folder='/templates', static_folder='/static')

# Set a secret key for the application
app.secret_key = secrets.token_urlsafe(24)

# Register blueprints with URL prefixes for account and login functionalities
app.register_blueprint(account_blueprint, url_prefix='/account')
app.register_blueprint(login_blueprint, url_prefix='/login')


@app.route('/')
async def home():
    """
    Redirects the default route to the login page.

    Returns:
        Response: A redirect response to the login blueprint's login page.
    """
    return redirect(url_for('login.login'))


def run_server(host, port):
    """
    Runs the Quart server with specified host and port.

    Parameters:
        host (str): Hostname or IP address to bind the server.
        port (int): The port number to bind the server.

    Returns:
        None
    """
    app.run(host=host, port=port, debug=True)


class WebModel:
    """
    A model to manage the web server's lifecycle including start and stop functionalities.
    """

    def __init__(self):
        """
        Initializes the WebModel instance, setting the server_process to None initially.
        """
        self.server_process = None

    def start_web_server(self, ip, port):
        """
        Starts the web server in a separate daemon process.

        Parameters:
            ip (str): IP address where the server should run.
            port (int): Port number for the server.

        Returns:
            None
        """
        try:
            if not self.server_process or not self.server_process.is_alive():
                self.server_process = Process(target=run_server, args=(ip, port), daemon=True)
                self.server_process.start()
                print(f"Web server process has started at {ip}:{port}.")
        except Exception as e:
            print(f"Failed to start web server at {ip}:{port}: {e}")

    def stop(self):
        """
        Stops the web server process if it is running.

        Returns:
            None
        """
        try:
            if self.server_process and self.server_process.is_alive():
                self.server_process.terminate()
                self.server_process.join()
                print("Web server process has been stopped.")
        except Exception as e:
            print("Failed to stop web server process:", e)
