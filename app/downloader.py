# app/downloader.py

import requests

def download_recording(recording_url, save_path, auth_token):
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = requests.get(recording_url, headers=headers)
    if response.status_code == 200:
        with open(save_path, "wb") as f:
            f.write(response.content)
        return True
    return False
