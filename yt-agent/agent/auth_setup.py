"""
Run once, interactively, to generate secrets/token.json:
    python -m agent.auth_setup
Opens a browser for you to authorize the app against your YouTube channel.
After this, the loop runs unattended using the refresh token.
"""
from dotenv import load_dotenv
load_dotenv()

from agent.youtube_client import _get_credentials  # noqa: E402

if __name__ == "__main__":
    creds = _get_credentials()
    print("Auth successful. Token saved. You can now run the agent unattended.")
