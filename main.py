import os
import subprocess
from dotenv import load_dotenv

load_dotenv()

port = os.environ.get("PORT", "10000")

# Use 'adk' CLI command, not 'python -m ...'
subprocess.run([
    "adk", "web",
    "--project", ".",
    "--host", "0.0.0.0",
    "--port", str(port)
])
