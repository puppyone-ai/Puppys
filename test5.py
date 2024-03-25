import os
from datetime import datetime
import json

# get date and time
now = datetime.now()
date_str = now.strftime("%Y-%m-%d_%H-%M-%S")

# create folder, if not exist
folder_path = "history"  # Corrected the folder name from 'histoty' to 'history'
os.makedirs(folder_path, exist_ok=True)

# create a new file
file_path = os.path.join(folder_path, f"history_{date_str}.txt")


json=[{'action': 'ok', 'code': 'import requests\n\n# Attempting to retrieve the HTML content of the website https://news.ycombinator.com/\ntry:\n    response = requests.get("https://news.ycombinator.com/")\n    HTML_text = response.text\nexcept Exception as e:\n    # If there\'s an error, send a message to the user asking for help\n    HTML_text = self.send_message_to_human(f"😟: I encountered an error trying to fetch the HTML content: {str(e)}. Could you please assist?")\n    \nprint(HTML_text)', 'status': 'fixed'}]
# Directly convert the Python object to a JSON string
pretty_json = json.dumps([{"file_path": file_path, "date": date_str}], indent=4)

# Write the JSON string to a file
with open(file_path, "w") as file:
    file.write(pretty_json)
