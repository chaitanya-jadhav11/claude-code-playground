import os
import sys
import requests
from dotenv import load_dotenv

# Load variables from .env file
load_dotenv()

# Fetch token and target HTTP MCP server URL
TOKEN = os.getenv("GITHUB_PAT")
TARGET_URL = "https://githubcopilot.com"  # Replace with your specific server URL


def main():
    headers = {
        "Authorization": f"Bearer {TOKEN}",
        "Content-Type": "application/json"
    }

    # Read incoming JSON-RPC requests from Claude Code (stdin)
    for line in sys.stdin:
        try:
            # Forward the request to the remote GitHub HTTP MCP server
            response = requests.post(TARGET_URL, data=line, headers=headers)
            # Write the server's response back to Claude Code (stdout)
            sys.stdout.write(response.text + "\n")
            sys.stdout.flush()
        except Exception as e:
            sys.stderr.write(f"Proxy Error: {str(e)}\n")
            sys.stderr.flush()


if __name__ == "__main__":
    main()
