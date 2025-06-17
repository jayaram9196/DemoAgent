import os
import subprocess
from dotenv import load_dotenv

load_dotenv()

port = os.environ.get("PORT", "10000")

subprocess.run([
    "python",
    "-m", "google_adk",       # ✅ correct CLI module
    "--project", ".",         # assumes __init__.py is in root
    "--host", "0.0.0.0",      # required for public access
    "--port", str(port)
])
