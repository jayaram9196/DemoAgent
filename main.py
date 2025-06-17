import os
import subprocess
from dotenv import load_dotenv

load_dotenv()

port = os.environ.get("PORT", "10000")

# Correct ADK CLI syntax
subprocess.run([
    "adk", "web",
    ".",  # 👈 this is your agents directory (positional argument)
    "--host", "0.0.0.0",
    "--port", str(port)
])
