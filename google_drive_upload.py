from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import cv2
import numpy as np


def authenticate_drive():
    gauth = GoogleAuth()
    gauth.LocalWebserverAuth()  # Authenticates the user
    return GoogleDrive(gauth)


def upload_to_drive(image):
    drive = authenticate_drive()

    # Convert image to file
    filename = "leaf.jpg"
    cv2.imwrite(filename, image)

    file = drive.CreateFile({'title': filename})
    file.SetContentFile(filename)
    file.Upload()

    print(f"Uploaded {filename} to Google Drive")
