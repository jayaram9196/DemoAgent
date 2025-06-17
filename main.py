import os
import subprocess

# Load .env variables if needed
from dotenv import load_dotenv
load_dotenv()

# Render provides PORT as an environment variable
port = os.environ.get("PORT", "8080")  # Default to 8080 if not set

# Launch the ADK Web server and expose to the internet
subprocess.run([
    "python",
    "-m", "google.adk.web",
    "--project", ".",               # current directory (where your __init__.py is)
    "--host", "0.0.0.0",
    "--port", port
])
