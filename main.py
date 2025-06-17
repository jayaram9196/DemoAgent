import os
import subprocess

from dotenv import load_dotenv
load_dotenv()

# Get the port Render expects your app to listen on
port = os.environ.get("PORT", "10000")  # Render sets this automatically

# Important: ADK Web must be told to bind to 0.0.0.0 and this port
subprocess.run([
    "python",
    "-m", "google.adk.web",
    "--project", ".",          # assumes __init__.py is in the root
    "--host", "0.0.0.0",       # required for public access on Render
    "--port", str(port)        # pass the port as a string
])
