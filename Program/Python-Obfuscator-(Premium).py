from Config.Util import *
from Config.Config import *
try:
    import webbrowser
except Exception as e:
    ErrorModule(e)

Title("Python Obfuscator (Premium)")

try:
    print(f"\n{BEFORE + current_time_hour() + AFTER} {INFO} This product is paid for and available on our telegram.")
    webbrowser.open_new_tab(f"https://{telegram}")
    Continue()
    Reset()
except Exception as e:
    Error(e)