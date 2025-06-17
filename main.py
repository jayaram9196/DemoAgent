
import os
import subprocess
from dotenv import load_dotenv

load_dotenv()

port = os.environ.get("PORT", "10000")

subprocess.run([
    "python",
    "-m", "google.adk.web",
    "--project", ".",
    "--host", "0.0.0.0",
    "--port", str(port)
])
