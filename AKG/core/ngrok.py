from pyngrok import ngrok
from config import NGROK_CONFIG

class NGROK:
    def __init__(self):
        print("NGROK Connected Successfully!")

        # Set the auth token from your config
        ngrok.set_auth_token(NGROK_CONFIG)

        # Create a tunnel to the specified port (5000 in this case)
        self.port_url = ngrok.connect(5000)

        # Store the public URL
        self.APP_URL = self.port_url

