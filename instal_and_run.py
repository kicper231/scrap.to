import os
import subprocess

subprocess.check_call(
    [os.sys.executable, "-m", "pip", "install", "-r", "requirements.txt"]
)

subprocess.check_call([os.sys.executable, "src/main.py"])
