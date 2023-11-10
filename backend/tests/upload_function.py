import requests
import os

url = "http://localhost:8000/functions/new_file"
files = {
    "file": open(os.path.join(os.getcwd(), "tests", "aplusb.py"), "rb"),
}

response = requests.post(url, files=files)

print(response.status_code)
print(response.json())
