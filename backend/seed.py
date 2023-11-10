import requests
import os

# add function file
url = "http://localhost:8000/functions/new_function"
files = {
    "file": open(os.path.join(os.getcwd(), "tests", "aplusb.py"), "rb"),
}

requests.post(url, files=files)


# add function file
url = "http://localhost:8000/algorithms/new_algo"
files = {
    "file": open(os.path.join(os.getcwd(), "tests", "aplusb.py"), "rb"),
}

requests.post(url, files=files)
